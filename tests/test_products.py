from http import client

import pytest
from app.models import User, Product, Category

def test_crear_producto(db):
    #Crear vendedor
    vendedor = User(username = 'vendedor_prod', email = 'vendedor_prod@test.com', role = 'vendedor')
    vendedor.set_password('12345678')
    db.session.add(vendedor)
    db.session.commit()

    #crear categoria
    categoria = Category(name = 'Electronica')
    db.session.add(categoria)
    db.session.commit()

    #crear producto
    producto = Product(
        name = 'Laptop',
        description = 'Laptop Gamer',
        price = 500,
        stock = 10,
        user_id = vendedor.id,
        category_id = categoria.id,
    )
    db.session.add(producto)
    db.session.commit()

    assert producto.id is not None
    assert producto.name == 'Laptop'
    assert producto.price == 500
    assert producto.stock == 10
    assert producto.seller.username == 'vendedor_prod'

def test_vendedor_no_puede_ver_dashboard_sin_login(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert 'Iniciar' .encode() in response.data

def test_comprador_no_puede_ver_dashboard_sin_login(client, db):
    comprador = User(username = 'comprador_prod', email = 'comprador_prod@test.com', role = 'comprador')
    comprador.set_password('12345678')
    db.session.add(comprador)
    db.session.commit()

    client.post('/login', data = {
        'email': 'comprador_prod@test.com',
        'password': '12345678'
    })

    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert 'Acceso restringido a vendedores' .encode() in response.data

def test_catalogo_visible_sin_login(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Catálogo' .encode() in response.data

def test_catalogo_muestra_productos(client, db):
    vendedor = User(username = 'vendedor_cat', email = 'vendedor_cat@test.com', role = 'vendedor')
    vendedor.set_password('12345678')
    db.session.add(vendedor)
    db.session.commit()

    categoria = Category(name = 'Tecnología')
    db.session.add(categoria)
    db.session.commit()

    producto = Product(
        name = 'Monitor',
        description = 'Monitor 4K',
        price = 350,
        stock = 10,
        user_id = vendedor.id,
        category_id = categoria.id,
    )
    db.session.add(producto)
    db.session.commit()

    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Monitor' .encode() in response.data

def test_filtro_por_categoria(client, db):
    vendedor = User(username = 'vendedor_filtro', email = 'vendedor_filtro@test.com', role = 'vendedor')
    vendedor.set_password('12345678')
    db.session.add(vendedor)
    db.session.commit()

    categoria = Category(name = 'Música')
    db.session.add(categoria)
    db.session.commit()

    producto = Product(
        name = 'Guitarra',
        description = 'Guitarra Eléctrica',
        price = 100,
        stock = 5,
        user_id = vendedor.id,
        category_id = categoria.id,
    )

    db.session.add(producto)
    db.session.commit()

    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Guitarra' .encode() in response.data




