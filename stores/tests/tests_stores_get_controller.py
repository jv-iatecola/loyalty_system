from accounts.repository.accounts_repository import AccountsRepository
from common.mock.jwt_token_mock import jwt_token
from django.test import TestCase, Client
from unittest.mock import patch
import json

@patch("middleware.middleware.AccountsRepository", spec=AccountsRepository)
@patch("stores.repository.stores_repository.list")
class TestsStoresGetController(TestCase):

    def setUp(self):
        self.client = Client(headers={"Authorization": jwt_token})

        self.user = {
            "email": "test_user@test.com",
            "password": "12345",
            "username": "Vouchers_Create_Tester",
            "email_is_validated": True
        }

    def create_mock_user(self, mock_repository):
        mock_user = mock_repository.__class__().create(
            email="test_user@test.com",
            password="12345",
            username="Store_Create_Tester",
            email_is_validated=True
        )
        mock_repository.get_by_email.return_value = mock_user
        return mock_user

    def test_stores_get(self, mock_list, mock_repository):
        self.create_mock_user(mock_repository)
        mock_list.return_value = ["Stores List"]

        response = self.client.get("/stores")
        response_content = json.loads(response.content)
        
        self.assertEqual(response_content["data"][0], "Stores List")
        self.assertEqual(response.status_code, 200)

    def test_stores_get_error(self, mock_list, mock_repository):
        mock_user = self.create_mock_user(mock_repository)
        mock_list.side_effect = Exception("Error")

        response = self.client.get("/stores")
        response_content = json.loads(response.content)

        self.assertEqual(response_content["message"], f"Failed to find Stores for the user {mock_user}.")
        self.assertEqual(response.status_code, 400)
