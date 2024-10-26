import os
from dotenv import load_dotenv

# Load .env.local file
load_dotenv(dotenv_path='.env.local')

# Fetch the API keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')

# Function to check if all required API keys are present
def check_api_keys():
    required_keys = ['OPENAI_API_KEY', 'TOGETHER_API_KEY', 'ANTHROPIC_API_KEY', 'COHERE_API_KEY', 'GROQ_API_KEY', 'HUGGINGFACEHUB_API_TOKEN']
    missing_keys = [key for key in required_keys if not globals()[key]]
    return missing_keys
