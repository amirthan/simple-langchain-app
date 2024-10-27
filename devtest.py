#from chains import translation_chain_cohere, translation_chain_openai, translation_chain_together, translation_chain_anthropic, translation_chain_groq, translation_chain_huggingface






#Calling LLM with LCEL chain 
#result_openai = translation_chain_openai.invoke({"language": "Finnish", "text": "The weather is so bad"})
#result_together = translation_chain_together.invoke({"language": "Finnish", "text": "The weather is so bad"})
#result_anthropic = translation_chain_anthropic.invoke({"language": "Finnish", "text": "The weather is so bad"})
#result_cohere = translation_chain_cohere.invoke({"language": "Finnish", "text": "The weather is so bad"})
#result_google = translation_chain_google.invoke({"language": "Finnish", "text": "The weather is so bad"})
#result_groq = translation_chain_groq.invoke({"language": "Finnish", "text": "The weather is so bad"})
#result_huggingface = translation_chain_huggingface.invoke({"language": "Finnish", "text": "The weather is so bad"})



#print(result_openai)
#print(result_together)
#print(result_anthropic)
#print(result_cohere)
#print(result_google)
#print(result_groq)
#print(result_huggingface)








## to install ollama




from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama

# Define the prompt template
template = """Question: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

# Initialize the Ollama model
model = Ollama(model="llama3.2:latest")

# Create the chain
chain = prompt | model

# Invoke the chain with a question
result = chain.invoke({"question": "What is LangChain?"})

# Print the result
print(result)
