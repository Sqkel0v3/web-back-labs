from flask import Blueprint, render_template

lab8_bp = Blueprint('lab8', __name__, template_folder='templates')

@lab8_bp.route('/')
def index():
    return render_template('lab8/index.html', username="anonymous")