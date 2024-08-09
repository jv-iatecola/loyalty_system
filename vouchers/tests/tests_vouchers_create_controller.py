from accounts.repository.accounts_repository import AccountsRepository
from stores.repository.stores_repository import StoresRepository
from common.mock.jwt_token_mock import jwt_token
from django.test import TestCase, Client
from unittest.mock import patch
import json


@patch("middleware.middleware.AccountsRepository", spec=AccountsRepository)
class TestsVoucherCreateController(TestCase):

    def setUp(self):
        self.client = Client(headers={"authorization": jwt_token})

        self.user = {
            "email": "test_user@test.com",
            "password": "12345",
            "username": "Vouchers_Create_Tester",
            "email_is_validated": True
        }

        self.second_user = {
            "email": "test_user2@test.com",
            "password": "12345",
            "username": "Vouchers_Create_Tester2",
            "email_is_validated": True
        }

    def create_mock_user(self, mock_repository):
        mock_user = mock_repository.__class__().create(
            email="test_user@test.com",
            password="12345",
            username="Vouchers_Create_Tester",
            email_is_validated=True
        )
        mock_repository.get_by_email.return_value = mock_user
        return mock_user
    
    def create_mock_store(self, mock_store_repository, mock_user):
        mock_store = mock_store_repository.__class__().create(
            store_name="Test_Store",
            accounts=mock_user
        )
        mock_store_repository.get_by_user_id.return_value = mock_store
        return mock_store


    def test_return_invalid_json_error(self, mock_repository):
        self.create_mock_user(mock_repository)

        response = self.client.post("/vouchers")

        self.assertEqual(response.json().get("message"), "Invalid JSON error")
        self.assertEqual(response.status_code, 400)

    def test_return_invalid_fields_error(self, mock_repository):
        self.create_mock_user(mock_repository)

        response = self.client.post("/vouchers", data=json.dumps({"emayl": self.user.get("email")}), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Fields Error: \'email\' is required.")
        self.assertEqual(response.status_code, 400)

    def test_return_store_not_found_for_user_id(self, mock_repository):
        self.create_mock_user(mock_repository)
    
        response = self.client.post("/vouchers", data=json.dumps({"email": self.user.get("email")}), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Store Error: Store Not Found.")
        self.assertEqual(response.status_code, 400)

    def test_return_store_not_found_for_store_id(self, mock_repository):
        self.create_mock_user(mock_repository)
        
        response = self.client.post("/vouchers", data=json.dumps({"email": self.user.get("email"), "store_id": "384b02c7-2af6-477d-ad4b-b3603036f45e"}), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Store Error: Store Not Found.")
        self.assertEqual(response.status_code, 400)

    @patch("vouchers.controller.vouchers_create_controller.StoresRepository", spec=StoresRepository)
    def test_return_requester_not_found(self, mock_stores_repository, mock_repository):
        mock_user = self.create_mock_user(mock_repository)
        self.create_mock_store(mock_stores_repository, mock_user)
        mock_stores_repository.__class__().get_by_user_id(mock_user.id)

        response = self.client.post("/vouchers",  data=json.dumps({"email": self.second_user.get("email")}), content_type="application/json")

        self.assertEqual(response.json().get("message"), f"Invalid User Error: Requester '{self.second_user.get('email')}' not found.")
        self.assertEqual(response.status_code, 400)

    @patch("vouchers.controller.vouchers_create_controller.StoresRepository", spec=StoresRepository)
    def test_generate_voucher(self, mock_stores_repository, mock_repository):
        mock_user = self.create_mock_user(mock_repository)
        mock_store = self.create_mock_store(mock_stores_repository, mock_user)
        mock_stores_repository.__class__().get_by_store_id(mock_store.id)

        response = self.client.post("/vouchers", data=json.dumps({"email": self.user.get("email")}), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Voucher generated successfully!")
        self.assertEqual(response.status_code, 200)
