
from chains import translation_chain_openai, translation_chain_together




 


 #Calling LLM with LCEL chain - use this instead
result_openai = translation_chain_openai.invoke({"language": "Finnish", "text": "The weather is so bad"})
result_together = translation_chain_together.invoke({"language": "Finnish", "text": "The weather is so bad"})

print(result_openai)
print(result_together)

