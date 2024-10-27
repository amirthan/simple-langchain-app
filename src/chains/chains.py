#LLM with LCEL chain - use this instead
from prompts.prompt_templates import translation_prompt_template
from models.model_configuration import model_configuration
from output.output_parsers import translation_parser




# Create translation chains for available models
translation_chains = {}

# Initialize chains for each available model
for model_name in model_configuration.get_available_models():
    chat_model = model_configuration.get_chat_model(model_name)
    if chat_model is not None:
        translation_chains[model_name] = translation_prompt_template | chat_model | translation_parser

def get_translation_chain(model_name):
    """Get translation chain for a specific model"""
    if model_name not in translation_chains:
        # Try to create the chain if it doesn't exist
        chat_model = model_configuration.get_chat_model(model_name)
        if chat_model is None:
            return None
        translation_chains[model_name] = translation_prompt_template | chat_model | translation_parser
    
    return translation_chains[model_name]
