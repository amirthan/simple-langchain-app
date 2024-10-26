#LLM with LCEL chain - use this instead
from prompt_templates import *
from model_configuration import model
from output_parsers import translation_parser




translation_chain = translation_prompt_template | model | translation_parser
