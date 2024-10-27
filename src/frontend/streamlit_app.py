import streamlit as st
import sys
import os
from dotenv import load_dotenv
import subprocess
import shutil
from chains.chains import get_translation_chain
import atexit
from api.apikeys import check_api_keys
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from models.model_configuration import model_configuration
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
        
        # Force refresh model configuration
        model_configuration.update_ollama_models()
        
        # Clear the session state to reset the selection
        if 'selected_model' in st.session_state:
            del st.session_state.selected_model
            
        time.sleep(2)  # Reduced sleep time
        success_message.empty()
        output_message.empty()
        
        # Rerun the app to refresh the UI
        st.rerun()
        return True
    except subprocess.CalledProcessError as e:
        error_message = st.error(f"Failed to remove {model_name} model. Error: {e}")
        output_message = st.code(e.output)
        time.sleep(2)
        error_message.empty()
        output_message.empty()
        return False
    except Exception as e:
        error_message = st.error(f"An unexpected error occurred while removing {model_name} model: {str(e)}")
        time.sleep(2)
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

# Get providers and their models
providers = model_configuration.get_providers()
models_by_provider = model_configuration.get_models_by_provider()

# Provider selection in sidebar
selected_provider = st.sidebar.selectbox("Select Provider:", providers)

# Model selection based on provider
if selected_provider:
    # Force refresh models list for Ollama provider
    if selected_provider == "ollama":
        model_configuration.update_ollama_models()
    
    available_provider_models = models_by_provider.get(selected_provider, [])
    
    # Special handling for Ollama provider
    if selected_provider == "ollama":
        if not available_provider_models:
            st.sidebar.warning("No Ollama models available. Please pull a model first.")
            selected_model = None
        else:
            # Store selection in session state
            if 'selected_model' not in st.session_state:
                st.session_state.selected_model = available_provider_models[0] if available_provider_models else None
                
            selected_model = st.sidebar.selectbox(
                "Select Ollama Model:",
                available_provider_models,
                key='selected_model'
            )
    else:
        selected_model = st.sidebar.selectbox(
            f"Select {selected_provider.capitalize()} Model:", 
            available_provider_models if available_provider_models else ["No models available"]
        )
        if selected_model == "No models available":
            selected_model = None
else:
    selected_model = None

# Ollama-specific controls (only show if Ollama provider is selected)
if selected_provider == "ollama":
    # Add new model section first
    if st.sidebar.checkbox("Add new Ollama model"):
        new_model_name = st.sidebar.text_input("Enter new model name:")
        if st.sidebar.button("Pull New Model") and new_model_name:
            if pull_ollama_model(new_model_name):
                # Force refresh of model configuration after successful pull
                model_configuration.update_ollama_models()
                st.rerun()

    # Only show other controls if there are models available
    if selected_model:
        if st.sidebar.button("Pull Ollama Model"):
            if pull_ollama_model(selected_model):
                model_configuration.update_ollama_models()
                st.rerun()
        
        if st.sidebar.button("Remove Ollama Model"):
            if remove_ollama_model(selected_model):
                # Force refresh of model configuration after successful removal
                model_configuration.update_ollama_models()
                st.rerun()
    
    # Always show service controls
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Stop Service"):
            stop_ollama_service()
    with col2:
        if st.button("Start Service"):
            start_ollama_serve()

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

with st.form("translation_form"):
    text = st.text_area(
        "Enter text to translate:",
        "What are the three key pieces of advice for learning how to code?",
    )
    language = st.selectbox("Select target language:", ["Finnish", "French", "Spanish", "German"])
    submitted = st.form_submit_button("Translate")
    if submitted:
        generate_response(text, language, selected_model)

# Add a section to display missing API keys
missing_keys = check_api_keys()
if missing_keys:
    st.sidebar.warning("Missing API Keys:")
    for key in missing_keys:
        st.sidebar.write(f"- {key}")
    st.sidebar.write("Please add these keys to your .env.local file.")
