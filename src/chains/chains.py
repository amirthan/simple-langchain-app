#LLM with LCEL chain - use this instead
from prompts.prompt_templates import translation_prompt_template
from models.model_configuration import available_models
from output.output_parsers import translation_parser




# Create translation chains for available models
translation_chains = {
    f"translation_chain_{model_provider}": translation_prompt_template | chat_model | translation_parser
    for model_provider, chat_model in available_models.items()
}