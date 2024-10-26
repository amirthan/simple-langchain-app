import os
from dotenv import load_dotenv

# Load .env.local file
load_dotenv(dotenv_path='.env.local')

# Fetch the API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')