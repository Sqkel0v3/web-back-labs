from flask import Flask, url_for, request, redirect, session
import datetime
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

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
    <title>HTTP, ФБ, Лабораторные работы</title>
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
            </ul>
        </nav>
        
        <footer>
            <p>ФБИ-34, 3 курс, 2025</p>
        </footer>
    </div>

</body>
</html>"""

@app.route("/lab1")
def lab1():
    return """<!doctype html>
<html>
<head>
    <title>Лабораторная 1</title>
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
        .back-link {
            display: inline-block;
            margin-bottom: 20px;
            padding: 10px 15px;
            background: #95a5a6;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .back-link:hover {
            background: #7f8c8d;
        }
        .content {
            margin: 20px 0;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 8px;
            line-height: 1.8;
            font-size: 16px;
        }
        .home-link {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 24px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            transition: background 0.3s ease;
        }
        .home-link:hover {
            background: #2980b9;
        }
        .routes-section {
            background: #e8f4f8;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #2c3e50;
        }
        .routes-list {
            list-style-type: none;
            padding: 0;
        }
        .routes-list li {
            margin: 8px 0;
        }
        .routes-list a {
            color: #2c3e50;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        .routes-list a:hover {
            background-color: #3498db;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link">← На главную</a>
        
        <header>
            <h1>Первая лабораторная работа</h1>
            <p>Изучение основ Flask</p>
        </header>
        
        <div class="content">
            <p>Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые ба-
            зовые возможности.</p>
        </div>
        
        <nav>
            <ul>
                <li><a href="/lab1/web">WEB</a></li>
                <li><a href="/lab1/author">АВТОР</a></li>
                <li><a href="/lab1/image">КАРТИНКА</a></li>
                <li><a href="/lab1/counter">счетчик</a></li>
                <li><a href="/lab1/info">инфо</a></li>
                <li><a href="/lab1/clear_counter">отчистка счетчика</a></li>
            </ul>
        </nav>
        
        <div class="routes-section">
            <h2>Список роутов</h2>
            <ul class="routes-list">
                <li><a href="/">/ (главная страница)</a></li>
                <li><a href="/index">/index (главная страница)</a></li>
                <li><a href="/lab1">/lab1 (первая лабораторная)</a></li>
                <li><a href="/lab1/web">/lab1/web (web-страница)</a></li>
                <li><a href="/lab1/author">/lab1/author (автор)</a></li>
                <li><a href="/lab1/image">/lab1/image (картинка)</a></li>
                <li><a href="/lab1/counter">/lab1/counter (счетчик)</a></li>
                <li><a href="/lab1/info">/lab1/info (информация)</a></li>
                <li><a href="/lab1/clear_counter">/lab1/clear_counter (очистка счетчика)</a></li>
                <li><a href="/error/400">/error/400 (ошибка 400)</a></li>
                <li><a href="/error/401">/error/401 (ошибка 401)</a></li>
                <li><a href="/error/402">/error/402 (ошибка 402)</a></li>
                <li><a href="/error/403">/error/403 (ошибка 403)</a></li>
                <li><a href="/error/405">/error/405 (ошибка 405)</a></li>
                <li><a href="/error/418">/error/418 (ошибка 418)</a></li>
                <li><a href="/error/500">/error/500 (ошибка 500)</a></li>
            </ul>
        </div>
        
        <a href="/" class="home-link">На главную страницу</a>
    </div>
</body>
</html>"""

@app.route("/error/400")
def error_400():
    return """<!doctype html>
<html>
<head>
    <title>400 Bad Request</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 {
            color: #e74c3c;
            font-size: 3em;
            margin-bottom: 10px;
        }
        .error-code {
            font-size: 6em;
            font-weight: bold;
            color: #e74c3c;
            margin: 0;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <p class="error-code">400</p>
        <h1>Bad Request</h1>
        <p>Сервер не может обработать запрос из-за неверного синтаксиса.</p>
        <a href="/" class="back-link">Вернуться на главную</a>
    </div>
</body>
</html>""", 400

@app.route("/error/401")
def error_401():
    return """<!doctype html>
<html>
<head>
    <title>401 Unauthorized</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 {
            color: #e67e22;
            font-size: 3em;
            margin-bottom: 10px;
        }
        .error-code {
            font-size: 6em;
            font-weight: bold;
            color: #e67e22;
            margin: 0;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <p class="error-code">401</p>
        <h1>Unauthorized</h1>
        <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
        <a href="/" class="back-link">Вернуться на главную</a>
    </div>
</body>
</html>""", 401

@app.route("/error/402")
def error_402():
    return """<!doctype html>
<html>
<head>
    <title>402 Payment Required</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 {
            color: #f39c12;
            font-size: 3em;
            margin-bottom: 10px;
        }
        .error-code {
            font-size: 6em;
            font-weight: bold;
            color: #f39c12;
            margin: 0;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <p class="error-code">402</p>
        <h1>Payment Required</h1>
        <p>Для доступа к ресурсу требуется оплата.</p>
        <a href="/" class="back-link">Вернуться на главную</a>
    </div>
</body>
</html>""", 402

@app.route("/error/403")
def error_403():
    return """<!doctype html>
<html>
<head>
    <title>403 Forbidden</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 {
            color: #d35400;
            font-size: 3em;
            margin-bottom: 10px;
        }
        .error-code {
            font-size: 6em;
            font-weight: bold;
            color: #d35400;
            margin: 0;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <p class="error-code">403</p>
        <h1>Forbidden</h1>
        <p>Доступ к запрашиваемому ресурсу запрещен.</p>
        <a href="/" class="back-link">Вернуться на главную</a>
    </div>
</body>
</html>""", 403

@app.route("/error/405")
def error_405():
    return """<!doctype html>
<html>
<head>
    <title>405 Method Not Allowed</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 {
            color: #c0392b;
            font-size: 3em;
            margin-bottom: 10px;
        }
        .error-code {
            font-size: 6em;
            font-weight: bold;
            color: #c0392b;
            margin: 0;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <p class="error-code">405</p>
        <h1>Method Not Allowed</h1>
        <p>Использованный метод HTTP не поддерживается для данного ресурса.</p>
        <a href="/" class="back-link">Вернуться на главную</a>
    </div>
</body>
</html>""", 405

@app.route("/error/418")
def error_418():
    return """<!doctype html>
<html>
<head>
    <title>418 I'm a teapot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 {
            color: #8e44ad;
            font-size: 3em;
            margin-bottom: 10px;
        }
        .error-code {
            font-size: 6em;
            font-weight: bold;
            color: #8e44ad;
            margin: 0;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .teapot {
            font-size: 4em;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <p class="error-code">418</p>
        <h1>I'm a teapot</h1>
        <div class="teapot">🫖</div>
        <p>Я - чайник! Сервер отказывается варить кофе в чайнике.</p>
        <p><em>(Это шуточный код ошибки из RFC 2324)</em></p>
        <a href="/" class="back-link">Вернуться на главную</a>
    </div>
</body>
</html>""", 418

@app.route("/")
@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
           <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
               <br>
               <a href="/lab1/counter">счетчик</a>
               <br>
               <a href="/lab1/image">изображение с CSS</a>
            </body>
        </html>"""

@app.route("/lab1/author")
def author():
    name = "Фомченко Роман Дмитриевич"
    group = "ФБИ-34"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route('/lab1/image')
def image():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    
    response = """
    <!doctype html>
        <html>
            <body>
                <h1>Дуб</h1>
                <img src=\"""" + path + """\" class="oak-image">
                <br>
                <a href="/" class="back-link">На главную</a>
            </body>
        </html>"""
    
    from flask import make_response
    resp = make_response(response)
    
    resp.headers['Content-Language'] = 'ru'
    
    resp.headers['X-Custom-Header-1'] = 'My-Custom-Value-1'
    resp.headers['X-Application-Name'] = 'Flask-Lab-Work'
    
    return resp

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        <h2>Счетчик посещений</h2>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + time + ''' <br>
        Запрошенный адрес: ''' + url + ''' <br>
        Ваш IP-адрес: ''' + client_ip + ''' <br>
        <br>
        <a href="/lab1/clear_counter"> Очистить счетчик</a><br>
        <a href="/lab1/web"> На главную</a>
   </body>
</html>
'''

@app.route('/lab1/clear_counter')
def clear_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        <h2>Счетчик очищен!</h2>
        <p>Счетчик посещений был сброшен в ноль.</p>
        <br>
        <a href="/lab1/counter"> Перейти к счетчику</a><br>
        <a href="/lab1/web"> На главную</a>
   </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201
