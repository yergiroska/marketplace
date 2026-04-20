# 🛒 Marketplace

Aplicación web de marketplace desarrollada con Python, Flask y PostgreSQL. Permite a vendedores publicar productos y a compradores realizar compras con un flujo completo de pedidos.

## 🚀 Tecnologías

- **Backend:** Python 3.13, Flask
- **Base de datos:** PostgreSQL
- **ORM:** Flask-SQLAlchemy
- **Migraciones:** Flask-Migrate
- **Autenticación:** Flask-Login
- **Formularios:** Flask-WTF
- **Testing:** pytest, pytest-flask
- **Frontend:** Jinja2, Bootstrap 5

## ✨ Funcionalidades

### Autenticación
- Registro con dos roles: **vendedor** y **comprador**
- Login y logout
- Rutas protegidas por rol con decoradores personalizados
- Contraseñas encriptadas con Werkzeug

### Panel del vendedor
- CRUD completo de productos con subida de imágenes
- CRUD completo de categorías
- Alertas de stock bajo y sin stock
- Gestión de pedidos con cambio de estado (`pendiente` → `enviado`)

### Catálogo público
- Listado de productos con imágenes
- Filtro por categoría
- Búsqueda por nombre
- Solo muestra productos con stock disponible

### Carrito de compras
- Persistencia en base de datos
- Agregar, actualizar cantidad y eliminar productos
- Cálculo automático del total
- Exclusivo para compradores

### Pedidos
- Confirmar pedido desde el carrito
- Reducción automática de stock al confirmar
- Historial de compras del comprador
- Confirmación de entrega por el comprador (`enviado` → `entregado`)

## 🧪 Testing

El proyecto usa TDD (Test Driven Development) con pytest.

```bash
# Correr todos los tests
pytest tests/ -v

# Correr tests específicos
pytest tests/test_auth.py -v
pytest tests/test_products.py -v
pytest tests/test_cart.py -v
pytest tests/test_orders.py -v
```

## ⚙️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/yergiroska/marketplace.git
cd marketplace
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Mac/Linux
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto:
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/marketplace
```

### 5. Crear la base de datos
Crea la base de datos `marketplace` en PostgreSQL y ejecuta las migraciones:
```bash
flask db upgrade
```

### 6. Levantar el servidor
```bash
flask run --debug
```

## 📁 Estructura del proyecto

```
marketplace/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── decorators.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   └── orders.py
│   ├── templates/
│   └── static/
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_orders.py
├── .env
├── run.py
└── requirements.txt
```
## 🗄️ Modelos de base de datos

- **User** → usuarios con rol vendedor o comprador
- **Product** → productos del vendedor
- **Category** → categorías de productos
- **CartItem** → items del carrito de compras
- **Order** → pedidos confirmados
- **OrderItem** → productos dentro de un pedido

## 👤 Autor

**Yergiroska** - [github.com/yergiroska](https://github.com/yergiroska)