from flask import Blueprint, render_template

lab8 = Blueprint('lab8', __name__, template_folder='templates')

@lab8.route('/')
def index():
    return render_template('lab8/index.html', username="anonymous")