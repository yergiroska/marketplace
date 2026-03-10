from flask import Blueprint, render_template
from flask_login import login_required

products = Blueprint('products', __name__)

@products.route('/')
def index():
    return render_template('products/index.html')

@products.route('/dashboard')
@login_required
def dashboard():
    return render_template('products/dashboard.html')