from flask import Flask

from . import utils

app = Flask(__name__)

@app.route("/lunch_command", methods=['POST'])
@utils.validate_request
def hello():
    return "Hello there!"
