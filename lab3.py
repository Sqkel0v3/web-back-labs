from flask import Blueprint, render_template

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def main():
    return render_template('/lab3.html')

@lab3.route('/cookie')
def cookie():
    return "Страница для работы с cookie"