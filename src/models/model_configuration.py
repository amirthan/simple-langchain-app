#import from libraries
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether
from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
import os
from langchain_community.llms import Ollama
import subprocess
from .model_catalog import MODEL_CATALOG, get_provider_info, get_model_info

class ModelConfiguration:
    def __init__(self):
        self.model_configs = {}
        # Initialize API models from catalog
        self._initialize_catalog_models()
        # Initialize Ollama models
        self.update_ollama_models()
        
    def _initialize_catalog_models(self):
        """Initialize models from the MODEL_CATALOG"""
        for provider_name, provider_info in MODEL_CATALOG.items():
            for model_name, model_info in provider_info.models.items():
                self.model_configs[model_name] = {
                    "provider": provider_name,
                    "class": eval(provider_info.model_class),  # Convert string to class reference
                    "api_key": provider_info.api_key_name,
                    "extra_kwargs": model_info.extra_kwargs or {}
                }
                
                # Special handling for HuggingFace models
                if provider_name == "huggingface" and model_info.extra_kwargs:
                    llm_config = model_info.extra_kwargs.get("llm", {})
                    if llm_config:
                        self.model_configs[model_name]["extra_kwargs"]["llm"] = \
                            HuggingFaceEndpoint(**llm_config["kwargs"])

    def update_ollama_models(self):
        """Update available Ollama models from the system"""
        try:
            # Remove existing Ollama models
            self.model_configs = {
                name: config for name, config in self.model_configs.items() 
                if config["provider"] != "ollama"
            }
            
            # Add current Ollama models
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                models = result.stdout.strip().split('\n')[1:]
                for model in models:
                    if model.strip():
                        model_name = model.split()[0]
                        self.model_configs[model_name] = {
                            "provider": "ollama",
                            "class": ChatOllama,
                            "extra_kwargs": {"model": model_name, "temperature": 0}
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
        kwargs = config.get("extra_kwargs", {}).copy()
        
        # Add model name and temperature for API-based models
        if config["provider"] != "ollama":
            # Get the actual model name from the catalog
            provider = config["provider"]
            model_info = get_model_info(provider, model_name)
            if model_info:
                kwargs["model"] = model_info.name  # Use the name from ModelInfo
                kwargs["temperature"] = 0
            else:
                print(f"Warning: Model {model_name} not found in catalog")
                return None
        
        if "api_key" in config:
            api_key = self.get_api_key(config["api_key"])
            if api_key is None:
                print(f"Warning: {model_name} not initialized due to missing API key.")
                return None
            kwargs["api_key"] = api_key
            
        try:
            return model_class(**kwargs)
        except Exception as e:
            print(f"Warning: Could not initialize {model_name}. Error: {str(e)}")
            return None

    def get_available_models(self):
        """Get list of all available models"""
        self.update_ollama_models()
        return list(self.model_configs.keys())

    def get_provider(self, model_name):
        """Get provider name for a model"""
        if model_name in self.model_configs:
            return self.model_configs[model_name]["provider"]
        return None

    def get_providers(self):
        """Get list of all available providers"""
        providers = set(config["provider"] for config in self.model_configs.values())
        providers.add("ollama")
        return sorted(providers)

    def get_models_by_provider(self):
        """Get dictionary of providers and their available models"""
        self.update_ollama_models()
        models_by_provider = {}
        
        # Initialize providers
        for provider in self.get_providers():
            if provider == "ollama":
                ollama_models = [model_name for model_name, config in self.model_configs.items() 
                               if config["provider"] == "ollama"]
                models_by_provider["ollama"] = ollama_models if ollama_models else ["No models available"]
            else:
                models_by_provider[provider] = []
        
        # Add models to providers
        for model_name, config in self.model_configs.items():
            provider = config["provider"]
            if provider != "ollama":
                models_by_provider[provider].append(model_name)
        
        return models_by_provider

# Create singleton instance
model_configuration = ModelConfiguration()
