from flask import Blueprint, render_template, request, session, redirect
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5')
@lab5.route('/lab5/')  # Добавьте этот маршрут
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
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='roman_fomchenko_knowledge_base',
            user='roman_fomchenko_knowledge_base',
            password='123'
        )
        cur = conn.cursor()

        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password))
        conn.commit()
        cur.close()
        conn.close()

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
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='roman_fomchenko_knowledge_base',
            user='roman_fomchenko_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
        user = cur.fetchone()
        
        if not user:
            cur.close()
            conn.close()
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        if user['password'] != password:
            cur.close()
            conn.close()
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        session['login'] = login
        cur.close()
        conn.close()
        return render_template('lab5/success_login.html', login=login)
    
    except Exception as e:
        return render_template('lab5/login.html', error=f'Ошибка базы данных: {str(e)}')

@lab5.route('/lab5/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab5')

@lab5.route('/lab5/list')
def list_articles():
    return "Список статей"

@lab5.route('/lab5/create')
def create_article():
    return "Создание статьи"