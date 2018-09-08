import unittest
from unittest import mock

from lunchhr_slack_command.slack.lunchhr_proxy import LunchhrProxy
from lunchhr_slack_command.slack import authenticate

class TestHandleAuthenticate(unittest.TestCase):
    def setUp(self):
        self.lunchhr_proxy_mock = mock.create_autospec(
            LunchhrProxy,
            spec_set=True,
            instance=True
        )

    def test_missing_credentials(self):
        result = authenticate.handle_authenticate(
            self.lunchhr_proxy_mock,
            ['some@email.com'],
            'some_id',
            'https://response-url.com'
        )

        self.assertEqual(result, authenticate.INVALID_EMAIL_OR_PASSWORD_MESSAGE)

    @mock.patch('lunchhr_slack_command.slack.authenticate.Thread')
    def test_valid_credentials(self, MockThread):
        '''
        When credentials are passed it should create a Thread
        and try to authenticate.
        '''

        result = authenticate.handle_authenticate(
            self.lunchhr_proxy_mock,
            ['some@email.com', 'somepassword'],
            'some_id',
            'https://response-url.com'
        )

        self.assertTrue(MockThread.called)
        self.assertTrue(result == authenticate.TRYING_TO_AUTHENTICATE_MESSAGE)
