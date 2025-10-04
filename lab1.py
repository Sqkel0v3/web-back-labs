from flask import Blueprint, url_for, redirect, request
import datetime

lab1 = Blueprint('lab1', __name__)

count = 0

@lab1.route("/lab1/")
def lab():
    return """<!doctype html>
<html>
<head>
    <title>Лабораторная 1</title>
</head>
<body>
    <h1>Первая лабораторная работа</h1>
    <p>Flask — фреймворк для создания веб-приложений на Python</p>
    
    <h2>Основные роуты:</h2>
    <ul>
        <li><a href="/lab1/web">WEB</a></li>
        <li><a href="/lab1/author">АВТОР</a></li>
        <li><a href="/lab1/image">КАРТИНКА</a></li>
        <li><a href="/lab1/counter">счетчик</a></li>
        <li><a href="/lab1/info">инфо</a></li>
        <li><a href="/lab1/clear_counter">очистка счетчика</a></li>
    </ul>
    
    <h2>Тестирование ошибок:</h2>
    <ul>
        <li><a href="/error/400">400 Bad Request</a></li>
        <li><a href="/error/401">401 Unauthorized</a></li>
        <li><a href="/error/402">402 Payment Required</a></li>
        <li><a href="/error/403">403 Forbidden</a></li>
        <li><a href="/error/405">405 Method Not Allowed</a></li>
        <li><a href="/error/418">418 I'm a Teapot</a></li>
    </ul>
    
    <p><a href="/">На главную</a></p>
</body>
</html>"""

@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
<html>
   <body>
   <h1>web-сервер на flask</h1>
       <a href="/lab1/author">author</a>
       <br>
       <a href="/lab1/counter">счетчик</a>
       <br>
       <a href="/lab1/image">изображение</a>
       <br>
       <a href="/lab1">Назад</a>
    </body>
</html>"""

@lab1.route("/lab1/author")
def author():
    name = "Фомченко Роман Дмитриевич"
    group = "ФБИ-34"
    faculty = "ФБ"

    return f"""<!doctype html>
<html>
    <body>
        <p>Студент: {name}</p>
        <p>Группа: {group}</p>
        <p>Факультет: {faculty}</p>
        <a href="/lab1/web">web</a>
        <br>
        <a href="/lab1">Назад</a>
    </body>
</html>"""

@lab1.route('/lab1/image')
def image():
    path = url_for("static", filename="oak.jpg")
    
    return f"""<!doctype html>
<html>
    <body>
        <h1>Дуб</h1>
        <img src="{path}" width="300">
        <br>
        <a href="/lab1">Назад</a>
    </body>
</html>"""

count = 0

@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr

    return f'''
<!doctype html>
<html>
    <body>
        <h2>Счетчик посещений</h2>
        Сколько раз вы сюда заходили: {count}
        <hr>
        Дата и время: {time} <br>
        Запрошенный адрес: {url} <br>
        Ваш IP-адрес: {client_ip} <br>
        <br>
        <a href="/lab1/clear_counter"> Очистить счетчик</a><br>
        <a href="/lab1"> Назад</a>
   </body>
</html>
'''

@lab1.route('/lab1/clear_counter')
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
        <a href="/lab1"> Назад</a>
   </body>
</html>
'''

@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
        <br>
        <a href="/lab1">Назад</a>
    </body>
</html>
''', 201

@lab1.route("/error/400")
def error_400():
    return """<!doctype html>
<html>
<head>
    <title>400 Bad Request</title>
</head>
<body>
    <h1>400 Bad Request</h1>
    <p>Сервер не может обработать запрос из-за неверного синтаксиса.</p>
    <a href="/lab1">Вернуться в lab1</a>
</body>
</html>""", 400

@lab1.route("/error/401")
def error_401():
    return """<!doctype html>
<html>
<head>
    <title>401 Unauthorized</title>
</head>
<body>
    <h1>401 Unauthorized</h1>
    <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
    <a href="/lab1">Вернуться в lab1</a>
</body>
</html>""", 401

@lab1.route("/error/402")
def error_402():
    return """<!doctype html>
<html>
<head>
    <title>402 Payment Required</title>
</head>
<body>
    <h1>402 Payment Required</h1>
    <p>Для доступа к ресурсу требуется оплата.</p>
    <a href="/lab1">Вернуться в lab1</a>
</body>
</html>""", 402

@lab1.route("/error/403")
def error_403():
    return """<!doctype html>
<html>
<head>
    <title>403 Forbidden</title>
</head>
<body>
    <h1>403 Forbidden</h1>
    <p>Доступ к запрашиваемому ресурсу запрещен.</p>
    <a href="/lab1">Вернуться в lab1</a>
</body>
</html>""", 403

@lab1.route("/error/405")
def error_405():
    return """<!doctype html>
<html>
<head>
    <title>405 Method Not Allowed</title>
</head>
<body>
    <h1>405 Method Not Allowed</h1>
    <p>Использованный метод HTTP не поддерживается для данного ресурса.</p>
    <a href="/lab1">Вернуться в lab1</a>
</body>
</html>""", 405

@lab1.route("/error/418")
def error_418():
    return """<!doctype html>
<html>
<head>
    <title>418 I'm a teapot</title>
</head>
<body>
    <h1>418 I'm a teapot</h1>
    <p>🫖 Я - чайник! Сервер отказывается варить кофе в чайнике.</p>
    <p><em>(Это шуточный код ошибки из RFC 2324)</em></p>
    <a href="/lab1">Вернуться в lab1</a>
</body>
</html>""", 418

