from accounts.repository.accounts_repository import AccountsRepository
from common.mock.jwt_token_mock import jwt_token
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
import json

@patch("accounts.repository.accounts_repository.Accounts.save")
@patch("middleware.middleware.AccountsRepository", spec=AccountsRepository)
class TestVerifyController(TestCase):

    def setUp(self):
        self.client = Client(headers={"Authorization": jwt_token})

    def create_user(self, mock_repository):
        mock_user = AccountsRepository.create(
            email="test_user@test.com",
            password="12345",
            username="Verify_Tester",
            email_is_validated=True
        )
        mock_repository.get_by_email.return_value = mock_user
        return mock_user

    def test_return_account_already_validated(self, mock_repository, mock_save):
        found_user = self.create_user(mock_repository)
        response = self.client.get(reverse("verify"))
        response_content = json.loads(response.content)

        self.assertEqual(response_content["message"], f"Account '{found_user.id}' already validated.")
        self.assertEqual(response.status_code, 200)
