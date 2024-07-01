from accounts.repository.accounts_repository import AccountsRepository
from common.mock.jwt_token_mock import jwt_token
from django.test import TestCase, Client
from unittest.mock import patch


@patch("middleware.middleware.AccountsRepository", spec=AccountsRepository)
class TestsResendEmailController(TestCase):
        
    def setUp(self):
        self.client = Client(headers={"authorization": jwt_token})

        self.user = {
            "email":"test_user@test.com",
            "password":"12345",
            "username":"ResendEmail_Tester",
            "email_is_validated": False
        }

        self.validated_user = {
            "email":"validated_test_user@test.com",
            "password":"12345",
            "username":"ResendEmailValid_Tester",
            "email_is_validated":True
        }

    def create_mock_user(self, mock_repository, **kwargs):
        mock_user = mock_repository.__class__().create(
            email=kwargs.pop("email"),
            password=kwargs.pop("password"),
            username=kwargs.pop("username"),
            email_is_validated=kwargs.pop("email_is_validated")
        )
        mock_repository.get_by_email.return_value = mock_user
        return mock_user


    def test_return_user_already_validated_error(self, mock_middleware_repository):
        mock_user = self.create_mock_user(mock_middleware_repository, **self.validated_user)

        response = self.client.get("/accounts/resend_email")

        self.assertEqual(response.json().get("message"), f"Invalid Request Error: User '{mock_user.id}' Already Validated.")
        self.assertEqual(response.status_code, 400)

    @patch("accounts.controller.accounts_resend_email_controller.hash_data")
    def test_return_failed_to_hash_data(self, mock_hash_data, mock_middleware_repository):
        self.create_mock_user(mock_middleware_repository, **self.user)
        mock_hash_data.return_value = False

        response = self.client.get("/accounts/resend_email")

        self.assertEqual(response.json().get("message"), "Account created successfully, but failed to send a validation email.")
        self.assertEqual(response.status_code, 500)
    
    @patch("accounts.controller.accounts_resend_email_controller.send_email")
    def test_return_failed_to_send_validation_email(self, mock_send_email, mock_middleware_repository):
        self.create_mock_user(mock_middleware_repository, **self.user)
        mock_send_email.return_value = {"error": True}

        response = self.client.get("/accounts/resend_email")

        self.assertEqual(response.json().get("message"), "Account created successfully, but failed to send a validation email.")
        self.assertEqual(response.status_code, 500)

    @patch("accounts.controller.accounts_resend_email_controller.send_email")
    def test_return_account_created_succesfully(self, mock_send_email, mock_middleware_repository):
        mock_user = self.create_mock_user(mock_middleware_repository, **self.user)
        mock_send_email.return_value = {"error": False}

        response = self.client.get("/accounts/resend_email")

        self.assertEqual(response.json().get("message"), f"Validation email sent successfully to '{mock_user.email}'.")
        self.assertEqual(response.status_code, 200)
