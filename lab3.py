from flask import Blueprint, render_template, request, make_response, redirect
import random
from datetime import datetime

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    
    if name is None:
        name = "Аноним"
    
    if age is None:
        age = "не указан"
    
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    
    if color or bg_color or font_size:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        return resp
    
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    
    resp = make_response(render_template('lab3/settings.html', color=color or '#000000',bg_color=bg_color or '#ffffff', font_size=font_size or '16'))
    return resp

@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    return render_template('lab3/ticket.html', fio=fio, shelf=shelf, linen=linen, luggage=luggage, age=age, departure=departure, destination=destination, date=date, insurance=insurance, errors=errors)

@lab3.route('/lab3/ticket_result')
def ticket_result():
    errors = {}
    
    fio = request.args.get('fio', '').strip()
    shelf = request.args.get('shelf', '').strip()
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age_str = request.args.get('age', '').strip()
    departure = request.args.get('departure', '').strip()
    destination = request.args.get('destination', '').strip()
    date = request.args.get('date', '').strip()
    insurance = request.args.get('insurance')

    if not fio:
        errors['fio'] = 'Заполните ФИО пассажира'
    
    if not shelf:
        errors['shelf'] = 'Выберите полку'
    
    if not age_str:
        errors['age'] = 'Заполните возраст'
    else:
        try:
            age = int(age_str)
            if age < 1 or age > 120:
                errors['age'] = 'Возраст должен быть от 1 до 120 лет'
        except ValueError:
            errors['age'] = 'Возраст должен быть числом'
    
    if not departure:
        errors['departure'] = 'Заполните пункт выезда'
    
    if not destination:
        errors['destination'] = 'Заполните пункт назначения'
    
    if not date:
        errors['date'] = 'Выберите дату поездки'

    if errors:
        return render_template('lab3/ticket.html',
                             fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                             age=age_str, departure=departure, destination=destination,
                             date=date, insurance=insurance, errors=errors)
    
    age = int(age_str)

    if age < 18:
        base_price = 700  
        ticket_type = "Детский билет"
    else:
        base_price = 1000  
        ticket_type = "Взрослый билет"

    additional_cost = 0
    
    if shelf in ['lower', 'side_lower']:
        additional_cost += 100
    
    if linen == 'on':
        additional_cost += 75

    if luggage == 'on':
        additional_cost += 250

    if insurance == 'on':
        additional_cost += 150
    
    total_price = base_price + additional_cost

    shelf_names = {
        'lower': 'Нижняя',
        'upper': 'Верхняя',
        'side_upper': 'Верхняя боковая',
        'side_lower': 'Нижняя боковая'
    }

    ticket_number = f"{random.randint(100000, 999999)}"
    
    return render_template('lab3/ticket_result.html',
                         fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                         age=age, departure=departure, destination=destination,
                         date=date, insurance=insurance, ticket_type=ticket_type,
                         shelf_name=shelf_names[shelf], total_price=total_price,
                         ticket_number=ticket_number)

@lab3.route('/lab3/clear_settings')
def clear_settings():
    """Очистка всех кук настроек"""
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    return resp

phones = [
    {'id': 1, 'name': 'iPhone 15 Pro', 'brand': 'Apple', 'price': 99990, 'color': 'Титановый', 'storage': '256GB'},
    {'id': 2, 'name': 'Samsung Galaxy S24', 'brand': 'Samsung', 'price': 79990, 'color': 'Черный', 'storage': '256GB'},
    {'id': 3, 'name': 'Xiaomi 14', 'brand': 'Xiaomi', 'price': 59990, 'color': 'Белый', 'storage': '256GB'},
    {'id': 4, 'name': 'Google Pixel 8 Pro', 'brand': 'Google', 'price': 89990, 'color': 'Бирюзовый', 'storage': '128GB'},
    {'id': 5, 'name': 'OnePlus 12', 'brand': 'OnePlus', 'price': 64990, 'color': 'Зеленый', 'storage': '256GB'},
    {'id': 6, 'name': 'iPhone 14', 'brand': 'Apple', 'price': 69990, 'color': 'Синий', 'storage': '128GB'},
    {'id': 7, 'name': 'Samsung Galaxy A54', 'brand': 'Samsung', 'price': 34990, 'color': 'Фиолетовый', 'storage': '128GB'},
    {'id': 8, 'name': 'Xiaomi Redmi Note 13', 'brand': 'Xiaomi', 'price': 24990, 'color': 'Черный', 'storage': '128GB'},
    {'id': 9, 'name': 'Realme 11 Pro+', 'brand': 'Realme', 'price': 32990, 'color': 'Золотой', 'storage': '256GB'},
    {'id': 10, 'name': 'iPhone 13 mini', 'brand': 'Apple', 'price': 54990, 'color': 'Розовый', 'storage': '128GB'},
    {'id': 11, 'name': 'Samsung Galaxy Z Flip5', 'brand': 'Samsung', 'price': 119990, 'color': 'Сиреневый', 'storage': '256GB'},
    {'id': 12, 'name': 'Google Pixel 7a', 'brand': 'Google', 'price': 44990, 'color': 'Коралловый', 'storage': '128GB'},
    {'id': 13, 'name': 'Nothing Phone (2)', 'brand': 'Nothing', 'price': 52990, 'color': 'Белый', 'storage': '256GB'},
    {'id': 14, 'name': 'Honor 90', 'brand': 'Honor', 'price': 37990, 'color': 'Изумрудный', 'storage': '256GB'},
    {'id': 15, 'name': 'Motorola Edge 40', 'brand': 'Motorola', 'price': 41990, 'color': 'Черный', 'storage': '256GB'},
    {'id': 16, 'name': 'iPhone 15 Plus', 'brand': 'Apple', 'price': 89990, 'color': 'Желтый', 'storage': '256GB'},
    {'id': 17, 'name': 'Samsung Galaxy S23 FE', 'brand': 'Samsung', 'price': 54990, 'color': 'Кремовый', 'storage': '128GB'},
    {'id': 18, 'name': 'Xiaomi Poco X6 Pro', 'brand': 'Xiaomi', 'price': 32990, 'color': 'Серый', 'storage': '256GB'},
    {'id': 19, 'name': 'Asus Zenfone 10', 'brand': 'Asus', 'price': 59990, 'color': 'Красный', 'storage': '256GB'},
    {'id': 20, 'name': 'Sony Xperia 5 V', 'brand': 'Sony', 'price': 84990, 'color': 'Синий', 'storage': '128GB'},
    {'id': 21, 'name': 'iPhone SE (2022)', 'brand': 'Apple', 'price': 42990, 'color': 'Белый', 'storage': '64GB'},
    {'id': 22, 'name': 'Samsung Galaxy A14', 'brand': 'Samsung', 'price': 14990, 'color': 'Серебристый', 'storage': '64GB'},
    {'id': 23, 'name': 'Xiaomi Redmi 12', 'brand': 'Xiaomi', 'price': 15990, 'color': 'Голубой', 'storage': '128GB'},
    {'id': 24, 'name': 'Nokia G42', 'brand': 'Nokia', 'price': 19990, 'color': 'Фиолетовый', 'storage': '128GB'}
]

@lab3.route('/lab3/search')
def search():
    min_price_cookie = request.cookies.get('min_price', '')
    max_price_cookie = request.cookies.get('max_price', '')

    min_price_form = request.args.get('min_price', '').strip()
    max_price_form = request.args.get('max_price', '').strip()

    if request.args.get('reset'):
        min_price = ''
        max_price = ''
        filtered_phones = phones
    else:
        min_price = min_price_form if min_price_form != '' else min_price_cookie
        max_price = max_price_form if max_price_form != '' else max_price_cookie

        filtered_phones = filter_phones(phones, min_price, max_price)

    total_count = len(phones)
    filtered_count = len(filtered_phones)

    all_prices = [phone['price'] for phone in phones]
    min_all_price = min(all_prices)
    max_all_price = max(all_prices)

    resp = make_response(render_template('lab3/search.html',
                                       phones=filtered_phones,
                                       min_price=min_price,
                                       max_price=max_price,
                                       total_count=total_count,
                                       filtered_count=filtered_count,
                                       min_all_price=min_all_price,
                                       max_all_price=max_all_price))
    
    if not request.args.get('reset'):
        if min_price:
            resp.set_cookie('min_price', min_price)
        if max_price:
            resp.set_cookie('max_price', max_price)
    else:
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
    
    return resp

def filter_phones(phones_list, min_price_str, max_price_str):
    """Фильтрация телефонов по цене"""
    filtered = phones_list.copy()
    
    try:
        if min_price_str:
            min_price = int(min_price_str)
            filtered = [phone for phone in filtered if phone['price'] >= min_price]

        if max_price_str:
            max_price = int(max_price_str)
            filtered = [phone for phone in filtered if phone['price'] <= max_price]
            
    except ValueError:
        return phones_list
    
    return filtered