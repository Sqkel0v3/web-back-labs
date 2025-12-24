from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles

lab8 = Blueprint('lab8', __name__, template_folder='templates')

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
                          user_articles=user_articles)

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
        
        session['user_id'] = new_user.id
        flash('Регистрация успешна! Добро пожаловать!', 'success')
        return redirect('/lab8/')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при регистрации: {str(e)}', 'error')
        return render_template('lab8/register.html')

@lab8.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    try:
        login_form = request.form.get('login')
        password_form = request.form.get('password')
        
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
        
        session['user_id'] = user.id
        session.permanent = True
        
        flash('Вы успешно вошли в систему!', 'success')
        return redirect('/lab8/')
        
    except Exception as e:
        current_app.logger.error(f'Ошибка при входе: {str(e)}')
        flash(f'Ошибка при входе: {str(e)}', 'error')
        return render_template('lab8/login.html')
    
@lab8.route('/articles')
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
def create_article():
    if 'user_id' not in session:
        return redirect('/lab8/login')
    
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
        
        return redirect('/lab8/articles')
    except Exception as e:
        return render_template('lab8/create.html', 
                              error=f'Ошибка сохранения: {str(e)}')

@lab8.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    if 'user_id' not in session:
        return redirect('/lab8/login')
    
    try:
        article = articles.query.get_or_404(article_id)
        
        if article.login_id != session['user_id']:
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
        
        return redirect('/lab8/articles')
    except:
        return redirect('/lab8/articles')

@lab8.route('/delete/<int:article_id>')
def delete_article(article_id):
    if 'user_id' not in session:
        return redirect('/lab8/login')
    
    try:
        article = articles.query.get_or_404(article_id)
        
        if article.login_id != session['user_id']:
            return redirect('/lab8/articles')
        
        db.session.delete(article)
        db.session.commit()
        
        return redirect('/lab8/articles')
    except:
        return redirect('/lab8/articles')

@lab8.route('/like/<int:article_id>')
def like_article(article_id):
    try:
        article = articles.query.get_or_404(article_id)
        article.likes = article.likes + 1
        db.session.commit()
    except:
        pass
    
    return redirect('/lab8/articles')

@lab8.route('/favorites')
def favorites():
    if 'user_id' not in session:
        return redirect('/lab8/login')
    
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
    session.pop('user_id', None)
    return redirect('/lab8/')

@lab8.route('/search', methods=['GET', 'POST'])
def search_articles():
    if request.method == 'GET':
        return render_template('lab8/search.html')
    
    search_query = request.form.get('query', '')
    
    if not search_query:
        return render_template('lab8/search.html', 
                              error='Введите поисковый запрос')
    
    try:
        found_articles = articles.query.filter(
            (articles.title.contains(search_query)) | 
            (articles.article_text.contains(search_query))
        ).filter_by(is_public=True).all()
    except:
        found_articles = []
    
    return render_template('lab8/search.html', 
                          search_query=search_query,
                          found_articles=found_articles)

# Тестовый маршрут для проверки
@lab8.route('/test')
def test():
    return '✅ Лабораторная работа 8 работает!'