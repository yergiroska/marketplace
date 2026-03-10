import pytest
from app.models import User

def test_crear_usuario_vendedor(db):
    user = User(
        username='vendedor1',
        email='vendedor1@test.com',
        role='vendedor'
    )
    user.set_password('12345')
    db.session.add(user)
    db.session.commit()

    assert user.id is not None
    assert user.role == 'vendedor'
    assert user.check_password('12345') == True
    assert user.check_password('wrong') == False

def test_crear_usuario_comprador(db):
    user = User(
        username='comprador1',
        email='comprador1@test.com',
        role='comprador'
    )
    user.set_password('12345')
    db.session.add(user)
    db.session.commit()

    assert user.id is not None
    assert user.role == 'comprador'

def test_email_unico(db):
    user1 = User(username='user1', email='mismo@test.com', role='comprador')
    user1.set_password('12345')
    db.session.add(user1)
    db.session.commit()

    user2 = User(username='user2', email='mismo@test.com', role='comprador')
    user2.set_password('12345')
    db.session.add(user2)

    with pytest.raises(Exception):
        db.session.commit()

def test_registro_vendedor(client, db):
    response = client.post('/register', data={
        'username': 'vendedor_test',
        'email': 'vendedor_test@test.com',
        'password': '12345678',
        'confirm_password': '12345678',
        'role': 'vendedor'
    }, follow_redirects=True)

    assert response.status_code == 200
    user = User.query.filter_by(email='vendedor_test@test.com').first()
    assert user is not None
    assert user.role == 'vendedor'

def test_registro_comprador(client, db):
    response = client.post('/register', data={
        'username': 'comprador_test',
        'email': 'comprador_test@test.com',
        'password': '12345678',
        'confirm_password': '12345678',
        'role': 'comprador'
    }, follow_redirects=True)

    assert response.status_code == 200
    user = User.query.filter_by(email='comprador_test@test.com').first()
    assert user is not None
    assert user.role == 'comprador'

def test_login_correcto(client, db):
    user = User(username='login_test', email='login_test@test.com', role='comprador')
    user.set_password('12345678')
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', data={
        'email': 'login_test@test.com',
        'password': '12345678'
    }, follow_redirects=True)

    assert response.status_code == 200

def test_login_incorrecto(client, db):
    response = client.post('/login', data={
        'email': 'noexiste@test.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Email o contraseña incorrectos'.encode() in response.data