import json
from accounts.repository.accounts_repository import AccountsRepository
from stores.repository.stores_repository import StoresRepository
from common.mock.jwt_token_mock import jwt_token
from django.test import TestCase, Client
from unittest.mock import patch


@patch("stores.controller.stores_create_controller.StoresRepository", spec=StoresRepository)
@patch("middleware.middleware.AccountsRepository", spec=AccountsRepository)
class TestsStoreCreateController(TestCase):
    
    def setUp(self):
        self.client = Client(headers={"authorization": jwt_token})

        self.store_name_param = {"store_name": "Test_Store"}
        self.new_store_name_param = {"store_name": "New_Acai_Store"}
        self.invalid_store_name_param = {"story_name": "New_Acai_Store"}

    def create_mock_user(self, mock_repository):
        mock_user = mock_repository.__class__().create(
            email="test_user@test.com",
            password="12345",
            username="Store_Create_Tester",
            email_is_validated=True
        )
        mock_repository.get_by_email.return_value = mock_user
        return mock_user
    
    def create_mock_store(self, mock_store_repository, mock_user):
        mock_store = mock_store_repository.__class__().create(
            store_name="Test_Store",
            accounts=mock_user
        )
        return mock_store
    
    def get_by_store_name(self, mock_store_repository, store_name):
        found_store = mock_store_repository.__class__().get_by_store_name(store_name)
        mock_store_repository.get_by_store_name.return_value = found_store

        return found_store


    def test_return_invalid_json_error(self, mock_controller_repository, mock_stores_repository):
        response = self.client.post("/stores")

        self.assertEqual(response.json().get("message"), "Invalid JSON error")
        self.assertEqual(response.status_code, 400)

    def test_return_invalid_store_name_error(self, mock_controller_repository, mock_stores_repository):
        self.create_mock_user(mock_controller_repository)

        response = self.client.post("/stores", data=json.dumps(self.invalid_store_name_param), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Fields Error: \"store_name\" Not Found.")
        self.assertEqual(response.status_code, 400)

    def test_return_error_store_already_exists(self, mock_controller_repository, mock_stores_repository):
        mock_user = self.create_mock_user(mock_controller_repository)
        self.create_mock_store(mock_stores_repository, mock_user)
        self.get_by_store_name(mock_stores_repository, self.store_name_param.get("store_name"))

        response = self.client.post("/stores", data=json.dumps(self.store_name_param), content_type="application/json")

        self.assertEqual(response.json().get("message"), "Invalid Store Error: Store Already Exists.")
        self.assertEqual(response.status_code, 400)

    def test_return_stores_table(self, mock_controller_repository, mock_stores_repository):
        mock_user = self.create_mock_user(mock_controller_repository)
        self.get_by_store_name(mock_stores_repository, self.new_store_name_param.get("store_name"))
        mock_store = self.create_mock_store(mock_stores_repository, mock_user)
        mock_stores_repository.create.return_value = mock_store

        response = self.client.post("/stores", data=json.dumps(self.new_store_name_param), content_type="application/json")

        self.assertEqual(response.json().get("message"), f"Store '{mock_store.store_name}' created Successfully!")
        self.assertEqual(response.status_code, 200)
