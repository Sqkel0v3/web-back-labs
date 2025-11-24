from flask import Blueprint, render_template, request, session
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

def get_db():
    db_path = path.join(path.dirname(path.abspath(__file__)), "offices.db")
    conn = sqlite3.connect(db_path)
    return conn

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    method = data['method']

    if method == 'info':
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
        offices = cur.fetchall()
        cur.close()
        conn.close()

        offices_list = [
            {"number": o[0], "tenant": o[1], "price": o[2]} for o in offices
        ]

        return {"jsonrpc": "2.0", "result": offices_list, "id": id}

    elif method == 'booking':
        login = session.get("login")
        if not login:
            return {
                "jsonrpc": "2.0",
                "error": {"code": 1, "message": "Unauthorized"},
                "id": id
            }

        office_number = data["params"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT number, tenant FROM offices WHERE number = ?", (office_number,))
        office = cur.fetchone()

        if not office:
            cur.close()
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32001, "message": "Office not found"},
                "id": id
            }

        if office[1]:
            cur.close()
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": 2, "message": "Already booked"},
                "id": id
            }

        # Резервируем
        cur.execute("UPDATE offices SET tenant = ? WHERE number = ?", (login, office_number))
        conn.commit()
        cur.close()
        conn.close()

        return {"jsonrpc": "2.0", "result": "success", "id": id}

    elif method == 'cancellation':
        login = session.get("login")
        if not login:
            return {
                "jsonrpc": "2.0",
                "error": {"code": 1, "message": "Unauthorized"},
                "id": id
            }

        office_number = data["params"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT number, tenant FROM offices WHERE number = ?", (office_number,))
        office = cur.fetchone()

        if not office:
            cur.close()
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32001, "message": "Office not found"},
                "id": id
            }

        if not office[1]:
            cur.close()
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": 3, "message": "Office is not booked"},
                "id": id
            }

        if office[1] != login:
            cur.close()
            conn.close()
            return {
                "jsonrpc": "2.0",
                "error": {"code": 4, "message": "You can only cancel your own booking"},
                "id": id
            }

        cur.execute("UPDATE offices SET tenant = '' WHERE number = ?", (office_number,))
        conn.commit()
        cur.close()
        conn.close()

        return {"jsonrpc": "2.0", "result": "success", "id": id}

    return {
        "jsonrpc": "2.0",
        "error": {"code": -32601, "message": "Method not found"},
        "id": id
    }
