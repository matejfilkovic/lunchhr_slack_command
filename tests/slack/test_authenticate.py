import unittest
from unittest import mock

from lunchhr_slack_command.slack.lunchhr_proxy import LunchhrProxy
from lunchhr_slack_command.slack import authenticate

class TestHandleAuthenticate(unittest.TestCase):
    def test_missing_credentials(self):
        lunchhr_proxy_mock = mock.create_autospec(LunchhrProxy, instance=True)

        result = authenticate.handle_authenticate(
            lunchhr_proxy_mock,
            ['some@email.com'],
            'some_id',
            'https://response-url.com'
        )

        self.assertEqual(result, authenticate.INVALID_EMAIL_OR_PASSWORD_MESSAGE)
