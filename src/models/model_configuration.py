#import from libraries
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether
from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_groq import ChatGroq
import os
from langchain_community.llms import Ollama

# Function to safely get API keys
def get_api_key(key_name, env_var_name):
    try:
        from src.api.apikeys import OPENAI_API_KEY, TOGETHER_API_KEY, ANTHROPIC_API_KEY, COHERE_API_KEY, GROQ_API_KEY, HF_TOKEN
        return locals().get(key_name)
    except ImportError:
        return os.getenv(env_var_name)

# Function to safely create chat models
def create_chat_model(model_class, api_key, **kwargs):
    if api_key is None:
        print(f"Warning: {model_class.__name__} not initialized due to missing API key.")
        return None
    try:
        return model_class(api_key=api_key, **kwargs)
    except Exception as e:
        print(f"Warning: {model_class.__name__} not initialized. Error: {str(e)}")
        return None

# Initialize chat models
openai_chat_model = create_chat_model(ChatOpenAI, get_api_key('OPENAI_API_KEY', 'OPENAI_API_KEY'), model="gpt-3.5-turbo")
together_chat_model = create_chat_model(ChatTogether, get_api_key('TOGETHER_API_KEY', 'TOGETHER_API_KEY'), model="meta-llama/Llama-3.2-3B-Instruct-Turbo")
anthropic_chat_model = create_chat_model(ChatAnthropic, get_api_key('ANTHROPIC_API_KEY', 'ANTHROPIC_API_KEY'), model="claude-3-5-sonnet-20240620")
cohere_chat_model = create_chat_model(ChatCohere, get_api_key('COHERE_API_KEY', 'COHERE_API_KEY'), model="command-r-plus")
groq_chat_model = create_chat_model(ChatGroq, get_api_key('GROQ_API_KEY', 'GROQ_API_KEY'), model="llama3-8b-8192")
huggingface_chat_model = create_chat_model(
    ChatHuggingFace, 
    get_api_key('HUGGINGFACEHUB_API_TOKEN', 'HUGGINGFACEHUB_API_TOKEN'), llm= HuggingFaceEndpoint(repo_id="microsoft/Phi-3-mini-4k-instruct",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,) ,verbose=True
)

# Initialize Ollama model (we'll use a placeholder here)
ollama_model = Ollama(model="llama2")

# Add Ollama to available models
available_models = {
    "openai": openai_chat_model,
    "together": together_chat_model,
    "anthropic": anthropic_chat_model,
    "cohere": cohere_chat_model,
    "groq": groq_chat_model,
    "huggingface": huggingface_chat_model,
    "ollama": ollama_model
}

available_models = {k: v for k, v in available_models.items() if v is not None}
