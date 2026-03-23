import pytest
from app.models import User, Product, Category, CartItem, Order, OrderItem

def test_confirmar_pedid(client, db):
    #Crear comprador
    comprador = User(username='comprador_order', email='comprador_order@test.com', role='comprador')
    comprador.set_password('12345678')
    db.session.add(comprador)
    db.session.commit()

    vendedor = User(username='vendedor_ordert', email='vendedor_ordert@test.com', role='vendedor')
    vendedor.set_password('12345678')
    db.session.add(vendedor)
    db.session.commit()

    categoria = Category(name='Order Test')
    db.session.add(categoria)
    db.session.commit()

    producto = Product(
        name = 'Producto Order',
        description = 'Test',
        price = 100,
        stock = 10,
        user_id = vendedor.id,
        category_id = categoria.id,
    )
    db.session.add(producto)
    db.session.commit()

    #Agregar al carrito
    cart_item = CartItem(
        user_id = comprador.id,
        product_id = producto.id,
        quantity = 2
    )
    db.session.add(cart_item)
    db.session.commit()


    #Login como comprador
    client.post('/login', data={
        'email': 'comprador_order@test.com',
        'password': '12345678'
    })

    #Confirmar pedido
    response = client.post('/orders/create', follow_redirects=True)
    assert response.status_code == 200

    db.session.expire_all()

    #Verificar que se creo el pedido
    order = Order.query.filter_by(user_id = comprador.id).first()
    assert order is not None
    assert order.total == 200

    # Verificar que el pedido tiene los items correctos
    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    assert len(order_items) == 1
    assert order_items[0].quantity == 2
    assert order_items[0].price == 100

    # Verificar que el stock se redujo
    producto = Product.query.get(producto.id)
    assert producto.stock == 8

def test_ver_pedidos(client, db):
        comprador = User(username='comprador_order2', email='comprador_order2@test.com', role='comprador')
        comprador.set_password('12345678')
        db.session.add(comprador)
        db.session.commit()

        client.post('/login', data={
            'email': 'comprador_order2@test.com',
            'password': '12345678'
        })

        response = client.get('/orders/', follow_redirects=True)
        assert response.status_code == 200
        assert 'Pedidos'.encode() in response.data

def test_carrito_vacio_no_crea_pedido(client, db):
        comprador = User(username='comprador_order3', email='comprador_order3@test.com', role='comprador')
        comprador.set_password('12345678')
        db.session.add(comprador)
        db.session.commit()

        client.post('/login', data={
            'email': 'comprador_order3@test.com',
            'password': '12345678'
        })

        response = client.post('/orders/create', follow_redirects=True)
        assert response.status_code == 200
        assert 'carrito está vacío'.encode() in response.data
