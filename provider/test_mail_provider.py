from provider.mail_provider import send_email
from unittest.mock import Mock, patch
from django.test import TestCase


class TestMailProvider(TestCase):

    @patch("provider.mail_provider.smtplib")
    def test_mail_sent_successfully(self, mock_smtplib):
        mock_response = Mock()
        mock_smtplib.login = mock_response
        mock_smtplib.send_email.return_value = mock_response

        result = send_email({
            "send_to": "test_provider@test.com",
            "name": "provider_tester",
            "body": (
                "Please click on the link below to validate your new "
                "Django's Loyalty System Account: \n"
                "http://localhost:8000/accounts/validate/hashed_data."
            )
        })

        self.assertEqual(result, True)

    @patch("provider.mail_provider.smtplib.SMTP_SSL", side_effect=Exception())
    def test_failed_to_send_mail(self, mock_smtplib):
        result = send_email({
            "send_to": "test_provider@test.com",
            "name": "provider_tester",
            "body": (
                "Please click on the link below to validate your new "
                "Django's Loyalty System Account: \n"
                "http://localhost:8000/accounts/validate/hashed_data."
            )
        })

        self.assertEqual(result, False)
