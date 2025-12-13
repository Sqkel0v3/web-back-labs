from flask import Blueprint, render_template, request, jsonify, session
import random
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
    {"id": 1, "message": "С Новым годом! Пусть этот год принесет много счастья и удачи!", "gift": "🎁"},
    {"id": 2, "message": "Желаем здоровья, любви и процветания в новом году!", "gift": "🎄"},
    {"id": 3, "message": "Пусть все мечты сбудутся, а планы осуществятся!", "gift": "⭐"},
    {"id": 4, "message": "Счастья, улыбок и тепла в вашем доме!", "gift": "❤️"},
    {"id": 5, "message": "Успехов в работе и творческого вдохновения!", "gift": "✨"},
    {"id": 6, "message": "Мира, добра и благополучия вашей семье!", "gift": "🏠"},
    {"id": 7, "message": "Пусть каждый день будет наполнен радостью!", "gift": "😊"},
    {"id": 8, "message": "Исполнения самых заветных желаний!", "gift": "🌠"},
    {"id": 9, "message": "Финансового благополучия и стабильности!", "gift": "💰"},
    {"id": 10, "message": "Крепкого здоровья и бодрости духа!", "gift": "💪"}
]

@lab9.route('/')
def index():
    if 'opened_count' not in session:
        session['opened_count'] = 0
    if 'user_opened_boxes' not in session:
        session['user_opened_boxes'] = []
    
    return render_template('lab9/index.html', 
                         box_positions=box_positions,
                         total_boxes=len(boxes_state['available_boxes']),
                         opened_count=session['opened_count'])

@lab9.route('/api/open_box', methods=['POST'])
def open_box():
    data = request.get_json()
    box_id = data.get('box_id')
    
    if box_id not in boxes_state['available_boxes']:
        return jsonify({'success': False, 'message': 'Коробка не найдена'})
    
    if box_id in boxes_state['opened_boxes']:
        return jsonify({'success': False, 'message': 'Эта коробка уже открыта'})
    
    if session.get('opened_count', 0) >= 3:
        return jsonify({'success': False, 'message': 'Вы уже открыли максимальное количество коробок (3)'})
    
    congrat = next((c for c in congratulations if c['id'] == box_id), None)
    if not congrat:
        return jsonify({'success': False, 'message': 'Поздравление не найдено'})
    
    boxes_state['opened_boxes'].add(box_id)
    
    session['opened_count'] = session.get('opened_count', 0) + 1
    user_opened = session.get('user_opened_boxes', [])
    user_opened.append(box_id)
    session['user_opened_boxes'] = user_opened
    
    boxes_state['available_boxes'] = [b for b in boxes_state['available_boxes'] if b != box_id]
    
    return jsonify({
        'success': True,
        'message': congrat['message'],
        'gift': congrat['gift'],
        'opened_count': session['opened_count'],
        'remaining_boxes': len(boxes_state['available_boxes'])
    })

@lab9.route('/api/get_state', methods=['GET'])
def get_state():
    user_opened = session.get('user_opened_boxes', [])
    return jsonify({
        'opened_boxes': list(boxes_state['opened_boxes']),
        'user_opened_boxes': user_opened,
        'opened_count': session.get('opened_count', 0),
        'remaining_boxes': len(boxes_state['available_boxes']),
        'total_boxes': 10
    })

@lab9.route('/reset', methods=['POST'])
def reset():
    boxes_state['opened_boxes'] = set()
    boxes_state['available_boxes'] = list(range(1, 11))
    session['opened_count'] = 0
    session['user_opened_boxes'] = []
    return jsonify({'success': True, 'message': 'Состояние сброшено'})