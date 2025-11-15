from flask import Blueprint, render_template, request, session
import psycopg2
import os

lab6 = Blueprint('lab6', __name__)

DATABASE_CONFIG = {
    'dbname': 'roman_fomchenko_knowledge_base',
    'user': 'roman_fomchenko_knowledge_base', 
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

def get_db():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT number, tenant, price FROM offices ORDER BY number')
        offices = cur.fetchall()
        cur.close()
        conn.close()
        
        offices_list = [
            {'number': office[0], 'tenant': office[1], 'price': office[2]}
            for office in offices
        ]
        
        return {
            'jsonrpc': '2.0',
            'result': offices_list,
            'id': id
        }
    
    elif data['method'] == 'booking':
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }

        office_number = data['params']
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'SELECT number, tenant FROM offices WHERE number = %s', 
            (office_number,)
        )
        office = cur.fetchone()
        
        if not office:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32001,
                    'message': 'Office not found'
                },
                'id': id
            }
        
        if office[1]:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }

        cur.execute(
            'UPDATE offices SET tenant = %s WHERE number = %s',
            (login, office_number)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
    
    elif data['method'] == 'cancellation':
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }

        office_number = data['params']
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'SELECT number, tenant FROM offices WHERE number = %s', 
            (office_number,)
        )
        office = cur.fetchone()
        
        if not office:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32001,
                    'message': 'Office not found'
                },
                'id': id
            }
        
        if not office[1]:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office is not booked'
                },
                'id': id
            }
        
        if office[1] != login:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'You can only cancel your own booking'
                },
                'id': id
            }

        cur.execute(
            'UPDATE offices SET tenant = %s WHERE number = %s',
            ('', office_number)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
    
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }