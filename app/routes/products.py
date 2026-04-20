from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Product, Category
from app.forms import ProductForm
from app.decorators import vendedor_required
import os
import uuid

products = Blueprint('products', __name__)

@products.route('/')
def index():
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '')

    query = Product.query.filter(Product.stock > 0)
    if category_id:
        query = query.filter_by(category_id = category_id)

    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    all_products = query.order_by(Product.created_at.desc()).all()
    categories = Category.query.all()

    return render_template('products/index.html',
        products=all_products,
        categories=categories,
        category_id=category_id,
        search=search
    )

@products.route('/dashboard')
@login_required
@vendedor_required
def dashboard():
    user_products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template('products/dashboard.html', products=user_products)

@products.route('/products/create', methods=['GET', 'POST'])
@login_required
@vendedor_required
def create():
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        image_filename = None
        if form.image.data:
            image_filename = save_image(form.image.data)
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=float(form.price.data),
            stock=form.stock.data,
            category_id=form.category_id.data,
            image=image_filename,
            user_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash('Producto creado exitosamente.', 'success')
        return redirect(url_for('products.dashboard'))
    return render_template('products/create.html', form=form)

@products.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@vendedor_required
def edit(product_id):
    product = Product.query.get_or_404(product_id)
    if product.user_id != current_user.id:
        flash('No tienes permiso para editar este producto.', 'danger')
        return redirect(url_for('products.dashboard'))
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = float(form.price.data)
        product.stock = form.stock.data
        product.category_id = form.category_id.data
        from werkzeug.datastructures import FileStorage
        if form.image.data and isinstance(form.image.data, FileStorage) and form.image.data.filename:
            product.image = save_image(form.image.data)
        db.session.commit()
        flash('Producto actualizado exitosamente.', 'success')
        return redirect(url_for('products.dashboard'))
    return render_template('products/edit.html', form=form, product=product)

@products.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
@vendedor_required
def delete(product_id):
    product = Product.query.get_or_404(product_id)
    if product.user_id != current_user.id:
        flash('No tienes permiso para eliminar este producto.', 'danger')
        return redirect(url_for('products.dashboard'))
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado exitosamente.', 'success')
    return redirect(url_for('products.dashboard'))

def save_image(image_file):
    ext = image_file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    image_file.save(path)
    return filename


@products.route('/categories')
@login_required
@vendedor_required
def categories():
    all_categories = Category.query.all()
    return render_template('products/categories.html', categories=all_categories)

@products.route('/categories/create', methods=['GET', 'POST'])
@login_required
@vendedor_required
def create_category():
    from app.forms import CategoryForm
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Categoria creado exitosamente.', 'success')
        return redirect(url_for('products.categories'))
    return render_template('products/create_category.html', form=form)

@products.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@vendedor_required
def edit_category(category_id):
    from app.forms import CategoryForm
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.add(category)
        db.session.commit()
        flash('Categoria actualizada exitosamente.', 'success')
        return redirect(url_for('products.categories'))
    return render_template('products/edit_category.html', form=form)

@products.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
@vendedor_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Categoría eliminada.', 'success')
    return redirect(url_for('products.categories'))

@products.route('/orders')
@login_required
@vendedor_required
def vendor_orders():
    from app.models import OrderItem, Order
    order_items = OrderItem.query.join(Product).filter(
        Product.user_id == current_user.id
    ).all()
    return render_template('products/vendor_orders.html', order_items=order_items)

@products.route('/orders/<int:order_id>/status', methods=['POST'])
@login_required
@vendedor_required
def update_order_status(order_id):
    from app.models import Order
    from flask import request
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status in ['enviado', 'entregado']:
        order.status = new_status
        db.session.commit()
        flash('Estado del pedido actualizado.', 'success')
    return redirect(url_for('products.vendor_orders'))
