from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re

rgz = Blueprint(
    'rgz',
    __name__,
    template_folder='templates/rgz',
    static_folder='static'
)

def get_db():
    return psycopg2.connect(
        dbname="shopdb",
        user="roman_fomchenko_rgz_base",
        password="111",
        host="localhost",
        cursor_factory=psycopg2.extras.RealDictCursor
    )

def get_user():
    uid = session.get("rgz_user_id")
    if not uid:
        return None
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (uid,))
    user = cur.fetchone()
    conn.close()
    return user

def valid_login(username):
    return bool(re.fullmatch(r"[A-Za-z0-9_.-]{3,30}", username))

def valid_pass(password):
    return bool(re.fullmatch(r"[A-Za-z0-9!@#$%^&*()_+.-]{6,50}", password))

@rgz.route("/rgz")
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()
    return render_template("index.html", products=products, user=get_user())

@rgz.route("/rgz/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        full_name = request.form["full_name"].strip()
        group = request.form["student_group"].strip()

        if not valid_login(username):
            flash("Логин некорректный")
            return redirect(url_for("rgz.register"))

        if not valid_pass(password):
            flash("Пароль некорректный")
            return redirect(url_for("rgz.register"))

        ph = generate_password_hash(password)

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO users (username, password_hash, full_name, student_group)
                VALUES (%s, %s, %s, %s)
            """, (username, ph, full_name, group))
            conn.commit()
        except psycopg2.Error:
            flash("Пользователь с таким логином уже существует")
            conn.close()
            return redirect(url_for("rgz.register"))

        conn.close()
        flash("Регистрация прошла успешно, войдите в систему")
        return redirect(url_for("rgz.login"))

    return render_template("register.html", user=get_user())

@rgz.route("/rgz/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["rgz_user_id"] = user["id"]
            flash("Вы успешно вошли")
            return redirect(url_for("rgz.index"))
        
        flash("Неверный логин или пароль")

    return render_template("login.html", user=get_user())

@rgz.route("/rgz/logout")
def logout():
    session.pop("rgz_user_id", None)
    flash("Вы вышли из аккаунта")
    return redirect(url_for("rgz.index"))

@rgz.route("/rgz/add/<int:pid>", methods=["POST"])
def add(pid):
    user = get_user()
    if not user:
        flash("Сначала войдите в аккаунт")
        return redirect(url_for("rgz.login"))

    q = int(request.form.get("quantity", 1))

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, quantity FROM cart_items WHERE user_id=%s AND product_id=%s",
        (user["id"], pid)
    )
    row = cur.fetchone()

    if row:
        cur.execute(
            "UPDATE cart_items SET quantity=quantity+%s WHERE id=%s",
            (q, row["id"])
        )
    else:
        cur.execute(
            "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (%s, %s, %s)",
            (user["id"], pid, q)
        )

    conn.commit()
    conn.close()

    flash("Товар добавлен в корзину")
    return redirect(url_for("rgz.index"))

@rgz.route("/rgz/cart")
def cart():
    user = get_user()
    if not user:
        flash("Сначала войдите в аккаунт")
        return redirect(url_for("rgz.login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT ci.id AS cart_id, p.name, p.price, ci.quantity,
               (p.price * ci.quantity) AS subtotal
        FROM cart_items ci
        JOIN products p ON p.id = ci.product_id
        WHERE ci.user_id=%s
    """, (user["id"],))

    items = cur.fetchall()
    conn.close()

    total = sum(i["subtotal"] for i in items) if items else 0
    return render_template("cart.html", items=items, total=total, user=user)

@rgz.route("/rgz/remove/<int:cid>", methods=["POST"])
def remove(cid):
    user = get_user()
    if not user:
        return redirect(url_for("rgz.login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM cart_items WHERE id=%s AND user_id=%s",
        (cid, user["id"])
    )
    conn.commit()
    conn.close()

    flash("Товар удалён из корзины")
    return redirect(url_for("rgz.cart"))

@rgz.route("/rgz/checkout", methods=["GET", "POST"])
def checkout():
    user = get_user()
    if not user:
        return redirect(url_for("rgz.login"))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.id, p.name, p.price, ci.quantity
        FROM cart_items ci
        JOIN products p ON p.id = ci.product_id
        WHERE ci.user_id=%s
    """, (user["id"],))

    items = cur.fetchall()

    if not items:
        flash("Корзина пуста")
        conn.close()
        return redirect(url_for("rgz.cart"))

    total = sum(i["price"] * i["quantity"] for i in items)

    if request.method == "POST":
        cur.execute("""
            INSERT INTO orders (user_id, created_at, total)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (user["id"], datetime.now(), total))

        oid = cur.fetchone()["id"]

        for i in items:
            cur.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (oid, i["id"], i["quantity"], i["price"]))

        cur.execute("DELETE FROM cart_items WHERE user_id=%s", (user["id"],))
        conn.commit()
        conn.close()

        flash("Заказ оформлен")
        return redirect(url_for("rgz.index"))

    conn.close()
    return render_template("checkout.html", items=items, total=total, user=user)