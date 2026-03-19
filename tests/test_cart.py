import pytest
from app.models import User, Product, Category, CartItem

def test_agregar_producto_al_carrito(client, db):
    #Crear comprador
    comprador = User(username = 'comprador_cart', email = 'comprador_cart@test.com', role = 'comprador')
    comprador.set_password('12345678')
    db.session.add(comprador)
    db.session.commit()

    vendedor = User(username='vendedor_cart', email='vendedor_cart@test.com', role='vendedor')
    vendedor.set_password('12345678')
    db.session.add(vendedor)
    db.session.commit()

    categoria = Category(name='Test')
    db.session.add(categoria)
    db.session.commit()

    producto = Product(
        name = 'Producto Test',
        description = 'Test',
        price = 350,
        stock = 10,
        user_id = vendedor.id,
        category_id = categoria.id,
    )
    db.session.add(producto)
    db.session.commit()

    #Login como comprador
    client.post('/login', data={
        'email': 'comprador_cart@test.com',
        'password': '12345678'
    })

    #Agregar al Carrito
    response = client.post(f'/cart/add/{producto.id}', follow_redirects=True)
    assert response.status_code == 200

    #Verificar que se guardó en BD
    cart_item = CartItem.query.filter_by(
        user_id = comprador.id,
        product_id = producto.id

    ).first()
    assert response.status_code == 200
    assert cart_item.quantity == 1

def test_carrito_solo_compradores(client, db):
    vendedor = User(username='vendedor_cart2', email='vendedor_cart2@test.com', role='vendedor')
    vendedor.set_password('12345678')
    db.session.add(vendedor)
    db.session.commit()

    categoria = Category(name='Test2')
    db.session.add(categoria)
    db.session.commit()

    producto = Product(
        name = 'Producto Test2',
        description = 'Test2',
        price = 320,
        stock = 8,
        user_id = vendedor.id,
        category_id = categoria.id,
    )
    db.session.add(producto)
    db.session.commit()

    # Cerrar sesión anterior
    client.get('/logout', follow_redirects=True)

    #Login como vendedor
    client.post('/login', data={
        'email': 'vendedor_cart2@test.com',
        'password': '12345678'
    })

    #Agregar al Carrito
    response = client.post(f'/cart/add/{producto.id}', follow_redirects=True)
    assert response.status_code == 200
    assert 'Acceso restringido a compradores.'.encode() in response.data

def test_ver_carrito(client, db):
    comprador = User(username='comprador_cart3', email='comprador_cart3@test.com', role='comprador')
    comprador.set_password('12345678')
    db.session.add(comprador)
    db.session.commit()

    client.post('/login', data={
        'email': 'comprador_cart3@test.com',
        'password': '12345678'
    })

    response = client.get('/cart/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Carrito'.encode() in response.data