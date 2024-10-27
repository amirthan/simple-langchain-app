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
from models.model_configuration import available_models
import time


st.title("🦜🔗 Language Translation App")

def check_ollama_installed():
    return shutil.which('ollama') is not None

def run_ollama_setup():
    project_root = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
    setup_script = os.path.join(project_root, '../models/ollama/setup_ollama.sh')  # Adjust the path to the script
    subprocess.run(['bash', setup_script], check=True)

def start_ollama_serve():
    subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_ollama_service():
    try:
        # Run the stop_ollama.sh script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../models/ollama/stop_ollama.sh')
        subprocess.run(['bash', script_path], check=True)
        st.success("Ollama service stopped successfully.")
    except subprocess.CalledProcessError:
        st.error("Failed to stop Ollama service. Make sure you have the necessary permissions.")

def pull_ollama_model(model_name):
    st.info(f"Pulling Ollama model: {model_name}. This may take a few minutes...")
    try:
        result = subprocess.run(['ollama', 'pull', model_name], check=True, capture_output=True, text=True)
        success_message = st.success(f"Successfully pulled {model_name} model.")
        output_message = st.code(result.stdout)
        # Auto-clear messages after 5 seconds
        time.sleep(5)
        success_message.empty()
        output_message.empty()
        return True
    except subprocess.CalledProcessError as e:
        error_message = st.error(f"Failed to pull {model_name} model. Error: {e}")
        output_message = st.code(e.output)
        time.sleep(5)
        error_message.empty()
        output_message.empty()
        return False
    except Exception as e:
        error_message = st.error(f"An unexpected error occurred while pulling {model_name} model: {str(e)}")
        time.sleep(5)
        error_message.empty()
        return False

def remove_ollama_model(model_name):
    st.info(f"Removing Ollama model: {model_name}.")
    try:
        result = subprocess.run(['ollama', 'rm', model_name], check=True, capture_output=True, text=True)
        success_message = st.success(f"Successfully removed {model_name} model.")
        output_message = st.code(result.stdout)
        time.sleep(5)
        success_message.empty()
        output_message.empty()
        return True
    except subprocess.CalledProcessError as e:
        error_message = st.error(f"Failed to remove {model_name} model. Error: {e}")
        output_message = st.code(e.output)
        time.sleep(5)
        error_message.empty()
        output_message.empty()
        return False
    except Exception as e:
        error_message = st.error(f"An unexpected error occurred while removing {model_name} model: {str(e)}")
        time.sleep(5)
        error_message.empty()
        return False

# Check if Ollama is installed, if not, run the setup
if not check_ollama_installed():
    st.warning("Ollama is not installed. Running setup script...")
    run_ollama_setup()
    st.success("Ollama setup completed.")

# Start Ollama serve
start_ollama_serve()

# Register the stop function to be called when the app exits
atexit.register(stop_ollama_service)

try:
    print("Successfully imported translation_chains")
except ImportError as e:
    print("Error importing translation_chains:", str(e))
    st.error(f"Failed to import translation_chains: {str(e)}")
    st.stop()

# Add Ollama to the available models
available_model_providers = list(available_models.keys()) 
selected_model_provider = st.sidebar.selectbox("Select Model provider:", available_model_providers)


# Ollama model selection
if selected_model_provider == "ollama":
    # Get the list of available Ollama models
    ollama_models = subprocess.check_output(["ollama", "list"]).decode().strip().split('\n')[1:]
    ollama_models = [model.split()[0] for model in ollama_models]
    # Add "Add new model" option to the list
    ollama_models = ["Add new model"] + ollama_models
    
    selected_ollama_model = st.sidebar.selectbox("Select Ollama Model:", ollama_models)
    
    # Show input field for new model name if "Add new model" is selected
    if selected_ollama_model == "Add new model":
        new_model_name = st.sidebar.text_input("Enter new model name:")
        if st.sidebar.button("Pull Ollama Model") and new_model_name:
            pull_ollama_model(new_model_name)
            st.rerun()  # Rerun the app to update the model list
    else:
        if st.sidebar.button("Pull Ollama Model"):
            pull_ollama_model(selected_ollama_model)
            st.rerun()
        
    # Add stop and start buttons in the sidebar
    if st.sidebar.button("Stop Ollama Service"):
        stop_ollama_service()
    if st.sidebar.button("Start Ollama Service"):
        start_ollama_serve()
    if selected_ollama_model != "Add new model" and st.sidebar.button("Remove Ollama Model"):
        remove_ollama_model(selected_ollama_model)
        st.rerun()

selected_chain = translation_chains[f"translation_chain_{selected_model_provider}"]

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
