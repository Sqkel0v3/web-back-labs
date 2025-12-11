from flask import Flask, request, render_template
import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from db import db
from dotenv import load_dotenv
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from rgz import rgz

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'roman_fomchenko_orm'
    db_user = 'roman_fomchenko_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432
    
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "ivan_ivanov_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(rgz)

if __name__ == '__main__':
    app.run(debug=True)

error_404_log = []

@app.errorhandler(404)
def not_found(err):
    # Получаем информацию о текущем запросе
    client_ip = request.remote_addr
    current_time = datetime.datetime.now()
    requested_url = request.url
    user_agent = request.headers.get('User-Agent', 'Неизвестный')
    
    # Добавляем запись в лог
    log_entry = {
        'timestamp': current_time,
        'ip': client_ip,
        'url': requested_url,
        'user_agent': user_agent
    }
    error_404_log.append(log_entry)
    
    # Ограничиваем лог последними 20 записями
    if len(error_404_log) > 20:
        error_404_log.pop(0)
    
    # Форматируем журнал для отображения
    journal_html = ""
    for entry in reversed(error_404_log[-10:]):  # Показываем последние 10 записей
        formatted_time = entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        journal_html += f"""
        <div class="log-entry">
            <span class="log-time">[{formatted_time}]</span>
            <span class="log-ip">пользователь {entry['ip']}</span>
            <span class="log-url">зашёл на адрес: {entry['url']}</span>
        </div>
        """
    
    return f"""<!doctype html>
<html>
<head>
    <title>404 - Страница не найдена</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            text-align: center;
            max-width: 900px;
            margin: 20px;
            backdrop-filter: blur(10px);
        }}
        .error-code {{
            font-size: 120px;
            font-weight: bold;
            color: #ff6b6b;
            margin: 0;
            text-shadow: 3px 3px 0 rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #2c3e50;
            margin: 10px 0 20px 0;
            font-size: 2.5em;
        }}
        p {{
            font-size: 1.2em;
            line-height: 1.6;
            color: #555;
            margin-bottom: 30px;
        }}
        .info-section {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: left;
            border-left: 5px solid #74b9ff;
        }}
        .info-section h3 {{
            color: #2d3436;
            margin-top: 0;
            border-bottom: 2px solid #74b9ff;
            padding-bottom: 10px;
        }}
        .info-item {{
            margin: 10px 0;
            padding: 8px;
            background: white;
            border-radius: 8px;
            border-left: 3px solid #ffeaa7;
        }}
        .info-label {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .journal-section {{
            background: #2c3e50;
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: left;
            max-height: 300px;
            overflow-y: auto;
        }}
        .journal-section h3 {{
            color: #ffeaa7;
            margin-top: 0;
            text-align: center;
            font-size: 1.5em;
            border-bottom: 2px solid #ffeaa7;
            padding-bottom: 10px;
        }}
        .log-entry {{
            background: rgba(255, 255, 255, 0.1);
            padding: 12px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #ff6b6b;
            font-family: monospace;
            font-size: 0.9em;
            line-height: 1.4;
        }}
        .log-time {{
            color: #74b9ff;
        }}
        .log-ip {{
            color: #ffeaa7;
            margin: 0 10px;
        }}
        .log-url {{
            color: #a29bfe;
        }}
        .emoji {{
            font-size: 80px;
            margin: 20px 0;
            animation: bounce 2s infinite;
        }}
        @keyframes bounce {{
            0%, 20%, 50%, 80%, 100% {{transform: translateY(0);}}
            40% {{transform: translateY(-20px);}}
            60% {{transform: translateY(-10px);}}
        }}
        .home-button {{
            display: inline-block;
            padding: 15px 30px;
            background: linear-gradient(45deg, #ff6b6b, #ee5a52);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            font-size: 1.1em;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
            margin: 10px;
        }}
        .home-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.6);
            background: linear-gradient(45deg, #ee5a52, #ff6b6b);
        }}
        .search-icon {{
            width: 100px;
            height: 100px;
            margin: 20px auto;
            background: #ffeaa7;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            color: #ff6b6b;
            box-shadow: 0 5px 15px rgba(255, 234, 167, 0.5);
        }}
        .advice {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            border-left: 5px solid #74b9ff;
        }}
        .advice h3 {{
            color: #2d3436;
            margin-top: 0;
        }}
        .image-container {{
            margin: 40px 0;
        }}
        .image-container img {{
            width: 450px;
            height: 300px;
            object-fit: cover;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            border: 5px solid #fff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="error-code">404</div>
        <div class="emoji">🔍</div>
        <h1>Ой! Кажется, мы потерялись...</h1>

        <div class="info-section">
            <h3>Информация о запросе</h3>
            <div class="info-item">
                <span class="info-label">Ваш IP-адрес:</span> {client_ip}
            </div>
            <div class="info-item">
                <span class="info-label">Дата и время:</span> {current_time.strftime('%Y-%m-%d %H:%M:%S')}
            </div>
            <div class="info-item">
                <span class="info-label">Запрошенный адрес:</span> {requested_url}
            </div>
            <div class="info-item">
                <span class="info-label">Браузер:</span> {user_agent}
            </div>
        </div>

        <div class="image-container">
            <img src="/static/kotik.jpg" alt="Милый котик">
        </div>
        
        <div class="search-icon">
            ❓
        </div>
        
        <div class="advice">
            <h3>Что можно сделать?</h3>
            <p>• Проверьте адрес страницы<br>
               • Вернитесь на главную<br>
               • Или просто наслаждайтесь видом этой красивой ошибки </p>
        </div>
        
        <a href="/" class="home-button">Вернуться домой</a>

        <div class="journal-section">
            <h3> Журнал 404 ошибок</h3>
            {journal_html if journal_html else '<div class="log-entry">Пока нет записей в журнале</div>'}
        </div>

    </div>
</body>
</html>""", 404

from flask import render_template_string

@app.route("/error/500")
def cause_error():
    result = 10 / 0
    return "Этот код никогда не выполнится"

@app.errorhandler(500)
def internal_server_error(err):
    error_message = str(err) if err else "Внутренняя ошибка сервера"
    
    return render_template_string("""
<!doctype html>
<html>
<head>
    <title>500 - Ошибка сервера</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            text-align: center;
            max-width: 700px;
            margin: 20px;
            backdrop-filter: blur(10px);
        }
        .error-code {
            font-size: 120px;
            font-weight: bold;
            color: #ff6b6b;
            margin: 0;
            text-shadow: 3px 3px 0 rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #2c3e50;
            margin: 10px 0 20px 0;
            font-size: 2.5em;
        }
        p {
            font-size: 1.2em;
            line-height: 1.6;
            color: #555;
            margin-bottom: 20px;
        }
        .error-details {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            border-left: 5px solid #74b9ff;
            text-align: left;
            font-family: monospace;
            overflow-x: auto;
        }
        .emoji {
            font-size: 80px;
            margin: 20px 0;
            animation: shake 0.5s infinite;
        }
        @keyframes shake {
            0%, 100% {transform: translateX(0);}
            25% {transform: translateX(-5px);}
            75% {transform: translateX(5px);}
        }
        .home-button {
            display: inline-block;
            padding: 15px 30px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            font-size: 1.1em;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            margin: 10px;
        }
        .home-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }
        .support-button {
            display: inline-block;
            padding: 15px 30px;
            background: linear-gradient(45deg, #f19066, #f5cd79);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            font-size: 1.1em;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(241, 144, 102, 0.4);
            margin: 10px;
        }
        .support-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(241, 144, 102, 0.6);
        }
        .advice {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            border-left: 5px solid #74b9ff;
        }
        .advice h3 {
            color: #2d3436;
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="error-code">500</div>
        <h1>Упс! Что-то пошло не так</h1>
        
        <p>На сервере произошла непредвиденная ошибка. Наша команда уже уведомлена и работает над решением проблемы.</p>
        
        <div class="error-details">
            <strong>Детали ошибки:</strong><br>
            {{ error_message }}
        </div>
        
        <div class="advice">
            <h3>Что можно сделать?</h3>
            <p>• Попробуйте обновить страницу через несколько минут<br>
               • Вернитесь на главную страницу<br>
               • Если проблема повторяется, свяжитесь с поддержкой</p>
        </div>
        
        <div>
            <a href="/" class="home-button">Вернуться на главную</a>
        </div>
    </div>
</body>
</html>
""", error_message=error_message), 500

count = 0

@app.route("/")
@app.route("/index")
def index():
    return """<!doctype html>
<html>
<head>
    <title>НГТУ, ФБ, Лабораторные работы</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        header {
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 10px 10px 0 0;
            margin: -30px -30px 30px -30px;
        }
        header h1 {
            margin: 0;
            font-size: 2.2em;
        }
        nav {
            background: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        nav ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        nav li {
            margin: 10px 0;
        }
        nav a {
            display: block;
            padding: 12px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            transition: background 0.3s ease;
            font-weight: bold;
        }
        nav a:hover {
            background: #2980b9;
            transform: translateX(5px);
        }
        footer {
            margin-top: 40px;
            padding: 20px;
            background: #34495e;
            color: white;
            text-align: center;
            border-radius: 0 0 10px 10px;
            margin: 30px -30px -30px -30px;
        }
        .lab-list {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>HГТУ, ФБ, WEB-программирование, часть 2</h1>
            <p>Список лабораторных работ</p>
        </header>

        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2">Вторая лабораторная</a></li>
                <li><a href="/lab3">Третья лабораторная</a></li>
                <li><a href="/lab4">Четвертая лабораторная</a></li>
                <li><a href="/lab5">Пятая лабораторная</a></li>
                <li><a href="/lab6">Шестая лабораторная</a></li>
                <li><a href="/lab7">Седьмая лабораторная</a></li>
                <li><a href="/lab8">Восьмая лабораторная</a></li>
                <li><a href="/rgz">РГЗ</a></li>
            </ul>
        </nav>
        
        <footer>
            <p>ФБИ-34, 3 курс, 2025</p>
        </footer>
    </div>
</body>
</html>"""

@app.route('/')
@app.route('/start')
def start():
    return '''
    <html>
    <body>
        <h1>Главная</h1>
        <a href="/lab3/">Лабораторная 3</a>
    </body>
    </html>
    '''