#LLM with LCEL chain - use this instead
from prompt_templates import translation_prompt_template
from model_configuration import available_models
from output_parsers import translation_parser




# Create translation chains for available models
translation_chains = {
    f"translation_chain_{model_name}": translation_prompt_template | model | translation_parser
    for model_name, model in available_models.items()
}
