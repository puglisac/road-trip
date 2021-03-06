from flask import Flask
from flask_cors import CORS
from users import users_blueprint
from items import items_blueprint
from categories import categories_blueprint
from models import db, connect_db
from flask_jwt_extended import JWTManager, create_access_token
import os
from datetime import timedelta

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///inventory_manager')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if os.environ.get('SQLALCHEMY_ECHO'):
    app.config['SQLALCHEMY_ECHO)'] = True
else:
    app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
jwt = JWTManager(app)

connect_db(app)
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(items_blueprint, url_prefix="/items")
app.register_blueprint(categories_blueprint, url_prefix="/categories")

# db.drop_all()
db.create_all()

@app.route('/')
def index():
    return "in app.py"