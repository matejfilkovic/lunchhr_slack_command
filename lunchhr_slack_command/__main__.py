from dotenv import load_dotenv
from .slack.app import app

load_dotenv()

app.run(port=3000)
