from common.utils import hash_data, make_pagination, uuid_validator
from django.test import TestCase
from unittest.mock import patch
import json


class TestUtils(TestCase):

    @patch("common.utils.json", spec=json)
    def test_return_hash_data_exception(self, mock_json):
        mock_json.dumps.side_effect = Exception('Hash Exception')
        response = hash_data("invalid_id")

        self.assertEqual(response, False)

    def test_return_uuid_validator_exeception(self):
        response = uuid_validator("invalid_id")

        self.assertEqual(response, False)

    def test_has_next_page(self):
        items = list(range(1, 101))
        per_page = 10
        page_number = 1

        result = make_pagination(items, per_page, page_number)

        self.assertEqual(result['current_page'], 1)
        self.assertEqual(result['per_page'], 10)
        self.assertEqual(result['max_page'], 10)
        self.assertEqual(result['next_page'], 2)
        self.assertEqual(len(result['results']), 10)
