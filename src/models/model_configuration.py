#import from libraries
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether
from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_groq import ChatGroq
import os
from langchain_community.llms import Ollama
import subprocess

class ModelConfiguration:
    def __init__(self):
        self.model_configs = {
            "gpt-3.5-turbo": {"provider": "openai", "class": ChatOpenAI, "api_key": "OPENAI_API_KEY"},
            "llama-3.2-3b-instruct-turbo": {"provider": "together", "class": ChatTogether, "api_key": "TOGETHER_API_KEY"},
            "claude-3-5-sonnet": {
                "provider": "anthropic", 
                "class": ChatAnthropic, 
                "api_key": "ANTHROPIC_API_KEY",
                "extra_kwargs": {"model_name": "claude-3-sonnet-20240229"}
            },
            "command-r-plus": {"provider": "cohere", "class": ChatCohere, "api_key": "COHERE_API_KEY"},
            "llama3-8b-8192": {"provider": "groq", "class": ChatGroq, "api_key": "GROQ_API_KEY"},
            "phi-3-mini": {
                "provider": "huggingface", 
                "class": ChatHuggingFace,
                "api_key": "HUGGINGFACEHUB_API_TOKEN",
                "extra_kwargs": {
                    "llm": HuggingFaceEndpoint(
                        repo_id="microsoft/Phi-3-mini-4k-instruct",
                        task="text-generation",
                        max_new_tokens=512,
                        do_sample=False,
                        repetition_penalty=1.03,
                    )
                }
            }
        }
        # Dynamically add Ollama models
        self.update_ollama_models()
        
    def update_ollama_models(self):
        """Update available Ollama models from the system"""
        try:
            import subprocess
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                models = result.stdout.strip().split('\n')[1:]  # Skip header
                for model in models:
                    model_name = model.split()[0]
                    self.model_configs[model_name] = {
                        "provider": "ollama",
                        "class": Ollama,
                        "extra_kwargs": {"model": model_name}
                    }
        except Exception as e:
            print(f"Warning: Could not fetch Ollama models: {str(e)}")

    def get_api_key(self, key_name):
        """Get API key from environment or api_keys file"""
        try:
            from src.api.apikeys import OPENAI_API_KEY, TOGETHER_API_KEY, ANTHROPIC_API_KEY, COHERE_API_KEY, GROQ_API_KEY, HF_TOKEN
            return locals().get(key_name)
        except ImportError:
            return os.getenv(key_name)

    def get_chat_model(self, model_name):
        """Get a chat model instance based on model name"""
        if model_name not in self.model_configs:
            raise ValueError(f"Unknown model: {model_name}")
            
        config = self.model_configs[model_name]
        model_class = config["class"]
        
        kwargs = config.get("extra_kwargs", {})
        
        if "api_key" in config:
            api_key = self.get_api_key(config["api_key"])
            if api_key is None:
                print(f"Warning: {model_name} not initialized due to missing API key.")
                return None
            kwargs["api_key"] = api_key
            
        try:
            return model_class(**kwargs)
        except Exception as e:
            print(f"Warning: {model_name} not initialized. Error: {str(e)}")
            return None

    def get_available_models(self):
        """Get list of all available models"""
        self.update_ollama_models()  # Refresh Ollama models
        return list(self.model_configs.keys())

    def get_provider(self, model_name):
        """Get provider name for a model"""
        if model_name in self.model_configs:
            return self.model_configs[model_name]["provider"]
        return None

    def get_providers(self):
        """Get list of all available providers"""
        # Always include Ollama in providers list, even if no models are currently available
        providers = set(config["provider"] for config in self.model_configs.values())
        providers.add("ollama")  # Add Ollama provider regardless of model availability
        return sorted(providers)

    def get_models_by_provider(self):
        """Get dictionary of providers and their available models"""
        self.update_ollama_models()  # Refresh Ollama models
        models_by_provider = {}
        
        # Initialize all providers with empty lists, including Ollama
        for provider in self.get_providers():
            models_by_provider[provider] = []
        
        # Add models to their respective providers
        for model_name, config in self.model_configs.items():
            provider = config["provider"]
            models_by_provider[provider].append(model_name)
            
        return models_by_provider

# Create singleton instance
model_configuration = ModelConfiguration()
