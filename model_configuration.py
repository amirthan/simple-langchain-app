
#import from libraries
from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether
from langchain_anthropic import ChatAnthropic
from langchain_cohere import ChatCohere
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
#from langchain_google_genai import ChatGemini
from langchain_groq import ChatGroq
from apikeys import OPENAI_API_KEY, TOGETHER_API_KEY, ANTHROPIC_API_KEY, COHERE_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY, HF_TOKEN

#model configuration
openai_chat_model = ChatOpenAI(model="gpt-4o-mini")
together_chat_model = ChatTogether(model="meta-llama/Llama-3.2-3B-Instruct-Turbo")
anthropic_chat_model = ChatAnthropic(model="claude-3-5-sonnet-20240620")
cohere_chat_model = ChatCohere(model="command-r-plus")
#google_chat_model = ChatGemini(model="gemini-1.5-flash-latest")
groq_chat_model = ChatGroq(model="llama3-8b-8192")



huggingface_llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
)

huggingface_chat_model = ChatHuggingFace(llm=huggingface_llm, verbose=True)