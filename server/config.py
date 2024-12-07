import os
from dotenv import load_dotenv

# Load the env variables from the .env file
load_dotenv()


# API_KEY is used to authenticate the client
API_KEY = os.getenv("API_KEY", "default_api_key")

# This is used to simulate the delay which corresponds to the time taken for the video to generate
SIMULATED_DELAY = int(os.getenv("DELAY", 10))
