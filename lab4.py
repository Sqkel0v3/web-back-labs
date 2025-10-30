from flask import Blueprint, render_template, request, redirect, session

lab4 = Blueprint('lab4', __name__)

users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Петров', 'gender': 'м'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Смит', 'gender': 'м'},
    {'login': 'admin', 'password': 'admin', 'name': 'Администратор', 'gender': 'м'},
    {'login': 'user', 'password': 'pass', 'name': 'Пользователь', 'gender': 'м'},
    {'login': 'anna', 'password': 'anna', 'name': 'Анна Иванова', 'gender': 'ж'}
]

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '':
        x1 = 0
    else:
        x1 = int(x1)
    
    if x2 == '':
        x2 = 0
    else:
        x2 = int(x2)
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('lab4/mult-form.html')

@lab4.route('/lab4/mult', methods=['POST'])
def mult():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '':
        x1 = 1
    else:
        x1 = int(x1)
    
    if x2 == '':
        x2 = 1
    else:
        x2 = int(x2)
    
    result = x1 * x2
    return render_template('lab4/mult.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)

    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Оба числа не могут быть равны нулю!')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')
    
    if operation == 'cut':
        tree_count -= 1
    elif operation == 'plant':
        tree_count += 1

    if tree_count < 0:
        tree_count = 0
    
    return redirect('/lab4/tree')

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            user_name = ''
            for user in users:
                if user['login'] == session['login']:
                    user_name = user['name']
                    break
            return render_template('lab4/login.html', authorized=authorized, name=user_name)
        else:
            return render_template('lab4/login.html', authorized=False)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login_value=login)
    
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login_value=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login_value=login)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge')
def fridge_form():
    return render_template('lab4/fridge.html')

@lab4.route('/lab4/fridge', methods=['POST'])
def fridge():
    temperature = request.form.get('temperature')

    if not temperature:
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    try:
        temp = int(temperature)
    except ValueError:
        return render_template('lab4/fridge.html', error='Ошибка: введите целое число')

    if temp < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    elif temp > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    elif -12 <= temp <= -9:
        snowflakes = '***'
        message = f'Установлена температура: {temp}°C'
        return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)
    elif -8 <= temp <= -5:
        snowflakes = '**'
        message = f'Установлена температура: {temp}°C'
        return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)
    elif -4 <= temp <= -1:
        snowflakes = '*'
        message = f'Установлена температура: {temp}°C'
        return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)
    
    return render_template('lab4/fridge.html')

@lab4.route('/lab4/grain')
def grain_form():
    return render_template('lab4/grain.html')

@lab4.route('/lab4/grain', methods=['POST'])
def grain():
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')

    prices = {
        'barley': 12000,
        'oats': 8500,
        'wheat': 9000,
        'rye': 15000
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }

    if not weight:
        return render_template('lab4/grain.html', error='Ошибка: не указан вес')
    
    try:
        weight_float = float(weight)
    except ValueError:
        return render_template('lab4/grain.html', error='Ошибка: введите корректное число для веса')

    if weight_float <= 0:
        return render_template('lab4/grain.html', error='Ошибка: вес должен быть больше 0')

    if weight_float > 100:
        return render_template('lab4/grain.html', error='Извините, такого объёма сейчас нет в наличии')

    price_per_ton = prices.get(grain_type)
    grain_name = grain_names.get(grain_type)
    
    total_cost = weight_float * price_per_ton

    discount = 0
    if weight_float > 10:
        discount = total_cost * 0.10
        total_cost -= discount
    
    message = f'Заказ успешно сформирован. Вы заказали {grain_name}. Вес: {weight_float} т. Сумма к оплате: {total_cost:,.0f} руб'
    
    if discount > 0:
        discount_message = f'Применена скидка 10% за большой объём. Размер скидки: {discount:,.0f} руб'
        return render_template('lab4/grain.html', message=message, discount_message=discount_message)
    
    return render_template('lab4/grain.html', message=message)

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    name = request.form.get('name')
    gender = request.form.get('gender')

    if not login or not password or not name:
        return render_template('lab4/register.html', error='Все поля обязательны для заполнения')
    
    if password != password_confirm:
        return render_template('lab4/register.html', error='Пароли не совпадают', login=login, name=name)

    for user in users:
        if user['login'] == login:
            return render_template('lab4/register.html', error='Пользователь с таким логином уже существует')

    new_user = {
        'login': login,
        'password': password,
        'name': name,
        'gender': gender
    }
    users.append(new_user)
    
    return render_template('lab4/register.html', success='Регистрация успешна! Теперь вы можете войти.')

@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user_login = session['login']
    return render_template('lab4/users.html', users=users, current_user=current_user_login)

@lab4.route('/lab4/delete_user', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    user_login = session['login']

    global users
    users = [user for user in users if user['login'] != user_login]

    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/edit_user', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    user_login = session['login']
    current_user = None

    for user in users:
        if user['login'] == user_login:
            current_user = user
            break
    
    if request.method == 'GET':
        return render_template('lab4/edit_user.html', user=current_user)

    new_login = request.form.get('login')
    new_name = request.form.get('name')
    new_password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    gender = request.form.get('gender')

    if not new_login or not new_name:
        return render_template('lab4/edit_user.html', user=current_user, error='Логин и имя обязательны')

    for user in users:
        if user['login'] == new_login and user['login'] != user_login:
            return render_template('lab4/edit_user.html', user=current_user, error='Пользователь с таким логином уже существует')

    current_user['login'] = new_login
    current_user['name'] = new_name
    current_user['gender'] = gender

    if new_password:
        if new_password != password_confirm:
            return render_template('lab4/edit_user.html', user=current_user, error='Пароли не совпадают')
        current_user['password'] = new_password

    if new_login != user_login:
        session['login'] = new_login
    
    return render_template('lab4/edit_user.html', user=current_user, success='Данные успешно обновлены')
