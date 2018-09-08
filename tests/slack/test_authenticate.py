import unittest
from unittest import mock

from lunchhr_slack_command.slack.lunchhr_proxy import LunchhrProxy
from lunchhr_slack_command.slack import authenticate, utils

from lunchhr_slack_command.lunchhr.pages.exceptions \
    import AuthenticationFailureException

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
    def test_valid_credentials(self, ThreadMock):
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

        self.assertTrue(ThreadMock.called)
        self.assertEqual(result, authenticate.TRYING_TO_AUTHENTICATE_MESSAGE)

class TestAuthenticate(unittest.TestCase):
    def setUp(self):
        self.lunchhr_proxy_mock = mock.create_autospec(
            LunchhrProxy,
            spec_set=True,
            instance=True
        )

    @mock.patch('requests.post')
    def test_authentication_failure(self, postMock):
        self.lunchhr_proxy_mock \
            .authenticate_user_and_create_pages \
            .side_effect = AuthenticationFailureException

        response_url = 'https://response-url.com'

        authenticate.authenticate(
            self.lunchhr_proxy_mock,
            'some_id',
            {
                'email': 'some@email.com',
                'password': 'somepassword'
            },
            response_url
        )

        self.assertTrue(postMock.called)

        postMock.assert_called_with(
            response_url,
            json=utils.create_slack_message(
                authenticate.AUTHENTICATION_FAILURE_MESSAGE
            )
        )

    @mock.patch('requests.post')
    def test_authentication_success(self, postMock):
        response_url = 'https://response-url.com'

        authenticate.authenticate(
            self.lunchhr_proxy_mock,
            'some_id',
            {
                'email': 'some@email.com',
                'password': 'somepassword'
            },
            response_url
        )

        self.assertTrue(postMock.called)

        postMock.assert_called_with(
            response_url,
            json=utils.create_slack_message(
                authenticate.AUTHENTICATION_SUCCESSFULL_MESSAGE
            )
        )
