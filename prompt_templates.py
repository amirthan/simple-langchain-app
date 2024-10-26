from langchain_core.prompts import ChatPromptTemplate


#  Translation Prompt Template
translation_system_template = "Translate this from English to {language}"

translation_prompt_template = ChatPromptTemplate.from_messages([
    ("system", translation_system_template),
    ("human", "{text}"),
])
