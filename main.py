
import apikeys
from model_configuration import model
from output_parsers import translation_parser
from prompt_templates import *
from chains import translation_chain




 


 #Calling LLM with LCEL chain - use this instead
result = translation_chain.invoke({"language": "Finnish", "text": "The weather is so bad"})
print(result)

