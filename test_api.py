import unittest
from main import create_app
from config import TestConfig
from werkzeug.security import generate_password_hash
from exts import db


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            # db.init_app(self.app)
            db.create_all()

    def test_hello_world(self):
        hello_response = self.client.get("/hello/")
        print("hello_response", hello_response)
        json = hello_response.json
        print(json)
        self.assertEqual(json, {"message": "Hello, World!"})

    def test_signup(self):
        signup_response = self.client.post(
            "/auth/signup",
            json={"username": "test_user", "email": "testuser@test.com", "password": "test_password"},
        )
        status_code = signup_response.status_code
        json = signup_response.json
        self.assertEqual(status_code, 201)
        self.assertEqual(json["message"], "User created successfully.")
        
    def test_login(self):
        self.client.post(
            "/auth/signup",
            json={"username": "test_user", "email": "test_user@tese.com", "password": "test_password"},
        )
        login_response = self.client.post(
            "/auth/login",
            json={"username": "test_user", "password": "test_password"},
        )
        status_code = login_response.status_code
        json = login_response.json
        self.assertEqual(status_code, 200)
        self.assertIn("access_token", json)
        self.assertIn("refresh_token", json)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
