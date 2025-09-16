from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route("/")
@app.route("/web")
def web():
    return """<!doctype html>
        <html>
           <body>
           <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
               <br>
               <a href="/counter">счетчик</a>
               <br>
               <a href="/lab1/image">изображение с CSS</a>
            </body>
        </html>"""

@app.route("/author")
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

@app.route('/counter')
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
        <a href="/clear_counter"> Очистить счетчик</a><br>
        <a href="/web"> На главную</a>
   </body>
</html>
'''

@app.route('/clear_counter')
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
        <a href="/counter"> Перейти к счетчику</a><br>
        <a href="/web"> На главную</a>
   </body>
</html>
'''

@app.route("/info")
def info():
    return redirect("/author")

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
