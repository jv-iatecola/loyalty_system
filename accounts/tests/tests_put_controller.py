from middleware.middleware import AccountsRepository
from common.mock.jwt_token_mock import jwt_token
from django.test import TestCase, Client
from unittest.mock import patch
import json


@patch("middleware.middleware.AccountsRepository", spec=AccountsRepository)
@patch("accounts.controller.accounts_put_controller.AccountsRepository", spec=AccountsRepository)
class TestPutController(TestCase):

    def setUp(self):
        self.client = Client(headers={"authorization": jwt_token})

        self.email = "test_user@test.com"
        self.password = "12345"
        self.username = "Put_Tester"

        self.user = {
            "email": "test@gmail.com",
            "password": "P4ssw0rd1",
            "username": "Put_Tester2"
        }

        self.invalid_user = {
            "email": "test_test.com",
            "password": "12345",
            "username": "Invalid_Put_Tester"
        }

        self.invalid_user2 = {
            "username": "In"
        }

        self.invalid_user3 = {
            "username": "¬¬¬"
        }

    def create_mock_user(self, mock_repository):
        mock_user = mock_repository.__class__().create(
            email=self.email,
            password=self.password,
            username=self.username,
            email_is_validated=True
        )
        mock_repository.get_by_email.return_value = mock_user
        return mock_user


    def test_return_invalid_json_error(self, mock_controller_repository, mock_repository):
        response = self.client.put("/accounts/put")

        self.assertEqual(response.json().get("message"), "Invalid JSON error")
        self.assertEqual(response.status_code, 400)

    def test_return_invalid_email_format_error(self, mock_controller_repository, mock_repository):
        self.create_mock_user(mock_controller_repository)

        response = self.client.put("/accounts/put", data=json.dumps(self.invalid_user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Email Error: Email 'test_test.com' is not valid.")
        self.assertEqual(response.status_code, 400)

    def test_return_invalid_email_error(self, mock_controller_repository, mock_repository):
        self.create_mock_user(mock_controller_repository)
        
        response = self.client.put("/accounts/put", data=json.dumps(self.user), content_type="application/json")

        self.assertEqual(response.json().get("message"), f"Invalid Email Error: Email '{self.user.get('email')}' is not valid.")
        self.assertEqual(response.status_code, 400)

    def test_return_invalid_email_error2(self, mock_controller_repository, mock_repository):
        self.create_mock_user(mock_controller_repository)
        mock_controller_repository.get_by_email.return_value = False
        
        response = self.client.put("/accounts/put", data=json.dumps(self.invalid_user), content_type="application/json")

        self.assertEqual(response.json().get("message"), f"Invalid Email Error: Enter a valid email address.")
        self.assertEqual(response.status_code, 400)

    def test_return_invalid_username(self, mock_controller_repository, mock_repository):
        self.create_mock_user(mock_controller_repository)
        mock_controller_repository.get_by_email.return_value = False
        
        response = self.client.put("/accounts/put", data=json.dumps(self.invalid_user2), content_type="application/json")

        self.assertEqual(response.json().get("message"), f"Invalid Username Error: Enter a valid username.")
        self.assertEqual(response.status_code, 400)

    def test_return_invalid_username2(self, mock_controller_repository, mock_repository):
        self.create_mock_user(mock_controller_repository)
        mock_controller_repository.get_by_email.return_value = False
        
        response = self.client.put("/accounts/put", data=json.dumps(self.invalid_user3), content_type="application/json")

        self.assertEqual(response.json().get("message"), f"Invalid Username Error: Enter a valid username.")
        self.assertEqual(response.status_code, 400)

    @patch("accounts.controller.accounts_put_controller.make_password", side_effect=Exception("Hashing Error"))
    def test_failed_to_hash_password(self, mock_make_password, mock_controller_repository, mock_repository):
        self.create_mock_user(mock_repository)
        mock_controller_repository.get_by_email.return_value = False

        response = self.client.put("/accounts/put", data=json.dumps(self.user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Password Error: Enter a valid password.")
        self.assertEqual(response.status_code, 400)

    def test_return_user_updated_successfully(self, mock_controller_repository, mock_repository):
        self.create_mock_user(mock_repository)
        mock_controller_repository.get_by_email.return_value = False

        response = self.client.put("/accounts/put", data=json.dumps(self.user), content_type="application/json")

        self.assertEqual(response.json().get("message"), "User updated successfully!")
        self.assertEqual(response.status_code, 200)
