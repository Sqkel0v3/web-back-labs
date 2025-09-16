from flask import Flask, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
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
    path = url_for("static", filename ="oak.jpg")
    return """<!doctype html>
        <html>
            <body>
                <h1>Дуб</h1>
                <img src=\"""" + path + """\" alt="Дуб" style="max-width: 600px; border: 2px solid black;">
            </body>
        </html>"""

count = 0

@app.route('/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
    </body>
</html>
'''

