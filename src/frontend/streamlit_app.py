import streamlit as st
import sys
import os
from dotenv import load_dotenv
import subprocess
import shutil
from chains.chains import translation_chains
import atexit
from api.apikeys import check_api_keys
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate


# Add the project root directory to the Python path
#project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.append(project_root)

#load_dotenv(dotenv_path=os.path.join(project_root, '.env.local'))  # Load environment variables from .env.local file

st.title("🦜🔗 Language Translation App")

def check_ollama_installed():
    return shutil.which('ollama') is not None

def run_ollama_setup():
    setup_script = os.path.join(project_root, 'setup_ollama.sh')
    subprocess.run(['bash', setup_script], check=True)

def start_ollama_serve():
    subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_ollama_service():
    try:
        subprocess.run(['sudo', 'systemctl', 'stop', 'ollama.service'], check=True)
        st.success("Ollama service stopped successfully.")
    except subprocess.CalledProcessError:
        st.error("Failed to stop Ollama service. Make sure you have the necessary permissions.")

# Check if Ollama is installed, if not, run the setup
if not check_ollama_installed():
    st.warning("Ollama is not installed. Running setup script...")
    run_ollama_setup()
    st.success("Ollama setup completed.")

# Start Ollama serve
start_ollama_serve()

# Register the stop function to be called when the app exits
atexit.register(stop_ollama_service)

# Add stop button in the sidebar
if st.sidebar.button("Stop Ollama Service"):
    stop_ollama_service()

try:
    print("Successfully imported translation_chains")
except ImportError as e:
    print("Error importing translation_chains:", str(e))
    st.error(f"Failed to import translation_chains: {str(e)}")
    st.stop()

# Add Ollama to the available models
available_models = list(translation_chains.keys()) + ["ollama"]
selected_model = st.sidebar.selectbox("Select Model:", available_models)

# Ollama model selection
if selected_model == "ollama":
    # Get the list of available Ollama models
    ollama_models = subprocess.check_output(["ollama", "list"]).decode().strip().split('\n')[1:]
    ollama_models = [model.split()[0] for model in ollama_models]
    
    selected_ollama_model = st.sidebar.selectbox("Select Ollama Model:", ollama_models)

    # Initialize Ollama model
    ollama_model = Ollama(model=selected_ollama_model)

    # Create Ollama chain
    ollama_prompt = ChatPromptTemplate.from_template("Translate this from English to {language}: {text}")
    ollama_chain = ollama_prompt | ollama_model

    selected_chain = ollama_chain
else:
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

# Add a section to display missing API keys
missing_keys = check_api_keys()
if missing_keys:
    st.sidebar.warning("Missing API Keys:")
    for key in missing_keys:
        st.sidebar.write(f"- {key}")
    st.sidebar.write("Please add these keys to your .env.local file.")
