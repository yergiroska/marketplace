from flask import Blueprint, render_template
from flask_login import login_required

cart = Blueprint('cart', __name__, url_prefix='/cart')

@cart.route('/')
@login_required
def index():
    return render_template('cart/index.html')