from unittest import TestCase
from app import app
from models import db, connect_db, User
from flask import jsonify
import os

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///inventory_manager_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "some_secret_key"
app.config['TESTING'] = True

connect_db(app)

db.create_all()

class TestUsersRoutes(TestCase):
    
    @classmethod
    def setUpClass(cls):
        """ get_some_resource() is slow, to avoid calling it for eachtest  use setUpClass()
            and store the result as class variable
        """
        super(TestUsersRoutes, cls).setUpClass()
        User.query.delete()
        cls.admin_test_user=User.signup(
                            email="admin_test@email.com",
                            password="password",
                            first_name="First",
                            last_name="Last",
                            is_admin=True
        )
        cls.test_user=User.signup(
                            email="test@email.com",
                            password="anotherPassword",
                            first_name="First",
                            last_name="Last",
                            is_admin=False
        )
        cls.editing_user=User.signup(    
                        email="email@email.com",
                        password="anotherPassword",
                        first_name="firstName",
                        last_name="lastName",
                        is_admin=False
        )
        db.session.add_all([cls.admin_test_user, cls.test_user, cls.editing_user])
        db.session.commit()
        cls.admin_token = None
        cls.token = None
        with app.test_client() as client:
            resp = client.post("/users/login", json=   {"email":"admin_test@email.com", "password": "password"})
            cls.admin_token = resp.json['access_token']

        with app.test_client() as client:
            resp = client.post("/users/login", json={"email":"test@email.com", "password": "anotherPassword"})
            cls.token = resp.json['access_token']


    def test_login(self):
        with app.test_client() as client:
            resp = client.post("/users/login", json={"email":"admin_test@email.com", "password": "password"})
            
            self.assertEqual(resp.status_code, 200)

    def test_invalid_login(self):
        with app.test_client() as client:
            resp = client.post("/users/login", json={"email":"test@email.com", "password": "password"})
            self.assertEqual(resp.status_code, 401)
    
    def test_signup(self):
        with app.test_client() as client:
            resp = client.post("/users/signup", json={
                                                "first_name":"New",
                                                "last_name":"User",
                                                "password":"password", 
                                                "email": "new@email.com", 
                                                "is_admin": False
                                                }, headers={ 'Authorization': f'Bearer {TestUsersRoutes.admin_token}'})
            self.assertEqual(resp.status_code, 201)

    def test_invalid_signup(self):
        with app.test_client() as client:
            resp = client.post("/users/signup", json={
                                                "first_name":"New",
                                                "last_name":"User",
                                                "password":"password", 
                                                "email": "another@email.com", 
                                                "is_admin": False
                                                }, headers={ 'Authorization': f'Bearer {TestUsersRoutes.token}'})
            self.assertEqual(resp.status_code, 401)
    
    def test_get_all_users(self):
        with app.test_client() as client:
            resp = client.get("/users/", headers={ 'Authorization': f'Bearer {TestUsersRoutes.admin_token}'})
            self.assertEqual(resp.status_code, 200)

    def test_invalid_get_all_users(self):
        with app.test_client() as client:
            resp = client.get("/users/", headers={ 'Authorization': f'Bearer {TestUsersRoutes.token}'})
            self.assertEqual(resp.status_code, 401)

    def test_get_one_user(self):
        with app.test_client() as client:
            resp = client.get("/users/test@email.com", headers={ 'Authorization': f'Bearer {TestUsersRoutes.admin_token}'})
            self.assertEqual(resp.status_code, 200)

    def test_unauth_get_one_users(self):
        with app.test_client() as client:
            resp = client.get("/users/admin_test@email.com", headers={ 'Authorization': f'Bearer {TestUsersRoutes.token}'})
            self.assertEqual(resp.status_code, 401)
    
    def test_get_self(self):
        with app.test_client() as client:
            resp = client.get("/users/test@email.com", headers={ 'Authorization': f'Bearer {TestUsersRoutes.token}'})
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['user']['email'], 'test@email.com')

    def test_unauth_edit_user(self):
        with app.test_client() as client:
            resp = client.patch("/users/email@email.com", headers={ 'Authorization': f'Bearer {TestUsersRoutes.token}'}, 
            json={'email': 'new_test@email.com'})
            self.assertEqual(resp.status_code, 401)

    def test_edit_user_as_admin(self):
        with app.test_client() as client:
            resp = client.patch("/users/email@email.com", headers={ 'Authorization': f'Bearer {TestUsersRoutes.admin_token}'}, 
            json={'email': 'new_test@email.com'})
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['user']['email'], 'new_test@email.com')