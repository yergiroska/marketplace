from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(testing=False):
    app = Flask(__name__)

    # Configuración
    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'test-secret-key'
    else:
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB máximo por imagen

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Crear carpeta uploads si no existe
    uploads_folder = os.path.join(app.root_path, 'static/uploads')
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    login_manager.login_view = 'auth.login'

    # Registrar rutas
    from app.routes.auth import auth
    from app.routes.products import products
    from app.routes.cart import cart
    from app.routes.orders import orders
    app.register_blueprint(auth)
    app.register_blueprint(products)
    app.register_blueprint(cart)
    app.register_blueprint(orders)

    from app import models

    # Manejador 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app