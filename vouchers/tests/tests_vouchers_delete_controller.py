from accounts.repository.accounts_repository import AccountsRepository
from vouchers.repository.vouchers_repository import VoucherRepository
from stores.repository.stores_repository import StoresRepository
from common.mock.jwt_token_mock import jwt_token
from django.test import TestCase, Client
from unittest.mock import Mock, patch

@patch("middleware.middleware.AccountsRepository", spec=AccountsRepository)
class TestsVouchersDeleteController(TestCase):

    def setUp(self):
        self.client = Client(headers={"authorization": jwt_token})

    def create_mock_user(self, mock_repository):
        mock_user = mock_repository.__class__().create(
            email="test_user@test.com",
            password="12345",
            username="Vouchers_Delete_Tester",
            email_is_validated=True
        )
        mock_repository.get_by_email.return_value = mock_user
        return mock_user
    
    def create_mock_store(self, mock_user):
        mock_instance = Mock(spec=StoresRepository).__class__()
        mock_store = mock_instance.create(
            store_name="Test_Store",
            accounts=mock_user
        )
        return mock_store 
    
    def create_mock_voucher(self, mock_voucher_repository, mock_user, mock_store):
        mock_voucher = mock_voucher_repository.__class__().create(
            accounts=mock_user,
            stores=mock_store
        )
        return mock_voucher
    
    def delete_mock_voucher(self, mock_voucher_repository, mock_user_id=None, mock_voucher_id=None):
        mock_instance = mock_voucher_repository.__class__()
        found_vouchers = None

        if mock_user_id:
            found_vouchers = mock_instance.delete_all_vouchers(mock_user_id)
            mock_voucher_repository.delete_all_vouchers.return_value = found_vouchers

        if mock_voucher_id:
            found_vouchers = mock_instance.delete_by_voucher_id(**{'id':[mock_voucher_id]})
            mock_voucher_repository.delete_by_voucher_id.return_value = found_vouchers

        return found_vouchers


    def test_return_voucher_not_found(self, mock_middleware_repository):
        mock_user = self.create_mock_user(mock_middleware_repository)
        self.create_mock_store(mock_user)

        response = self.client.delete("/vouchers", QUERY_STRING=f"id={mock_user.id}")

        self.assertEqual(response.json().get("message"), f"Failed to find vouchers for the id '{mock_user.id}'.")
        self.assertEqual(response.status_code, 400)

    @patch("vouchers.controller.vouchers_delete_controller.VoucherRepository", spec=VoucherRepository)
    def test_return_delete_all_vouchers(self, mock_voucher_repository, mock_middleware_repository):
        mock_user = self.create_mock_user(mock_middleware_repository)
        mock_store = self.create_mock_store(mock_user)
        self.create_mock_voucher(mock_voucher_repository, mock_user, mock_store)
        self.delete_mock_voucher(mock_voucher_repository, mock_user_id=mock_user.id)
        
        response = self.client.delete("/vouchers")

        self.assertEqual(response.json().get("message"), f"Deleted '1' voucher(s) for user '{mock_user.id}' at vouchers_delete_controller.")
        self.assertEqual(response.status_code, 200)

    @patch("vouchers.controller.vouchers_delete_controller.VoucherRepository", spec=VoucherRepository)
    def test_return_delete_by_voucher_id(self, mock_voucher_repository, mock_middleware_repository):
        mock_user = self.create_mock_user(mock_middleware_repository)
        mock_store = self.create_mock_store(mock_user)
        mock_voucher = self.create_mock_voucher(mock_voucher_repository, mock_user, mock_store)
        self.delete_mock_voucher(mock_voucher_repository, mock_voucher_id=mock_voucher.id)
        
        response = self.client.delete("/vouchers", QUERY_STRING=f"id={mock_voucher.id}")

        self.assertEqual(response.json().get("message"), f"Voucher '{mock_voucher.id}' deleted successfully.")
        self.assertEqual(response.status_code, 200)
