from unittest.mock import patch
from accounts.repository.accounts_repository import AccountsRepository
from common.mock.jwt_token_mock import jwt_token
from django.test import TestCase, Client

class TestMiddleware(TestCase):
    
    def setUp(self):
        self.client = Client(headers={"authorization": jwt_token})

        self.user = {
            "email":"test_user@test.com",
            "password":"12345",
            "username":"Middleware_Tester",
            "email_is_validated": False
        }

        self.validated_user = {
            "email":"test_user@test.com",
            "password":"12345",
            "username":"Middleware_Tester",
            "email_is_validated": True
        }

    def create_mock_user(self, mock_repository, user):
        mock_user = mock_repository.__class__().create(
            email=user.get("email"),
            password=user.get("password"),
            username=user.get("username"),
            email_is_validated=user.get("email_is_validated")
        )
        return mock_user
    

    def test_return_jwt_token_not_found(self):
        client = Client()
        response = client.get("/vouchers")

        self.assertEqual(response.json().get("message"), "Invalid Token Error: Token Not Found.")
        self.assertEqual(response.status_code, 401)

    def test_return_failed_to_decode_jwt_token(self):
        client = Client(headers={"authorization": "Invalid JWT Token"})
        response = client.get("/vouchers")

        self.assertEqual(response.json().get("message"), "Invalid Token Error.")
        self.assertEqual(response.status_code, 401)

    @patch("middleware.middleware.AccountsRepository")
    def test_return_invalid_user_error(self, mock_repository):
        mock_repository.get_by_email.return_value = False
        response = self.client.get("vouchers")

        self.assertEqual(response.json().get("message"), "Invalid User Error: User 'test_user@test.com' not found.")
        self.assertEqual(response.status_code, 400)

    @patch("middleware.middleware.AccountsRepository", spec=AccountsRepository)
    def test_return_invalid_request_error(self, mock_repository):
        mock_user = self.create_mock_user(mock_repository, self.user)
        mock_repository.get_by_email.return_value = mock_user

        response = self.client.get("/vouchers")

        self.assertEqual(response.json().get("message"), "Invalid Request Error: Account Not Validated.")
        self.assertEqual(response.status_code, 401)

    @patch("middleware.middleware.AccountsRepository", spec=AccountsRepository)
    def test_return_valid_request(self, mock_repository):
        mock_user = self.create_mock_user(mock_repository, self.validated_user)
        mock_repository.get_by_email.return_value = mock_user

        response = self.client.get("/vouchers")

        self.assertEqual(response.status_code, 200)
