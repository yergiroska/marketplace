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