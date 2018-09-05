from threading import Thread
import requests

from ..lunchhr.pages.exceptions import AuthenticationFailureException
from . import utils

def authenticate(lunchhrProxy, user_id, credentials, response_url):
    try:
        lunchhrProxy.authenticate_user_and_create_pages(user_id, credentials)

        message = utils.create_slack_message('Authentication successfull!')

        requests.post(response_url, json=message)
    except AuthenticationFailureException:
        message = utils.create_slack_message('Authentication failure!')

        requests.post(response_url, json=message)

def handle_authenticate(lunchhrProxy, tokens, user_id, response_url):
    '''
    Handles authenticate sub command.
    '''

    try:
        email, password = tokens

        credentials = {
            'email': email,
            'password': password
        }

        thr = Thread(target=authenticate, args=[lunchhrProxy, user_id, credentials, response_url])
        thr.start()

        return "Trying to authenticate you."
    except ValueError:
        return "Please specify an email and a password!"
