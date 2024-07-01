from accounts.repository.accounts_repository import AccountsRepository
from vouchers.repository.vouchers_repository import VoucherRepository
from stores.repository.stores_repository import StoresRepository
from common.mock.jwt_token_mock import jwt_token
from django.test import TestCase, Client
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import json


@patch("vouchers.controller.vouchers_get_controller.VoucherRepository", spec=VoucherRepository)
@patch("middleware.middleware.AccountsRepository", spec=AccountsRepository)
class TestsVoucherGetController(TestCase):

    def setUp(self):
        self.today = datetime.today().strftime('%Y-%m-%d')
        self.tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.client = Client(headers={"authorization": jwt_token})

    def create_mock_user(self, mock_repository):
        mock_user = mock_repository.__class__().create(
            email="test_user@test.com",
            password="12345",
            username="Vouchers_Get_Tester",
            email_is_validated=True
        )
        mock_repository.get_by_email.return_value = mock_user
        return mock_user

    def create_mock_store(self, mock_user):
        mock_store = Mock(spec=StoresRepository).__class__().create(
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

    def get_mock_vouchers(self, mock_voucher_repository, mock_user=None, query_parameters=None):
        if mock_user and not query_parameters:
            found_vouchers = mock_voucher_repository.__class__().get_by_user_id(mock_user.id)
            mock_voucher_repository.get_by_user_id.return_value = found_vouchers

        if mock_user and query_parameters:
            found_vouchers = mock_voucher_repository.__class__().get_by_filters(**query_parameters, user_id=mock_user.id)
            mock_voucher_repository.get_by_filters.return_value = found_vouchers

        return found_vouchers

    def test_invalid_parameters(self, mock_middleware_repository, mock_voucher_repository):
        invalid_params = [
            ({"stores_id": "invalid_id"}, "Parameter 'invalid_id' in 'stores_id' is not valid."),
            ({"random_param": "?"}, "Parameter 'random_param' is not allowed, the allowed parameters are: ['from', 'until', 'stores_id', 'order_by', 'page', 'perPage']."),
            ({"from": "v0uch3r"}, "Pagination by 'from' param: 'v0uch3r' is not allowed, please insert a valid date."),
            ({"until": "v0uch3r"}, "Pagination by 'until' param: 'v0uch3r' is not allowed, please insert a valid date."),
            ({"from": "2024-01-01", "until": self.today, "order_by": "id", "page": "p4ge", "perPage": "1"}, "Pagination by 'page' param:'p4ge' is not allowed, please insert a valid number."),
            ({"from": "2024-01-01", "until": self.today, "order_by": "id", "page": "01", "perPage": "p4ge"}, "Pagination by 'perPage' param:'p4ge' is not allowed, please insert a valid number."),
            ({"from": "2024-01-01", "until": self.today, "order_by": "0rd3r", "page": "01", "perPage": "1"}, "Ordering by '0rd3r' is not allowed, the allowed assortments are: ['id', 'created_at', 'accounts_id', 'stores_id']."),
        ]

        for params, error_message in invalid_params:
            with self.subTest(params=params):
                response = self.client.get("/vouchers", params)

                self.assertEqual(response.json().get("message"), error_message)
                self.assertEqual(response.status_code, 400)

    def test_vouchers_get(self, mock_middleware_repository, mock_voucher_repository):
        mock_user = self.create_mock_user(mock_middleware_repository)
        mock_store = self.create_mock_store(mock_user)
        mock_voucher = self.create_mock_voucher(mock_voucher_repository, mock_user, mock_store)

        valid_params = [
            ({"until": [self.tomorrow]}, {"until": [self.tomorrow]}),
            ({"from": ["2024-01-01"]}, {"from": ["2024-01-01"]}),
            ({"from": ["2024-01-01"], "until": [self.tomorrow]}, {"from": ["2024-01-01"], "until": [self.tomorrow]}),
            ({"from": ["2024-01-01"], "until": [self.tomorrow], "stores_id": [mock_store.id]}, {"from": ["2024-01-01"], "until": [self.tomorrow], "stores_id": [mock_store.id]}),
            ({"from": ["2024-01-01"], "until": [self.tomorrow], "stores_id": [mock_store.id], "order_by": ["id"]}, {"from": ["2024-01-01"], "until": [self.tomorrow], "stores_id": [mock_store.id], "order_by": ["id"]}),
            ({"from": ["2024-01-01"], "until": [self.tomorrow], "stores_id": [mock_store.id], "order_by": ["id"], "page": ["01"]}, {"from": ["2024-01-01"], "until": [self.tomorrow], "stores_id": [mock_store.id], "order_by": ["id"], "page": ["01"]}),
            ({"from": ["2024-01-01"], "until": [self.tomorrow], "stores_id": [mock_store.id], "order_by": ["id"], "page": ["01"], "perPage": ["01"]}, {"from": ["2024-01-01"], "until": [self.tomorrow], "stores_id": [mock_store.id], "order_by": ["id"], "page": ["01"], "perPage": ["01"]}),
        ]

        for params, query in valid_params:
            with self.subTest(params=params):
                self.get_mock_vouchers(mock_voucher_repository, mock_user, query)
                response = self.client.get("/vouchers", params)
                response_content = json.loads(response.content)

                self.assertEqual(response_content['data']['results'][0]['id'], mock_voucher.id)
                self.assertEqual(response_content['data']['results'][0]['stores_id'], mock_store.id)
                self.assertEqual(response_content['data']['current_page'], 1)
                self.assertEqual(response_content['data']['next_page'], None)
                self.assertEqual(response.status_code, 200)

    def test_vouchers_get_without_params(self, mock_middleware_repository, mock_voucher_repository):
        mock_user = self.create_mock_user(mock_middleware_repository)
        mock_store = self.create_mock_store(mock_user)
        mock_voucher = self.create_mock_voucher(mock_voucher_repository, mock_user, mock_store)
        self.get_mock_vouchers(mock_voucher_repository, mock_user)

        response = self.client.get("/vouchers")
        response_content = json.loads(response.content)
       
        self.assertEqual(response_content['data'][0]['id'], mock_voucher.id)
        self.assertNotEqual(response_content['data'][0]['created_at'], None)
        self.assertEqual(response_content['data'][0]['accounts_id'], mock_user.id)
        self.assertEqual(response_content['data'][0]['stores_id'], mock_store.id)
        self.assertEqual(response.status_code, 200)
