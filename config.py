import os
from dotenv import load_dotenv

load_dotenv()

username = os.environ.get("REDDIT_USERNAME")
password = os.environ.get("REDDIT_PASSSWORD")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")