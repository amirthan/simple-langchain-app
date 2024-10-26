
#import from libraries
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether
from apikeys import OPENAI_API_KEY, TOGETHER_API_KEY


#model configuration
openai_chat_model = ChatOpenAI(model="gpt-4o-mini")
together_chat_model = ChatTogether(model="meta-llama/Llama-3.2-3B-Instruct-Turbo")
