import os
import sys

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("Инициализация базы данных для lab8")
print("=" * 50)

try:
    from app import app
    from db import db
    from db.models import users, articles
    from werkzeug.security import generate_password_hash
    
    print(" Модули успешно импортированы")
    
    with app.app_context():
        print("Создание таблиц в базе данных...")
        
        # Создаем таблицы
        db.create_all()
        print(" Таблицы созданы")
        
        # Создаем тестового пользователя
        user_count = users.query.count()
        if user_count == 0:
            test_user = users(
                login="admin",
                password=generate_password_hash("admin123")
            )
            db.session.add(test_user)
            db.session.commit()
            print(" Создан тестовый пользователь:")
            print("   Логин: admin")
            print("   Пароль: admin123")
        else:
            print(f" В базе уже есть {user_count} пользователей")
        
        articles_count = articles.query.count()
        print(f" База данных готова к использованию!")
        print(f"   Всего пользователей: {user_count}")
        print(f"   Всего статей: {articles_count}")
        
except Exception as e:
    print(f" Ошибка: {e}")
    import traceback
    traceback.print_exc()
