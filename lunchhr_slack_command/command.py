from flask import Flask

app = Flask(__name__)

# An example of one of your Flask app's routes
@app.route("/test")
def hello():
    return "Hello there!"
