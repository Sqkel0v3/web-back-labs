from flask import Blueprint, url_for, redirect, request, render_template, abort
import datetime

lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/')
def lab2_index():
    return """
    <!doctype html>
    <html>
    <head>
        <title>Лабораторная 2</title>
    </head>
    <body>
        <h1>Вторая лабораторная работа</h1>
        <nav>
            <ul>
                <li><a href="/lab2/example">Пример шаблона</a></li>
                <li><a href="/lab2/books">Книги</a></li>
                <li><a href="/lab2/berries">Ягоды</a></li>
                <li><a href="/lab2/filters">Фильтры</a></li>
                <li><a href="/lab2/calc/5/3">Калькулятор (5 и 3)</a></li>
                <li><a href="/lab2/a">Без слеша</a></li>
                <li><a href="/lab2/a/">Со слешем</a></li>
                <li><a href="/lab2/all_flowers">Цветы</a></li>
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


@lab2.route('/lab2/a/')
def a():
    return 'со слешем'

@lab2.route('/lab2/a')
def a2():
    return 'без слеша'

flower_list = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 330},
    {'name': 'георгин', 'price': 300},
    {'name': 'гладиолус', 'price': 310}
]

@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        flower_list.pop(flower_id)
        return redirect(url_for('lab2.all_flowers'))

@lab2.route('/lab2/all_flowers')
def all_flowers():
    flowers_html = ""
    for i, flower in enumerate(flower_list):
        flowers_html += f"<li>{flower['name']} - {flower['price']} руб. <a href='/lab2/del_flower/{i}'>Удалить</a> | <a href='/lab2/flowers/{i}'>Подробнее</a></li>"
    
    return f"""
    <!doctype html>
    <html>
        <head>
            <title>Все цветы</title>
        </head>
        <body>
            <h1>Все цветы</h1>
            <ul>{flowers_html}</ul>
            <p><a href="/lab2/add_flower/новый_цветок">Добавить цветок "новый_цветок"</a></p>
            <p><a href="/lab2/clear_flowers">Очистить все цветы</a></p>
            <p><a href="/lab2/">Назад к списку лабораторных</a></p>
        </body>
    </html>
    """

@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append({'name': name, 'price': 300})
    return redirect(url_for('lab2.all_flowers'))

@lab2.route('/lab2/add_flower_manual')
def add_flower_manual():
    name = request.args.get('name', '').strip()
    if name:
        flower_list.append({'name': name, 'price': 300})
    return redirect(url_for('lab2.all_flowers'))

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        flower = flower_list[flower_id]
        return f'''
<!doctype html>
<html>
    <head>
        <title>Цветок {flower_id}</title>
    </head>
    <body>
        <h1>Цветок #{flower_id}</h1>
        <p>Название: {flower['name']}</p>
        <p>Цена: {flower['price']} руб</p>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a><br>
        <a href="/lab2/add_flower/новый_цветок">Добавить новый цветок</a><br>
        <a href="/lab2/">Назад к списку лабораторных</a>
    </body>
</html>
'''

@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('lab2.all_flowers'))

@lab2.route('/lab2/example/minimal')
def example_minimal():
    return render_template('lab2/example.html', lab_number=2)

@lab2.route('/lab2/example/empty')
def example_empty():
    fruits = []
    return render_template('lab2/example.html',
                         fruits=fruits,  
                         name='Тест',
                         lab_number=2,
                         group='ТЕСТ',
                         course=1)

@lab2.route('/lab2/example/<int:lab_number>')
@lab2.route('/lab2/example/<int:lab_number>/<name>')
@lab2.route('/lab2/example/<int:lab_number>/<name>/<group>/<course>')
def example_flexible(lab_number, name=None, group=None, course=None):
    if name is None:
        name = 'Фомченко Роман'
    if group is None:
        group = 'ФБИ-34'
    if course is None:
        course = 3
        
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80}
    ]
    
    return render_template('lab2/example.html',
                         name=name,
                         lab_number=lab_number,
                         group=group,
                         course=course,
                         fruits=fruits)

@lab2.route('/lab2/example')
def example():
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html',
                         name='Фомченко Роман',
                         lab_number=2,
                         group='ФБИ-34',
                         course=3,
                         fruits=fruits)

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)

@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('lab2.calc', a=1, b=1))

@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('lab2.calc', a=a, b=1))

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    operations = {
        'суммирование': a + b,
        'вычитание': a - b,
        'умножение': a * b,
        'деление': a / b if b != 0 else 'Ошибка: деление на ноль',
        'возведение в степень': a ** b
    }
    
    return render_template('lab2/calc.html', a=a, b=b, operations=operations)

books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказ', 'pages': 320},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
    {'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 120},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 640},
    {'author': 'Александр Грибоедов', 'title': 'Горе от ума', 'genre': 'Комедия', 'pages': 160},
    {'author': 'Николай Лесков', 'title': 'Левша', 'genre': 'Повесть', 'pages': 96}
]

@lab2.route('/lab2/books')
def books_list():
    return render_template('lab2/books.html', books=books)

berries = [
    {
        'name': 'Клубника', 
        'image': 'strawberry.jpg',
        'description': 'Сочная красная ягода с сладким вкусом, богатая витамином C и антиоксидантами.'
    },
    {
        'name': 'Малина', 
        'image': 'raspberry.jpg',
        'description': 'Нежная ароматная ягода, известная своими противовоспалительными свойствами.'
    },
    {
        'name': 'Черника', 
        'image': 'blueberry.jpg',
        'description': 'Маленькая синяя ягода, улучшающая зрение и память благодаря антоцианам.'
    },
    {
        'name': 'Ежевика', 
        'image': 'blackberry.jpg',
        'description': 'Тёмно-фиолетовая ягода с кисло-сладким вкусом, богатая клетчаткой.'
    },
    {
        'name': 'Смородина чёрная', 
        'image': 'black_currant.jpg',
        'description': 'Ароматная ягода с высоким содержанием витамина C, укрепляет иммунитет.'
    },
    {
        'name': 'Смородина красная', 
        'image': 'red_currant.jpg',
        'description': 'Прозрачная красная ягода с освежающим кислым вкусом.'
    },
    {
        'name': 'Крыжовник', 
        'image': 'gooseberry.jpg',
        'description': 'Зелёная или жёлтая ягода с характерными прожилками, богат пектином.'
    },
    {
        'name': 'Брусника', 
        'image': 'lingonberry.jpg',
        'description': 'Мелкая красная ягода с горьковатым вкусом, часто используется в медицине.'
    },
    {
        'name': 'Клюква', 
        'image': 'cranberry.jpg',
        'description': 'Кислая красная ягода, растущая на болотах, полезна для мочеполовой системы.'
    },
    {
        'name': 'Голубика', 
        'image': 'bilberry.jpg',
        'description': 'Крупная синяя ягода, похожая на чернику, но с более нежным вкусом.'
    },
    {
        'name': 'Облепиха', 
        'image': 'sea_buckthorn.jpg',
        'description': 'Оранжевые ягоды, богатые витаминами A, E и K, обладают лечебными свойствами.'
    },
    {
        'name': 'Шиповник', 
        'image': 'rose_hip.jpg',
        'description': 'Плоды розы, рекордсмен по содержанию витамина C, используются для чая.'
    },
    {
        'name': 'Боярышник', 
        'image': 'hawthorn.jpg',
        'description': 'Красные ягоды, полезные для сердечно-сосудистой системы.'
    },
    {
        'name': 'Рябина', 
        'image': 'rowan.jpg',
        'description': 'Ярко-красные горькие ягоды, становятся слаще после заморозков.'
    },
    {
        'name': 'Ирга', 
        'image': 'serviceberry.jpg',
        'description': 'Сине-чёрные сладкие ягоды, богатые каротином и витамином P.'
    },
    {
        'name': 'Жимолость', 
        'image': 'honeysuckle.jpg',
        'description': 'Вытянутые синие ягоды с уникальным вкусом, ранняя ягода сезона.'
    },
    {
        'name': 'Калина', 
        'image': 'viburnum.jpg',
        'description': 'Красные горькие ягоды, используемые в народной медицине от простуды.'
    },
    {
        'name': 'Бузина', 
        'image': 'elderberry.jpg',
        'description': 'Чёрные мелкие ягоды с терпким вкусом, используются для сиропов и варенья.'
    },
    {
        'name': 'Арония', 
        'image': 'chokeberry.jpg',
        'description': 'Чёрноплодная рябина с терпким вкусом, регулирует давление.'
    },
    {
        'name': 'Виноград', 
        'image': 'grape.jpg',
        'description': 'Сладкие ягоды разного цвета, используются для еды, вина и изюма.'
    },
    {
        'name': 'Вишня', 
        'image': 'cherry.jpg',
        'description': 'Кисло-сладкие красные ягоды с косточкой, богаты мелатонином.'
    },
    {
        'name': 'Черешня', 
        'image': 'sweet_cherry.jpg',
        'description': 'Сладкие крупные ягоды, более нежные и сочные чем вишня.'
    },
    {
        'name': 'Шелковица', 
        'image': 'mulberry.jpg',
        'description': 'Сладкие ягоды белого, красного или чёрного цвета, растут на деревьях.'
    },
    {
        'name': 'Земляника', 
        'image': 'wild_strawberry.jpg',
        'description': 'Лесная родственница клубники, мелкая но очень ароматная ягода.'
    }
]

@lab2.route('/lab2/berries')
def berries_list():
    return render_template('lab2/berries.html', berries=berries)

@lab2.route("/error/400")
def error_400():
    return """<!doctype html>
<html>
<head>
    <title>400 Bad Request</title>
</head>
<body>
    <h1>400 Bad Request</h1>
    <p>Сервер не может обработать запрос из-за неверного синтаксиса.</p>
    <a href="/lab2">Вернуться в lab2</a>
</body>
</html>""", 400

@lab2.route("/error/401")
def error_401():
    return """<!doctype html>
<html>
<head>
    <title>401 Unauthorized</title>
</head>
<body>
    <h1>401 Unauthorized</h1>
    <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
    <a href="/lab2">Вернуться в lab2</a>
</body>
</html>""", 401

@lab2.route("/error/402")
def error_402():
    return """<!doctype html>
<html>
<head>
    <title>402 Payment Required</title>
</head>
<body>
    <h1>402 Payment Required</h1>
    <p>Для доступа к ресурсу требуется оплата.</p>
    <a href="/lab2">Вернуться в lab2</a>
</body>
</html>""", 402

@lab2.route("/error/403")
def error_403():
    return """<!doctype html>
<html>
<head>
    <title>403 Forbidden</title>
</head>
<body>
    <h1>403 Forbidden</h1>
    <p>Доступ к запрашиваемому ресурсу запрещен.</p>
    <a href="/lab2">Вернуться в lab2</a>
</body>
</html>""", 403

@lab2.route("/error/405")
def error_405():
    return """<!doctype html>
<html>
<head>
    <title>405 Method Not Allowed</title>
</head>
<body>
    <h1>405 Method Not Allowed</h1>
    <p>Использованный метод HTTP не поддерживается для данного ресурса.</p>
    <a href="/lab2">Вернуться в lab2</a>
</body>
</html>""", 405

@lab2.route("/error/418")
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
    <a href="/lab2">Вернуться в lab2</a>
</body>
</html>""", 418