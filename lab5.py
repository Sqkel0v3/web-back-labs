from flask import Blueprint, render_template, request, session, redirect, current_app, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='roman_fomchenko_knowledge_base',
            user='roman_fomchenko_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5')
@lab5.route('/lab5/')
def lab():
    return render_template('lab5/index.html', login=session.get('login'))

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    try:
        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT login FROM users WHERE login=?;", (login,))

        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        password_hash = generate_password_hash(password)
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
        else:
            cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))

        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)
    
    except Exception as e:
        return render_template('lab5/register.html', error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not login or not password:
        return render_template('lab5/login.html', error="Заполните поля")
    
    try:
        conn, cur = db_connect()
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        session['login'] = login
        session['user_id'] = user['id']
        db_close(conn, cur)
        return render_template('lab5/success_login.html', login=login)
    
    except Exception as e:
        return render_template('lab5/login.html', error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    return redirect('/lab5')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    user_id = user['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY id DESC;", (user_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=? ORDER BY id DESC;", (user_id,))

    articles = cur.fetchall()
    
    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles, login=login)

# Создание статьи
@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create_article():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните название и текст статьи')
    
    if len(title) > 50:
        return render_template('lab5/create_article.html', error='Название статьи не должно превышать 50 символов')
    
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    user_id = user['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles (user_id, title, article_text, is_favorite, is_public, likes) VALUES (%s, %s, %s, %s, %s, %s);", 
                   (user_id, title, article_text, False, False, 0))
    else:
        cur.execute("INSERT INTO articles (user_id, title, article_text, is_favorite, is_public, likes) VALUES (?, ?, ?, ?, ?, ?);", 
                   (user_id, title, article_text, False, False, 0))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, session.get('user_id')))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, session.get('user_id')))
    
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return redirect('/lab5/list')
    
    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    
    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error='Заполните название и текст статьи')
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", 
                   (title, article_text, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", 
                   (title, article_text, article_id))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, session.get('user_id')))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, session.get('user_id')))
    
    article = cur.fetchone()
    
    if article:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
        else:
            cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))
    
    db_close(conn, cur)
    return redirect('/lab5/list')