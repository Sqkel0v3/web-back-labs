from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

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
    <title>Первая лабораторная</title>
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
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link">← На главную</a>
        
        <header>
            <h1>Первая лабораторная работа</h1>
            <p>Файлы первой лабораторной</p>
        </header>
        
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
    </div>
</body>
</html>"""

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
    return """<!doctype html>
        <html>
            <body>
                <h1>Дуб</h1>
                <img src=\"""" + path + """\" class="oak-image">
                <br>
                <a href="/" class="back-link">На главную</a>
            </body>
        </html>"""

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
