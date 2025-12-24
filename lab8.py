from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from db import db
from db.models import users, articles
from functools import wraps

lab8 = Blueprint('lab8', __name__, template_folder='templates')

# ========== ДЕКОРАТОР ДЛЯ ПРОВЕРКИ АВТОРИЗАЦИИ ==========
def login_required_decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Для доступа к этой странице необходимо войти в систему', 'error')
            return redirect('/lab8/login')
        return f(*args, **kwargs)
    return decorated_function


@lab8.route('/')
def index():
    username = "anonymous"
    user_articles = []
    
    if 'user_id' in session:
        user = users.query.get(session['user_id'])
        if user:
            username = user.login
            user_articles = articles.query.filter_by(login_id=user.id).all()
    
    return render_template('lab8/index.html', 
                          username=username, 
                          user_articles=user_articles,
                          config={'SQLALCHEMY_DATABASE_URI': 'sqlite:///roman_fomchenko_orm.db'})


@lab8.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    if not login_form or not password_form:
        flash('Логин и пароль не могут быть пустыми', 'error')
        return render_template('lab8/register.html')
    
    if len(login_form) < 3:
        flash('Логин должен содержать минимум 3 символа', 'error')
        return render_template('lab8/register.html')
    
    if len(password_form) < 3:
        flash('Пароль должен содержать минимум 3 символа', 'error')
        return render_template('lab8/register.html')
    
    try:
        login_exists = users.query.filter_by(login=login_form).first()
    except Exception as e:
        flash(f'Ошибка базы данных: {str(e)}', 'error')
        return render_template('lab8/register.html')
    
    if login_exists:
        flash('Такой пользователь уже существует', 'error')
        return render_template('lab8/register.html')
    
    try:
        password_hash = generate_password_hash(password_form)
        new_user = users(login=login_form, password=password_hash)
        
        db.session.add(new_user)
        db.session.commit()
        
        # ✅ АВТОМАТИЧЕСКИЙ ЛОГИН ПОСЛЕ РЕГИСТРАЦИИ
        session['user_id'] = new_user.id
        login_user(new_user, remember=False)
        
        flash('Регистрация успешна! Вы автоматически вошли в систему.', 'success')
        return redirect('/lab8/')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при регистрации: {str(e)}', 'error')
        return render_template('lab8/register.html')


@lab8.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = 'remember' in request.form  # ✅ ГАЛОЧКА "ЗАПОМНИТЬ МЕНЯ"
    
    if not login_form or not password_form:
        flash('Логин и пароль не могут быть пустыми', 'error')
        return render_template('lab8/login.html')
    
    user = users.query.filter_by(login=login_form).first()
    
    if not user:
        flash('Пользователь не найден', 'error')
        return render_template('lab8/login.html')
    
    if not check_password_hash(user.password, password_form):
        flash('Неверный пароль', 'error')
        return render_template('lab8/login.html')
    
    # ✅ ИСПОЛЬЗУЕМ ПАРАМЕТР REMEMBER ИЗ ФОРМЫ
    login_user(user, remember=remember_me)  
    session['user_id'] = user.id
    
    # Делаем сессию постоянной если галочка установлена
    if remember_me:
        session.permanent = True
    
    flash('Вы успешно вошли в систему!', 'success')
    return redirect('/lab8/')


@lab8.route('/articles')
@login_required_decorator  # ✅ ЗАЩИЩАЕМ ДОСТУП
def articles_list():
    try:
        public_articles = articles.query.filter_by(is_public=True).all()
    except:
        public_articles = []
    
    user_articles = []
    if 'user_id' in session:
        try:
            user_articles = articles.query.filter_by(login_id=session['user_id']).all()
        except:
            user_articles = []
    
    return render_template('lab8/articles.html', 
                          public_articles=public_articles,
                          user_articles=user_articles)


@lab8.route('/create', methods=['GET', 'POST'])
@login_required_decorator  # ✅ ЗАЩИЩАЕМ ДОСТУП
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title_form = request.form.get('title')
    article_text_form = request.form.get('article_text')
    is_favorite_form = 'is_favorite' in request.form
    is_public_form = 'is_public' in request.form
    
    if not title_form or not article_text_form:
        return render_template('lab8/create.html', 
                              error='Заголовок и текст статьи не могут быть пустыми')
    
    if len(title_form) > 50:
        return render_template('lab8/create.html', 
                              error='Заголовок не может превышать 50 символов')
    
    try:
        new_article = articles(
            login_id=session['user_id'],
            title=title_form,
            article_text=article_text_form,
            is_favorite=is_favorite_form,
            is_public=is_public_form,
            likes=0
        )
        
        db.session.add(new_article)
        db.session.commit()
        
        flash('Статья успешно создана!', 'success')
        return redirect('/lab8/articles')
    except Exception as e:
        return render_template('lab8/create.html', 
                              error=f'Ошибка сохранения: {str(e)}')


@lab8.route('/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required_decorator  # ✅ ЗАЩИЩАЕМ ДОСТУП
def edit_article(article_id):
    try:
        article = articles.query.get_or_404(article_id)
        
        if article.login_id != session['user_id']:
            flash('Вы не можете редактировать чужую статью', 'error')
            return redirect('/lab8/articles')
        
        if request.method == 'GET':
            return render_template('lab8/edit.html', article=article)
        
        title_form = request.form.get('title')
        article_text_form = request.form.get('article_text')
        is_favorite_form = 'is_favorite' in request.form
        is_public_form = 'is_public' in request.form
        
        if not title_form or not article_text_form:
            return render_template('lab8/edit.html', 
                                  article=article,
                                  error='Заголовок и текст статьи не могут быть пустыми')
        
        article.title = title_form
        article.article_text = article_text_form
        article.is_favorite = is_favorite_form
        article.is_public = is_public_form
        
        db.session.commit()
        
        flash('Статья успешно обновлена!', 'success')
        return redirect('/lab8/articles')
    except:
        flash('Ошибка при редактировании статьи', 'error')
        return redirect('/lab8/articles')


@lab8.route('/delete/<int:article_id>')
@login_required_decorator  # ✅ ЗАЩИЩАЕМ ДОСТУП
def delete_article(article_id):
    try:
        article = articles.query.get_or_404(article_id)
        
        if article.login_id != session['user_id']:
            flash('Вы не можете удалить чужую статью', 'error')
            return redirect('/lab8/articles')
        
        db.session.delete(article)
        db.session.commit()
        
        flash('Статья успешно удалена!', 'success')
        return redirect('/lab8/articles')
    except:
        flash('Ошибка при удалении статьи', 'error')
        return redirect('/lab8/articles')


@lab8.route('/like/<int:article_id>')
def like_article(article_id):
    try:
        article = articles.query.get_or_404(article_id)
        article.likes = article.likes + 1
        db.session.commit()
        flash('Статья оценена!', 'success')
    except:
        flash('Ошибка при оценке статьи', 'error')
    
    return redirect('/lab8/articles')


@lab8.route('/favorites')
@login_required_decorator
def favorites():
    try:
        favorite_articles = articles.query.filter_by(
            login_id=session['user_id'],
            is_favorite=True
        ).all()
    except:
        favorite_articles = []
    
    return render_template('lab8/favorites.html', 
                          favorite_articles=favorite_articles)


@lab8.route('/logout')
def logout():
    logout_user()
    session.pop('user_id', None)
    session.permanent = False
    flash('Вы успешно вышли из системы', 'success')
    return redirect('/lab8/')


@lab8.route('/test')
def test():
    return '✅ Лабораторная работа 8 работает!'