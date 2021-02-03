from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

# models go below
class User(db.Model):
    """User."""

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.email} {u.first_name} {u.last_name}>"

    __tablename__ = "users"

    email = db.Column(db.Text,
                      primary_key=True,
                      nullable=False,
                      unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)

    @classmethod
    # authenticate a user
    def authenticate(cls, email, password):
        u=User.query.get_or_404(email)
        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else: 
            return False
    
    @classmethod
    # signs up a new user
    def signup(cls, email, password, first_name, last_name):
        hashed_password = bcrypt.generate_password_hash(password).decode("utf8")
        u=cls(email=email, password=hashed_password, first_name=first_name, last_name=last_name)
        db.session.add(u)
        try:
            db.session.commit()
            return u
        except:
            raise RuntimeError('something went wrong')

class Item(db.Model):
    """Item."""

    def __repr__(self):
        """Show info about item."""

        i = self
        return f"<Item {i.id} {i.name} {i.quantity} {i.image_path}>"

    __tablename__ = "items"

    id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_path=db.Column(db.Text)

class Category(db.Model):
    """category."""

    def __repr__(self):
        """Show info about category."""

        c = self
        return f"<Item {c.id} {c.name} {c.description}>"

    __tablename__ = "categories"

    id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

class Item_Category():
    