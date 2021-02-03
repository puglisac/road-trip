from flask import Flask
from users.users import users_blueprint
from models import db, connect_db
from flask_jwt_extended import JWTManager, create_access_token
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

connect_db(app)
app.register_blueprint(users_blueprint, url_prefix="/users")

db.create_all()

@app.route('/')
def index():
    return "in app.py"