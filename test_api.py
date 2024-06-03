import unittest
from main import create_app
from config import TestConfig
from exts import db


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            # db.init_app(self.app)
            db.create_all()

        # # 注册一个测试用户
        self.client.post(
            "/auth/signup",
            json={
                "username": "test_user",
                "email": "test_user@test.com",
                "password": "test_password",
            },
        )

        # 使用测试用户登录获取token
        response = self.client.post(
            "/auth/login",
            json={"username": "test_user", "password": "test_password"},
        )
        self.access_token = response.json["access_token"]

    def test_hello_world(self):
        hello_response = self.client.get("/hello/")
        print("hello_response", hello_response)
        json = hello_response.json
        print(json)
        self.assertEqual(json, {"message": "Hello, World!"})

    def test_signup(self):
        signup_response = self.client.post(
            "/auth/signup",
            json={
                "username": "test_user2",
                "email": "test_user2@test.com",
                "password": "test_password",
            },
        )
        status_code = signup_response.status_code
        json = signup_response.json
        self.assertEqual(status_code, 201)
        self.assertEqual(json["message"], "User created successfully.")

    def test_login(self):
        self.client.post(
            "/auth/signup",
            json={
                "username": "test_user3",
                "email": "test_user3@test.com",
                "password": "test_password",
            },
        )
        login_response = self.client.post(
            "/auth/login",
            json={"username": "test_user3", "password": "test_password"},
        )

        status_code = login_response.status_code
        json = login_response.json
        self.assertEqual(status_code, 200)
        self.assertIn("access_token", json)
        self.assertIn("refresh_token", json)

    def test_get_all_recipes(self):
        """Test get all recipes"""
        response = self.client.get("/recipe/recipes")
        status_code = response.status_code

        self.assertEqual(status_code, 200)

    def test_get_recipe(self):
        """Test get a recipe by ID"""
        response = self.client.get("/recipe/recipes/1")
        status_code = response.status_code

        self.assertEqual(status_code, 404)

    def test_create_recipe(self):
        """Test create a recipe"""
        recipe_data = {
            "title": "test_recipe",
            "description": "test_description",
        }
        response = self.client.post(
            "/recipe/recipes",
            json=recipe_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        status_code = response.status_code
        json = response.json
        self.assertEqual(status_code, 201)
        self.assertEqual(json["title"], recipe_data["title"])
        self.assertEqual(json["description"], recipe_data["description"])

    def test_update_recipe(self):
        """Test update a recipe"""
        recipe_data = {
            "title": "test_recipe",
            "description": "test_description",
        }
        response = self.client.post(
            "/recipe/recipes",
            json=recipe_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        recipe_id = response.json["id"]
        updated_recipe_data = {
            "title": "updated_title",
            "description": "updated_description",
        }
        response = self.client.put(
            f"/recipe/recipes/{recipe_id}",
            json=updated_recipe_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        status_code = response.status_code
        json = response.json
        self.assertEqual(status_code, 200)
        self.assertEqual(json["title"], updated_recipe_data["title"])
        self.assertEqual(json["description"], updated_recipe_data["description"])

    def test_delete_recipe(self):
        """Test delete a recipe"""

        recipe_data = {
            "title": "test_recipe",
            "description": "test_description",
        }
        response = self.client.post(
            "/recipe/recipes",
            json=recipe_data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        recipe_id = response.json["id"]
        response = self.client.delete(
            f"/recipe/recipes/{recipe_id}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        status_code = response.status_code
        self.assertEqual(status_code, 204)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
