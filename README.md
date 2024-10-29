# AI Chat Application

A versatile chat application that supports multiple AI models including OpenAI, Anthropic, Google, Cohere, Together.ai, Groq, and Hugging Face models. Built with Python, LangChain, and Streamlit.

## Features

- 🤖 Multi-model support: Chat with various AI models
- 🔄 Easy model switching: Switch between different AI providers seamlessly
- 💬 Interactive chat interface: Built with Streamlit for a smooth user experience
- 🔑 Secure API key management: Local environment variable support
- 🎯 Flexible deployment: Run locally or deploy to cloud

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. Create and activate a virtual environment:

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Copy .env.example to .env.local and add your API key
cp .env.example .env.local

# Install requirements
pip install -r requirements.txt

# Run main.py
python main.py

# Setup Python path
unset PYTHONPATH
echo $PYTHONPATH
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"

# To run streamlit app
streamlit run src/frontend/streamlit_app.py

## Errors
- If you get an error about chains module not found, you need to add the Python path as shown above

# Important links
## Langchain

https://python.langchain.com/api_reference/

https://python.langchain.com/docs/tutorials/

https://python.langchain.com/docs/integrations/chat/

https://python.langchain.com/docs/integrations/providers/

### How to guide from langchain

https://python.langchain.com/docs/how_to/

## Openai

https://platform.openai.com/docs/models

## Together

https://api.together.ai/models

## Anthropic

https://console.anthropic.com/dashboard

https://docs.anthropic.com/en/docs/about-claude/models

## Cohere

https://dashboard.cohere.com/

https://docs.cohere.com/docs/models

## Google

https://ai.google.dev/gemini-api

https://ai.google.dev/gemini-api/docs/models/gemini

https://cloud.google.com/vertex-ai

## Groq

https://console.groq.com/docs/models

## Huggingface

https://huggingface.co/
The list of avaialble models could be found here https://huggingface.co/models

you can define other parameters pipelinekwargs, model_kwargs based on your needs and those information canbe found in the model documentation.

Huggingface integration https://python.langchain.com/docs/integrations/providers/huggingface/

## Streamlit

https://docs.streamlit.io/

https://docs.streamlit.io/develop/tutorials

## Huggingface

## To use ollama with huggingface

https://huggingface.co/docs/hub/en/ollama

## Replicat

https://replicate.com/pricing

https://replicate.com/docs

https://replicate.com/explore