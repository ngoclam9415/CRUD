import re
import unittest
from app import create_app, db
from app.models import User


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_login(self):
        # register a new account
        response = self.client.post('/auth/register', data={
            'email': 'john@example.com',
            'password': 'Admin123',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # login with the new account
        response = self.client.post('/auth/login', data={
            'email': 'john@example.com',
            'password': 'Admin123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # log out
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_wrong_type_password(self):
        # register a new account
        response = self.client.post('/auth/register', data={
            'email': 'john@example.com',
            'password': 'cat',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b'Your password must contain at least one lowercase letter, one capital letter and one number, 8-30 characters long' in response.data)
