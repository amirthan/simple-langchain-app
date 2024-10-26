#LLM with LCEL chain - use this instead
from prompt_templates import translation_prompt_template
from model_configuration import openai_chat_model, together_chat_model, anthropic_chat_model, cohere_chat_model, groq_chat_model, huggingface_chat_model
from output_parsers import translation_parser




translation_chain_openai = translation_prompt_template | openai_chat_model | translation_parser
translation_chain_together = translation_prompt_template | together_chat_model | translation_parser
translation_chain_anthropic = translation_prompt_template | anthropic_chat_model | translation_parser
translation_chain_cohere = translation_prompt_template | cohere_chat_model | translation_parser
#translation_chain_google = translation_prompt_template | google_chat_model | translation_parser
translation_chain_groq = translation_prompt_template | groq_chat_model | translation_parser
translation_chain_huggingface = translation_prompt_template | huggingface_chat_model | translation_parser