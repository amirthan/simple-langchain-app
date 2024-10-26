#LLM with LCEL chain - use this instead
from prompt_templates import translation_prompt_template
from model_configuration import openai_chat_model, together_chat_model
from output_parsers import translation_parser




translation_chain_openai = translation_prompt_template | openai_chat_model | translation_parser
translation_chain_together = translation_prompt_template | together_chat_model | translation_parser
