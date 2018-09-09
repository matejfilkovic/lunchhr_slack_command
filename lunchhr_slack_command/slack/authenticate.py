from threading import Thread
import requests

from ..lunchhr.pages.exceptions import AuthenticationFailureException
from . import utils

AUTHENTICATION_SUCCESSFULL_MESSAGE = 'Authentication successfull!'
AUTHENTICATION_FAILURE_MESSAGE = 'Authentication failure!'

def authenticate(lunchhr_proxy, user_id, credentials, response_url):
    try:
        lunchhr_proxy.authenticate_user_and_create_pages(user_id, credentials)

        message = utils.create_slack_message(
            AUTHENTICATION_SUCCESSFULL_MESSAGE
        )

        requests.post(response_url, json=message)
    except AuthenticationFailureException:
        message = utils.create_slack_message(AUTHENTICATION_FAILURE_MESSAGE)

        requests.post(response_url, json=message)

INVALID_EMAIL_OR_PASSWORD_MESSAGE = 'Please specify an email and a password!'
TRYING_TO_AUTHENTICATE_MESSAGE = 'Trying to authenticate you.'

def handle_authenticate(lunchhr_proxy, tokens, user_id, response_url):
    '''
    Handles authenticate sub command.
    '''

    try:
        email, password = tokens

        credentials = {
            'email': email,
            'password': password
        }

        thr = Thread(
            target=authenticate,
            args=[lunchhr_proxy, user_id, credentials, response_url]
        )
        thr.start()

        return TRYING_TO_AUTHENTICATE_MESSAGE
    except ValueError:
        return INVALID_EMAIL_OR_PASSWORD_MESSAGE
