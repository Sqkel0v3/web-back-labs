from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import os

lab7 = Blueprint('lab7', __name__)

DB_CONFIG = {
    'dbname': 'roman_fomchenko_knowledge_base',
    'user': 'roman_fomchenko_knowledge_base',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    """Создание соединения с PostgreSQL БД"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"ОШИБКА ПОДКЛЮЧЕНИЯ К БД: {e}")
        return None

def validate_film(film_data):
    """ПОЛНАЯ ВАЛИДАЦИЯ ВСЕХ ПОЛЕЙ ФИЛЬМА"""
    errors = {}
    current_year = datetime.now().year

    title_ru = film_data.get('title_ru', '').strip()
    if not title_ru:
        errors['title_ru'] = 'Русское название обязательно'

    title = film_data.get('title', '').strip()
    if not title_ru and not title:
        errors['title'] = 'Оригинальное название обязательно если русское название не задано'

    if 'year' not in film_data or film_data['year'] == '':
        errors['year'] = 'Год обязателен'
    else:
        try:
            year = int(film_data['year'])
            if year < 1895:
                errors['year'] = f'Год должен быть не ранее 1895 (первый фильм "Прибытие поезда")'
            elif year > current_year:
                errors['year'] = f'Год не может быть больше {current_year}'
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'

    description = film_data.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание обязательно'
    elif len(description) > 2000:
        errors['description'] = f'Описание не должно превышать 2000 символов (сейчас: {len(description)})'
    
    return errors

@lab7.route('/lab7/')
def main():
    """Главная страница лабораторной"""
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    """ПОЛУЧИТЬ ВСЕ ФИЛЬМЫ ИЗ БД"""
    conn = get_db_connection()
    if not conn:

        return jsonify([
            {"id": 1, "title": "Test Film", "title_ru": "Тестовый фильм", "year": 2024, "description": "Тестовое описание"}
        ])
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute('SELECT id, title, title_ru, year, description FROM films ORDER BY id')
        films = cursor.fetchall()
        return jsonify(films)
    except Exception as e:
        return jsonify({"error": f"Ошибка при получении фильмов: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    """ПОЛУЧИТЬ ОДИН ФИЛЬМ ПО ID"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "База данных не доступна"}), 500
    
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute('SELECT id, title, title_ru, year, description FROM films WHERE id = %s', (id,))
        film = cursor.fetchone()
        
        if not film:
            return jsonify({"error": "Фильм не найден"}), 404
        
        return jsonify(film)
    except Exception as e:
        return jsonify({"error": f"Ошибка при получении фильма: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    """УДАЛИТЬ ФИЛЬМ ПО ID"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "База данных не доступна"}), 500
    
    cursor = conn.cursor()
    
    try:

        cursor.execute('SELECT id FROM films WHERE id = %s', (id,))
        if not cursor.fetchone():
            return jsonify({"error": "Фильм не найден"}), 404

        cursor.execute('DELETE FROM films WHERE id = %s', (id,))
        conn.commit()
        
        return '', 204
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка при удалении фильма: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    """ОБНОВИТЬ ФИЛЬМ ПО ID"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "База данных не доступна"}), 500
    
    cursor = conn.cursor()
    
    try:

        cursor.execute('SELECT id FROM films WHERE id = %s', (id,))
        if not cursor.fetchone():
            return jsonify({"error": "Фильм не найден"}), 404
        
        film_data = request.get_json()

        errors = validate_film(film_data)
        if errors:
            return jsonify(errors), 400

        title = film_data.get('title', '').strip()
        title_ru = film_data.get('title_ru', '').strip()
        if not title and title_ru:
            film_data['title'] = title_ru

        cursor.execute('''
            UPDATE films 
            SET title = %s, title_ru = %s, year = %s, description = %s
            WHERE id = %s
        ''', (
            film_data['title'],
            film_data['title_ru'],
            int(film_data['year']),
            film_data['description'],
            id
        ))
        
        conn.commit()
        
        return jsonify({
            'id': id,
            'title': film_data['title'],
            'title_ru': film_data['title_ru'],
            'year': int(film_data['year']),
            'description': film_data['description']
        })
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка при обновлении фильма: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    """ДОБАВИТЬ НОВЫЙ ФИЛЬМ"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "База данных не доступна"}), 500
    
    cursor = conn.cursor()
    
    try:
        film_data = request.get_json()

        errors = validate_film(film_data)
        if errors:
            return jsonify(errors), 400

        title = film_data.get('title', '').strip()
        title_ru = film_data.get('title_ru', '').strip()
        if not title and title_ru:
            film_data['title'] = title_ru

        cursor.execute('''
            INSERT INTO films (title, title_ru, year, description)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        ''', (
            film_data['title'],
            film_data['title_ru'],
            int(film_data['year']),
            film_data['description']
        ))

        new_id = cursor.fetchone()[0]
        
        conn.commit()
        
        return jsonify(new_id)
    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Ошибка при добавлении фильма: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()