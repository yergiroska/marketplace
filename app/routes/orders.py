from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import  db
from app.models import Order, OrderItem, CartItem
from app.decorators import comprador_required

orders = Blueprint('orders', __name__, url_prefix='/orders')

@orders.route('/')
@login_required
@comprador_required

def index():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders/index.html', orders=user_orders)

@orders.route('/create', methods=['POST'])
@login_required
@comprador_required
def create():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash('Tú carrito esta vacío', 'danger')
        return redirect(url_for('cart.index'))

    #Calcular total
    total = sum(item.product.price * item.quantity for item in cart_items)

    #Craer Pedido
    order = Order(
        user_id=current_user.id,
        total=total,
        status = 'pendiente'
    )
    db.session.add(order)
    db.session.flush()

    #Crear order item y reducir stock
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.session.add(order_item)
        item.product.stock -= item.quantity
        db.session.add(item.product)
        db.session.delete(item)

    db.session.commit()
    flash('¡Pedido confirmado exitosamente!', 'success')
    return redirect(url_for('orders.index'))

@orders.route('/<int:order_id>/confirm', methods=['POST'])
@login_required
@comprador_required
def confirm_delivery(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('No tienes permiso para confirmar este pedido.', 'danger')
        return redirect(url_for('orders.index'))
    if order.status == 'enviado':
        order.status = 'entregado'
        db.session.commit()
        flash('¡Entrega confirmada exitosamente!', 'success')
    return redirect(url_for('orders.index'))