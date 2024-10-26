# install virtual environment
python -m venv .venv

# activate virtual environment
source .venv/bin/activate

# copy .env.example to .env.local and add your API key
cp .env.example .env.local

# install requirements
pip install -r requirements.txt

# run main.py
python main.py


# important links
## langchain

https://python.langchain.com/api_reference/


https://python.langchain.com/docs/tutorials/

## openai
https://platform.openai.com/docs/models

## together
https://api.together.ai/models

