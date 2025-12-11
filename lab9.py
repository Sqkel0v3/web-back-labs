from flask import Blueprint, render_template, request, jsonify
import math
lab6 = Blueprint('lab9', __name__)

@lab9.route('/')
def index():
    return render_template('lab9/index.html')
