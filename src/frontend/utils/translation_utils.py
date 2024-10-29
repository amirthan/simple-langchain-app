import streamlit as st
from chains.chains import get_translation_chain

def generate_response(input_text, language="Finnish", model_name=None):
    """Generate translation response using the specified model"""
    if model_name is None:
        st.error("No model selected")
        return
        
    chain = get_translation_chain(model_name)
    if chain is None:
        st.error(f"Could not initialize chain for model {model_name}")
        return
    
    try:
        result = chain.invoke({"language": language, "text": input_text})
        st.info(result)
    except Exception as e:
        st.error(f"Error during translation: {str(e)}") 