from accounts.repository.accounts_repository import AccountsRepository
from common.mock.jwt_token_mock import jwt_token
from django.test import TestCase, Client
from unittest.mock import patch

@patch("middleware.middleware.AccountsRepository", spec=AccountsRepository)
class TestPatchController(TestCase):

    def setUp(self):
        self.client = Client(headers={"authorization": jwt_token})
        self.email = "test_user@test.com"
        self.password = "12345"
        self.old_username = "OldTester"
        self.new_username = "NewTester"

    def create_mock_user(self, mock_repository):
        mock_user = mock_repository.__class__().create(
            email=self.email,
            password=self.password,
            username=self.old_username,
            email_is_validated=True
        )
        mock_repository.get_by_email.return_value = mock_user
        return mock_user

    def test_return_new_username_param_is_required(self, mock_repository):
        response = self.client.patch("/accounts/patch")

        self.assertEqual(response.json().get("message"), "Invalid Request Error: Parameter 'new_username' is required.")
        self.assertEqual(response.status_code, 400)

    def test_return_username_already_provided(self, mock_repository):
        self.create_mock_user(mock_repository)

        response = self.client.patch("/accounts/patch", QUERY_STRING=f"new_username={self.old_username}", content_type='application/json')

        self.assertEqual(response.json().get("message"), "Invalid Request Error: Username 'OldTester' already provided for this account.")
        self.assertEqual(response.status_code, 400)

    def test_username_patched(self, mock_repository):
        self.create_mock_user(mock_repository)

        response = self.client.patch("/accounts/patch", QUERY_STRING=f"new_username={self.new_username}", content_type='application/json')

        self.assertEqual(response.json().get("message"), "Username updated successfully!")
        self.assertEqual(response.status_code, 200)
