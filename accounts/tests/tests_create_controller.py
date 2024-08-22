from accounts.repository.accounts_repository import AccountsRepository
from django.test import TestCase, Client
from common.utils import jwt_decoder
from unittest.mock import patch
import json


@patch("accounts.controller.accounts_create_controller.AccountsRepository", spec=AccountsRepository)
class TestsCreateController(TestCase):

    def setUp(self):
        self.client = Client()
        
        self.user = {
            "email": "test@gmail.com",
            "password": "P4ssw0rd!",
            "username": "create_test_user"
        }

        self.invalid_fields_user = {
            "emayl": "test@gmail.com",
            "password": "12345",
            "username": "create_test_user"
        }

        self.invalid_email_user = {
            "email": "testgmail.com",
            "password": "12345",
            "username": "create_test_user"
        }

        self.invalid_username_user = {
            "email": "test@gmail.com",
            "password": "P4ssw0rd!",
            "username": ""
        }

    def create_mock_user(self, mock_repository):
        mock_user = mock_repository.__class__().create(
            email="test@user.com",
            password="12345",
            username="Create_Tester"
        )
        mock_repository.create.return_value = mock_user
        return mock_user


    def test_return_invalid_json_error(self, mock_repository):
        response = self.client.post("/accounts/create")

        self.assertEqual(response.json().get("message"), "Invalid JSON error")
        self.assertEqual(response.status_code, 400)

    def test_return_invalid_fields_error(self, mock_repository):
        response = self.client.post("/accounts/create", data=json.dumps(self.invalid_fields_user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Fields Error: Email, Password and Username are required.")
        self.assertEqual(response.status_code, 400)

    def test_return_invalid_email_error(self, mock_repository):
        response = self.client.post("/accounts/create", data=json.dumps(self.invalid_email_user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Email Error: Enter a valid email address")
        self.assertEqual(response.status_code, 400)

    def test_return_invalid_user_error(self, mock_repository):
        mock_repository.get_by_email.return_value = True
        
        response = self.client.post("/accounts/create", data=json.dumps(self.user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid User Error: User 'test@gmail.com' already exists.")
        self.assertEqual(response.status_code, 400)

    def test_return_invalid_username_error(self, mock_repository):
        mock_repository.get_by_email.return_value = False

        response = self.client.post("/accounts/create", data=json.dumps(self.invalid_username_user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Username Error: Enter a valid username.")
        self.assertEqual(response.status_code, 400)

    @patch("accounts.controller.accounts_create_controller.make_password")
    def test_return_invalid_password_error(self, mock_make_password, mock_repository):
        mock_make_password.side_effect = Exception("Password Exception")
        mock_repository.get_by_email.return_value = False

        response = self.client.post("/accounts/create", data=json.dumps(self.user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Password Error: Enter a valid password.")
        self.assertEqual(response.status_code, 400)

    @patch("accounts.controller.accounts_create_controller.hash_data")
    def test_return_failed_to_hash_data(self, mock_hash_data, mock_repository):
        mock_hash_data.return_value = False
        mock_repository.get_by_email.return_value = False

        response = self.client.post("/accounts/create", data=json.dumps(self.user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Account created successfully, but failed to send a validation email.")
        self.assertEqual(response.status_code, 500)

    @patch("accounts.controller.accounts_create_controller.send_email")
    def test_return_failed_to_send_validation_email(self, mock_send_email, mock_repository):
        self.create_mock_user(mock_repository)
        mock_send_email.return_value = {"error": True}
        mock_repository.get_by_email.return_value = False

        response = self.client.post("/accounts/create", data=json.dumps(self.user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Account created successfully, but failed to send a validation email.")
        self.assertEqual(response.status_code, 500)

    @patch("accounts.controller.accounts_create_controller.send_email")
    def test_return_user_created_successfully(self, mock_send_email, mock_repository):
        self.create_mock_user(mock_repository)
        mock_send_email.return_value = {"error": False}
        mock_repository.get_by_email.return_value = False

        response = self.client.post("/accounts/create", data=json.dumps(self.user), content_type="application/json")
        response_content = jwt_decoder(json.loads(response.content).get("message"))

        self.assertEqual(response_content.get("email"), self.user.get("email"))
        self.assertEqual(self.user.get("email"), response_content.get("email"))
        self.assertEqual(self.user.get("username"), "create_test_user")
        self.assertEqual(response.status_code, 201)
