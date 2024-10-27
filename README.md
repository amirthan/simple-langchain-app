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

# setup python path
unset PYTHONPATH
echo $PYTHONPATH
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"


# to run streamlit app
streamlit run frontend/streamlit_app.py


# important links
## langchain

https://python.langchain.com/api_reference/

https://python.langchain.com/docs/tutorials/

https://python.langchain.com/docs/integrations/chat/

https://python.langchain.com/docs/integrations/providers/

### How to guide from langchain 

https://python.langchain.com/docs/how_to/


## openai

https://platform.openai.com/docs/models

## together

https://api.together.ai/models

## anthropic

https://console.anthropic.com/dashboard

https://docs.anthropic.com/en/docs/about-claude/models

## cohere

https://dashboard.cohere.com/

https://docs.cohere.com/docs/models

## google

https://ai.google.dev/gemini-api

https://ai.google.dev/gemini-api/docs/models/gemini

https://cloud.google.com/vertex-ai


## groq

https://console.groq.com/docs/models

## huggingface

https://huggingface.co/
The list of avaialble models could be found here https://huggingface.co/models

you can define other parameters pipelinekwargs, model_kwargs based on your needs and those information canbe found in the model documentation.

Huggingface integration https://python.langchain.com/docs/integrations/providers/huggingface/


## streamlit

https://docs.streamlit.io/

https://docs.streamlit.io/develop/tutorials

## Huggingface

## to use ollama with huggingface

https://huggingface.co/docs/hub/en/ollama
