# create_db.py
import os
import sys

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from db import db
from db.models import users, articles
from werkzeug.security import generate_password_hash

print("Инициализация базы данных...")

with app.app_context():
    # Создаем таблицы
    print("Создание таблиц...")
    db.create_all()
    
    # Создаем тестового пользователя
    user_count = users.query.count()
    if user_count == 0:
        test_user = users(
            login="admin",
            password=generate_password_hash("admin123")
        )
        db.session.add(test_user)
        db.session.commit()
        print("✅ Создан тестовый пользователь:")
        print("   Логин: admin")
        print("   Пароль: admin123")
    
    print(f"✅ База данных создана!")
    print(f"   Пользователей: {users.query.count()}")
    print(f"   Статей: {articles.query.count()}")