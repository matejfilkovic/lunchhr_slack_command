from flask import Flask, request

from . import utils
from .lunchhr_proxy import LunchhrProxy
from .authenticate import handle_authenticate

app = Flask(__name__)

lunchhrProxy = LunchhrProxy.create()

@app.route("/lunch_command", methods=['POST'])
@utils.validate_request
def hello():
    user_id = request.form['user_id']
    command_text = request.form['text']
    response_url = request.form['response_url']
    return handle_command(user_id, command_text, response_url)


HANDLERS = {
    'authenticate': handle_authenticate
}

def handle_command(user_id, command_text, response_url):
    tokens = command_text.split(' ')
    if not tokens:
        return "authenticate <email> <password>"

    handler = HANDLERS.get(tokens[0])

    if not handler:
        return "authenticate <email> <password>"

    return handler(lunchhrProxy, tokens[1:], user_id, response_url)
