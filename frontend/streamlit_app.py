import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Add debug prints


# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

load_dotenv(dotenv_path=os.path.join(project_root, '.env.local'))  # Load environment variables from .env.local file

st.title("🦜🔗 Language Translation App")

try:
    from chains import translation_chains
    print("Successfully imported translation_chains")
except ImportError as e:
    print("Error importing translation_chains:", str(e))
    st.error(f"Failed to import translation_chains: {str(e)}")
    st.stop()

# Add a dropdown to select the model in the sidebar
available_models = list(translation_chains.keys())
selected_model = st.sidebar.selectbox("Select Model:", available_models)

# Use the selected model's translation chain
selected_chain = translation_chains[selected_model]

def generate_response(input_text, language="Finnish"):
    result = selected_chain.invoke({"language": language, "text": input_text})
    st.info(result)

with st.form("translation_form"):
    text = st.text_area(
        "Enter text to translate:",
        "What are the three key pieces of advice for learning how to code?",
    )
    language = st.selectbox("Select target language:", ["Finnish", "French", "Spanish", "German"])
    submitted = st.form_submit_button("Translate")
    if submitted:
        generate_response(text, language)

#st.sidebar.write("Available models:", ", ".join(available_models))

# Add a section to display missing API keys
from apikeys import check_api_keys
missing_keys = check_api_keys()
if missing_keys:
    st.sidebar.warning("Missing API Keys:")
    for key in missing_keys:
        st.sidebar.write(f"- {key}")
    st.sidebar.write("Please add these keys to your .env.local file.")
