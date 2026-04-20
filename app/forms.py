from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(), Length(min=3, max=80)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(), Length(min=6)
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(), EqualTo('password')
    ])
    role = SelectField('Rol', choices=[
        ('comprador', 'Comprador'),
        ('vendedor', 'Vendedor')
    ])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ese nombre de usuario ya existe.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ese email ya está registrado.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired()
    ])
    submit = SubmitField('Iniciar Sesión')

class ProductForm(FlaskForm):
    name = StringField('Nombre', validators=[
        DataRequired(), Length(min=3, max=200)
    ])
    description = StringField('Descripción', validators=[])
    price = DecimalField('Precio', validators=[
        DataRequired()
    ], places = 2)
    stock = StringField('Stock', validators=[
        DataRequired()
    ])
    category_id = SelectField('Categoría', coerce=int)
    image = FileField('Imagen del producto', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imágenes jpg y png.')
    ])
    submit = SubmitField('Guardar Producto')


class CategoryForm(FlaskForm):
    name = StringField('Nombre', validators=[
        DataRequired(), Length(min=3, max=100)
    ])
    submit = SubmitField('Guardar Categoría')