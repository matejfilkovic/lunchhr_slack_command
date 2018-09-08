import os
import hashlib
import hmac
import time
from functools import wraps

from flask import request, Response

SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')

def validate_request(func):
    '''
    Decorator that validates incoming requests. If an incoming request
    in not comming from Slack, it replies with 401.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not validate_slack_signature():
            return Response('Could not verify request', 401)

        return func(*args, **kwargs)

    return wrapper

def validate_slack_signature():
    try:
        timestamp = request.headers['X-Slack-Request-Timestamp']
        if abs(time.time() - int(timestamp)) > 60 * 5:
            # The request timestamp is more than five minutes from local time.
            # It could be a replay attack, so let's ignore it.
            return False

        request_body = request.get_data()
        sig_basestring = ('v0:' + timestamp + ':').encode('utf_8') + request_body
        digest = hmac.new(
            SLACK_SIGNING_SECRET.encode('utf_8'),
            msg=sig_basestring,
            digestmod=hashlib.sha256
        ).hexdigest()

        # Pull the signature and remove v0= from the begining.
        slack_signature = request.headers['X-Slack-Signature'][3:]

        return hmac.compare_digest(digest, slack_signature)
    except (KeyError, ValueError):
        # Missing Slack headers or invalid timestamp value.
        return False

def create_slack_message(text):
    return {
        'response_type': 'ephemeral',
        'text': text
    }
