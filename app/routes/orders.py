from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

orders = Blueprint('orders', __name__, url_prefix='/orders')

@orders.route('/')
@login_required
def index():
    return render_template('orders/index.html')

@orders.route('/create', methods=['POST'])
@login_required
def create():
    return redirect(url_for('orders.index'))