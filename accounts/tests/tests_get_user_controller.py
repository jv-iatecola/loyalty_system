from accounts.repository.accounts_repository import AccountsRepository
from common.mock.jwt_token_mock import jwt_token
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

@patch("accounts.repository.accounts_repository.Accounts.save")
@patch("middleware.middleware.AccountsRepository", spec=AccountsRepository)
class TestsGetUserController(TestCase):

    def setUp(self):
        self.client = Client(headers={"Authorization": jwt_token})

    def create_user(self, mock_repository):
        mock_user = AccountsRepository.create(
            email="test_user@test.com",
            password="12345",
            username="Vouchers_Create_Tester",
            email_is_validated=True
        )
        mock_repository.get_by_email.return_value = mock_user
        return mock_user

    def test_return_user_object(self, mock_repository, mock_save):
        mock_user = self.create_user(mock_repository)

        response = self.client.get(reverse("get_user"))
        
        self.assertEqual(response.json(), {"data": {"id": mock_user.id, "username": mock_user.username, "email": mock_user.email}})
        self.assertEqual(response.status_code, 200)
