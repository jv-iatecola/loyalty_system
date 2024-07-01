from accounts.repository.accounts_repository import AccountsRepository
from django.test import TestCase, Client
from datetime import datetime, timedelta
from common.utils import hash_data
from unittest.mock import patch
from ast import literal_eval

@patch("accounts.controller.accounts_validate_controller.AccountsRepository", spec=AccountsRepository)
class TestValidateController(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = {
            "email": "test_user@test.com",
            "password": "12345",
            "username": "Validate_Tester",
            "email_is_validated": False
        }

        self.validated_user = {
            "email": "validated_test_user@test.com",
            "password": "12345",
            "username": "Validated_Tester",
            "email_is_validated": True
        }

    def create_mock_user(self, mock_repository, **kwargs):
        mock_user = mock_repository.__class__().create(
            email=kwargs.pop("email"),
            password=kwargs.pop("password"),
            username=kwargs.pop("username"),
            email_is_validated=kwargs.pop("email_is_validated")
        )
        return mock_user


    def test_return_invalid_request_error(self, mock_repository):
        response = self.client.get("/accounts/validate/invalidHash")

        self.assertEqual(response.json().get("message"), "Invalid Request Error")
        self.assertEqual(response.status_code, 500)

    def test_return_invalid_user_error(self, mock_repository):
        mock_user = self.create_mock_user(mock_repository, **self.user)
        mock_repository.__class__().get_by_id("Invalid_id")
        mock_repository.get_by_id.return_value = False

        response = self.client.get(f"/accounts/validate/{hash_data(mock_user.id)}")

        self.assertEqual(response.json().get("message"), f"Invalid User Error: User '{mock_user.id}' not found.")
        self.assertEqual(response.status_code, 400)
        
    def test_return_user_already_validated_error(self, mock_repository):
        mock_user = self.create_mock_user(mock_repository, **self.validated_user)
        mock_repository.__class__().get_by_id(mock_user.id)
        
        response = self.client.get(f"/accounts/validate/{hash_data(mock_user.id)}")

        self.assertEqual(response.json().get("message"), f"Invalid Request Error: User '{mock_user.id}' Already Validated.")
        self.assertEqual(response.status_code, 400)

    @patch("accounts.controller.accounts_validate_controller.literal_eval", spec=literal_eval)
    def test_return_invalid_date_parameter_error(self, mock_literal_eval, mock_repository):
        mock_user = self.create_mock_user(mock_repository, **self.user)
        invalid_exp = (datetime.now() - timedelta(minutes=15)).time()
        mock_literal_eval.return_value = {'id': mock_user.id, 'exp': str(invalid_exp)}
        mock_repository.get_by_id.return_value = mock_user

        response = self.client.get(f"/accounts/validate/{hash_data(mock_user.id)}")

        self.assertEqual(response.json().get("message"), f"Invalid Date Parameter Error: Date '{invalid_exp}' has expired.")
        self.assertEqual(response.status_code, 400)

    def test_return_account_validated_successfully(self, mock_repository):
        mock_user = self.create_mock_user(mock_repository, **self.user)
        mock_repository.get_by_id.return_value = mock_user

        response = self.client.get(f"/accounts/validate/{hash_data(mock_user.id)}")

        self.assertEqual(response.json().get("message"), "Your account was validated successfully!!!")
        self.assertEqual(response.status_code, 200)
