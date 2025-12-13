from flask import Blueprint, render_template, request, jsonify, session
import json

lab9 = Blueprint('lab9', __name__, url_prefix='/lab9')

box_positions = [
    {'id': 1, 'top': '10%', 'left': '5%'},
    {'id': 2, 'top': '25%', 'left': '20%'},
    {'id': 3, 'top': '15%', 'left': '40%'},
    {'id': 4, 'top': '30%', 'left': '60%'},
    {'id': 5, 'top': '5%', 'left': '75%'},
    {'id': 6, 'top': '50%', 'left': '10%'},
    {'id': 7, 'top': '45%', 'left': '35%'},
    {'id': 8, 'top': '60%', 'left': '55%'},
    {'id': 9, 'top': '40%', 'left': '80%'},
    {'id': 10, 'top': '75%', 'left': '25%'}
]

boxes_state = {
    'opened_boxes': set(),
    'available_boxes': list(range(1, 11))
}

congratulations = [
    {"id": 1, "message": "С Новым годом! Пусть этот год принесет много счастья и удачи!", "gift": "🎁", "requires_auth": False},
    {"id": 2, "message": "Желаем здоровья, любви и процветания в новом году!", "gift": "🎄", "requires_auth": False},
    {"id": 3, "message": "Пусть все мечты сбудутся, а планы осуществятся!", "gift": "⭐", "requires_auth": False},
    {"id": 4, "message": "Счастья, улыбок и тепла в вашем доме!", "gift": "❤️", "requires_auth": False},
    {"id": 5, "message": "Успехов в работе и творческого вдохновения!", "gift": "✨", "requires_auth": False},
    {"id": 6, "message": "Мира, добра и благополучия вашей семье!", "gift": "🏠", "requires_auth": True},
    {"id": 7, "message": "Пусть каждый день будет наполнен радостью!", "gift": "😊", "requires_auth": True},
    {"id": 8, "message": "Исполнения самых заветных желаний!", "gift": "🌠", "requires_auth": True},
    {"id": 9, "message": "Финансового благополучия и стабильности!", "gift": "💰", "requires_auth": True},
    {"id": 10, "message": "Крепкого здоровья и бодрости духа!", "gift": "💪", "requires_auth": True}
]

USERS = {
    'user': '123',
    'admin': 'admin',
    'student': 'password'
}

GUEST_LIMIT = 3
AUTH_LIMIT = 5

@lab9.route('/')
def index():
    if 'opened_count' not in session:
        session['opened_count'] = 0
    if 'user_opened_boxes' not in session:
        session['user_opened_boxes'] = []
    if 'is_authenticated' not in session:
        session['is_authenticated'] = False
    if 'username' not in session:
        session['username'] = None
    
    user_limit = AUTH_LIMIT if session['is_authenticated'] else GUEST_LIMIT
    
    return render_template('lab9/index.html',
                         box_positions=box_positions,
                         total_boxes=len(boxes_state['available_boxes']),
                         opened_count=session['opened_count'],
                         is_authenticated=session['is_authenticated'],
                         username=session['username'],
                         user_limit=user_limit)

@lab9.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Введите логин и пароль'
            })
        
        if username in USERS and USERS[username] == password:
            session['is_authenticated'] = True
            session['username'] = username
            return jsonify({
                'success': True,
                'message': f'Добро пожаловать, {username}! Теперь вы можете открыть до {AUTH_LIMIT} коробок.',
                'username': username
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Неверное имя пользователя или пароль'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка сервера: {str(e)}'
        })

@lab9.route('/logout', methods=['POST'])
def logout():
    session['is_authenticated'] = False
    session['username'] = None
    return jsonify({
        'success': True,
        'message': 'Вы вышли из системы'
    })

@lab9.route('/api/open_box', methods=['POST'])
def open_box():
    try:
        data = request.get_json()
        box_id = int(data.get('box_id', 0))
        
        if box_id < 1 or box_id > 10:
            return jsonify({'success': False, 'message': 'Коробка не найдена'})
        
        if box_id in boxes_state['opened_boxes']:
            return jsonify({'success': False, 'message': 'Эта коробка уже открыта'})
        
        is_auth = session.get('is_authenticated', False)
        current_opened = session.get('opened_count', 0)
        
        if is_auth:
            if current_opened >= AUTH_LIMIT:
                return jsonify({
                    'success': False,
                    'message': f'Вы уже открыли максимальное количество коробок ({AUTH_LIMIT})'
                })
        else:
            if current_opened >= GUEST_LIMIT:
                return jsonify({
                    'success': False,
                    'message': f'Гости могут открыть только {GUEST_LIMIT} коробки. Войдите в систему, чтобы открывать до {AUTH_LIMIT} коробок!'
                })
        
        congrat = next((c for c in congratulations if c['id'] == box_id), None)
        if not congrat:
            return jsonify({'success': False, 'message': 'Поздравление не найдено'})
        
        if congrat['requires_auth'] and not is_auth:
            return jsonify({
                'success': False,
                'message': 'Коробки 6-10 доступны только авторизованным пользователям. Войдите в систему!',
                'requires_auth': True
            })
        
        boxes_state['opened_boxes'].add(box_id)
        boxes_state['available_boxes'] = [b for b in boxes_state['available_boxes'] if b != box_id]
        
        session['opened_count'] = current_opened + 1
        user_opened = session.get('user_opened_boxes', [])
        user_opened.append(box_id)
        session['user_opened_boxes'] = user_opened
        
        remaining_limit = (AUTH_LIMIT if is_auth else GUEST_LIMIT) - session['opened_count']
        
        return jsonify({
            'success': True,
            'message': congrat['message'],
            'gift': congrat['gift'],
            'opened_count': session['opened_count'],
            'remaining_boxes': len(boxes_state['available_boxes']),
            'requires_auth': congrat['requires_auth'],
            'remaining_limit': remaining_limit,
            'is_authenticated': is_auth
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка при открытии коробки: {str(e)}'
        })

@lab9.route('/api/santa', methods=['POST'])
def santa_refill():
    if not session.get('is_authenticated', False):
        return jsonify({
            'success': False,
            'message': 'Только авторизованные пользователи могут вызывать Деда Мороза!'
        })
    
    boxes_state['opened_boxes'] = set()
    boxes_state['available_boxes'] = list(range(1, 11))
    
    session['opened_count'] = 0
    session['user_opened_boxes'] = []
    
    return jsonify({
        'success': True,
        'message': f'🎅 Дед Мороз наполнил все коробки! Теперь вы можете открыть до {AUTH_LIMIT} новых подарков.',
        'remaining_boxes': 10,
        'opened_count': 0
    })

@lab9.route('/api/get_state', methods=['GET'])
def get_state():
    is_auth = session.get('is_authenticated', False)
    user_limit = AUTH_LIMIT if is_auth else GUEST_LIMIT
    
    return jsonify({
        'opened_boxes': list(boxes_state['opened_boxes']),
        'user_opened_boxes': session.get('user_opened_boxes', []),
        'opened_count': session.get('opened_count', 0),
        'remaining_boxes': len(boxes_state['available_boxes']),
        'total_boxes': 10,
        'is_authenticated': is_auth,
        'username': session.get('username', None),
        'user_limit': user_limit,
        'remaining_limit': user_limit - session.get('opened_count', 0)
    })

@lab9.route('/reset', methods=['POST'])
def reset():
    boxes_state['opened_boxes'] = set()
    boxes_state['available_boxes'] = list(range(1, 11))
    
    session['opened_count'] = 0
    session['user_opened_boxes'] = []
    session['is_authenticated'] = False
    session['username'] = None
    
    return jsonify({
        'success': True,
        'message': 'Игра полностью сброшена'
    })