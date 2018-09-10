import unittest
from unittest import mock

from lunchhr_slack_command.slack.lunchhr_proxy import LunchhrProxy
from lunchhr_slack_command.slack import overview, utils

class TestHandleOverview(unittest.TestCase):
    def setUp(self):
        self.lunchhr_proxy_mock = mock.create_autospec(
            LunchhrProxy,
            spec_set=True,
            instance=True
        )

    def test_user_not_authenticated(self):
        '''
        Only users authenticated to lunchhr should
        be able to use overview subcommand.
        '''
        self.lunchhr_proxy_mock.is_user_authenticated.return_value = False

        result = overview.handle_overview(
            self.lunchhr_proxy_mock,
            [],
            'some_id',
            'https://response-url.com'
        )

        self.assertEqual(result, utils.PLEASE_AUTHENTICATE_MESSAGE)

    @mock.patch('lunchhr_slack_command.slack.overview.Thread')
    def test_user_authenticated(self, ThreadMock):
        self.lunchhr_proxy_mock.is_user_authenticated.return_value = True

        result = overview.handle_overview(
            self.lunchhr_proxy_mock,
            [],
            'some_id',
            'https://response-url.com'
        )

        self.assertTrue(ThreadMock.called)
        self.assertEqual(result, overview.FETCHING_ORDERS_MESSAGE)
