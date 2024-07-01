from django.test import TestCase, Client
from common.utils import jwt_decoder
from unittest.mock import patch
import json

@patch("accounts.controller.accounts_login_controller.AccountsRepository")
class TestLoginController(TestCase):
    client = Client()

    user = {
        "email": "test@gmail.com",
        "password": "12345",
        "username": "create_test_user"
    }

    invalid_fields_user = {
        "emayl": "test@gmail.com",
        "password": "12345",
        "username": "create_test_user"
    }


    def test_return_invalid_json_error(self, mock_repository):
        response = self.client.post("/accounts/login")

        self.assertEqual(response.json().get("message"), "Invalid JSON error")
        self.assertEqual(response.status_code, 400)

    def test_return_invalid_fields_error(self, mock_repository):
        response = self.client.post("/accounts/login", data=json.dumps(self.invalid_fields_user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Fields Error: Email and Password are required.")
        self.assertEqual(response.status_code, 400)

    def test_return_user_not_found_error(self, mock_repository):
        mock_repository.get_by_email.return_value = False
        
        response = self.client.post("/accounts/login", data=json.dumps(self.user), content_type="application/json")

        self.assertEqual(response.json().get("message"), f"Invalid User Error: User '{self.user.get('email')}' Not Found.")
        self.assertEqual(response.status_code, 400)

    @patch("accounts.controller.accounts_login_controller.check_password")
    def test_return_invalid_password_internal_error(self, mock_check_password, mock_repository):
        mock_check_password.side_effect = Exception("Internal Error")
        response = self.client.post("/accounts/login", data=json.dumps(self.user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Password Error: Failed due to internal error.")
        self.assertEqual(response.status_code, 500)

    def test_return_invalid_password(self, mock_repository):
        response = self.client.post("/accounts/login", data=json.dumps(self.user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid User Error: Invalid Password.")
        self.assertEqual(response.status_code, 401)

    @patch("accounts.controller.accounts_login_controller.check_password")
    def test_return_jwt_token(self, mock_check_password, mock_repository):
        mock_check_password.return_value = True

        response = self.client.post("/accounts/login", data=json.dumps(self.user), content_type="application/json")
        response_content = jwt_decoder(json.loads(response.content).get("message"))

        self.assertEqual(response_content.get("email"), self.user.get("email"))
        self.assertEqual(response.status_code, 200)
