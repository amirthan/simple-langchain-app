from dataclasses import dataclass
from typing import Dict, Any, Optional, List

@dataclass
class ModelInfo:
    name: str
    context_window: int
    input_cost_per_1k: float
    output_cost_per_1k: float
    description: str = ""
    extra_kwargs: Dict[str, Any] = None

@dataclass
class ProviderInfo:
    name: str
    model_class: Any
    api_key_name: str
    models: Dict[str, ModelInfo]

MODEL_CATALOG = {
    "openai": ProviderInfo(
        name="openai",
        model_class="ChatOpenAI",
        api_key_name="OPENAI_API_KEY",
        models={
            "gpt-3.5-turbo": ModelInfo(
                name="gpt-3.5-turbo",
                context_window=16385,
                input_cost_per_1k=0.0005,
                output_cost_per_1k=0.0015,
                description="Most capable GPT-3.5 model for chat completion"
            ),
            "gpt-4": ModelInfo(
                name="gpt-5",
                context_window=8192,
                input_cost_per_1k=0.03,
                output_cost_per_1k=0.06,
                description="Most capable GPT-4 model"
            )
        }
    ),
    "anthropic": ProviderInfo(
        name="anthropic",
        model_class="ChatAnthropic",
        api_key_name="ANTHROPIC_API_KEY",
        models={
            "claude-3-sonnet": ModelInfo(
                name="claude-3-sonnet",
                context_window=200000,
                input_cost_per_1k=0.0015,
                output_cost_per_1k=0.0015,
                description="Anthropic's latest model, balanced between intelligence and speed",
                extra_kwargs={"model_name": "claude-3-sonnet-20240229"}
            )
        }
    ),
    "together": ProviderInfo(
        name="together",
        model_class="ChatTogether",
        api_key_name="TOGETHER_API_KEY",
        models={
            "llama-3.2-3b-instruct-turbo": ModelInfo(
                name="llama-3.2-3b-instruct-turbo",
                context_window=4096,
                input_cost_per_1k=0.0002,
                output_cost_per_1k=0.0002,
                description="Optimized Llama model for instruction following"
            )
        }
    ),
    "cohere": ProviderInfo(
        name="cohere",
        model_class="ChatCohere",
        api_key_name="COHERE_API_KEY",
        models={
            "command-r-plus": ModelInfo(
                name="command-r-plus",
                context_window=128000,
                input_cost_per_1k=0.0015,
                output_cost_per_1k=0.0015,
                description="Cohere's most capable model"
            )
        }
    ),
    "groq": ProviderInfo(
        name="groq",
        model_class="ChatGroq",
        api_key_name="GROQ_API_KEY",
        models={
            "llama3-8b-8192": ModelInfo(
                name="llama3-8b-8192",
                context_window=8192,
                input_cost_per_1k=0.0001,
                output_cost_per_1k=0.0001,
                description="Optimized Llama model with Groq's infrastructure"
            )
        }
    ),
    "huggingface": ProviderInfo(
        name="huggingface",
        model_class="ChatHuggingFace",
        api_key_name="HUGGINGFACEHUB_API_TOKEN",
        models={
            "phi-3-mini": ModelInfo(
                name="phi-3-mini",
                context_window=4096,
                input_cost_per_1k=0.0,
                output_cost_per_1k=0.0,
                description="Microsoft's compact yet capable language model",
                extra_kwargs={
                    "llm": {
                        "class": "HuggingFaceEndpoint",
                        "kwargs": {
                            "repo_id": "microsoft/Phi-3-mini-4k-instruct",
                            "task": "text-generation",
                            "max_new_tokens": 512,
                            "do_sample": False,
                            "repetition_penalty": 1.03,
                        }
                    }
                }
            )
        }
    )
}

def get_provider_info(provider_name: str) -> Optional[ProviderInfo]:
    return MODEL_CATALOG.get(provider_name)

def get_model_info(provider_name: str, model_name: str) -> Optional[ModelInfo]:
    provider = get_provider_info(provider_name)
    if provider:
        return provider.models.get(model_name)
    return None

def get_all_providers() -> List[str]:
    return sorted(MODEL_CATALOG.keys())

def get_provider_models(provider_name: str) -> List[str]:
    provider = get_provider_info(provider_name)
    if provider:
        return sorted(provider.models.keys())
    return []
