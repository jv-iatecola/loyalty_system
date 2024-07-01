from provider.mail_provider import send_email
from unittest.mock import Mock, patch
from django.test import TestCase


class TestMailProvider(TestCase):

    @patch("provider.mail_provider.requests.post")
    def test_mail_provider(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response

        result = send_email({
            "sendto": "test_provider@test.com",
            "name": "provider_tester",
            "body": (
                "Please click on the link below to validate your new "
                "Django's Loyalty System Account: \n"
                "http://localhost:8000/accounts/validate/hashed_data."
            )
        })

        self.assertEqual(result.get("status"), "success")
