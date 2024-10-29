import streamlit as st
import atexit
from api.apikeys import check_api_keys
from models.model_configuration import model_configuration
from utils.ollama_utils import (
    check_ollama_installed,
    run_ollama_setup,
    start_ollama_serve,
    stop_ollama_service,
    pull_ollama_model,
    remove_ollama_model
)
from utils.translation_utils import generate_response

st.title("🦜🔗 Language Translation App")

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
if 'providers' not in st.session_state:
    st.session_state.providers = model_configuration.get_providers()
selected_provider = st.sidebar.selectbox("Select Provider:", st.session_state.providers)

# Get fresh models list every time
models_by_provider = model_configuration.get_models_by_provider()

# Model selection based on provider
if selected_provider:
    # Force refresh models list for Ollama provider
    if selected_provider == "ollama":
        model_configuration.update_ollama_models()
        models_by_provider = model_configuration.get_models_by_provider()
    
    available_provider_models = models_by_provider.get(selected_provider, [])
    
    # Special handling for Ollama provider
    if selected_provider == "ollama":
        if not available_provider_models:
            st.sidebar.warning("No Ollama models available. Please pull a model first.")
            selected_model = None
        else:
            if ('selected_model' in st.session_state and 
                st.session_state.selected_model not in available_provider_models):
                del st.session_state.selected_model
                
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

# Ollama-specific controls
if selected_provider == "ollama":
    # Add new model section
    if st.sidebar.checkbox("Add new Ollama model"):
        new_model_name = st.sidebar.text_input("Enter new model name:")
        if st.sidebar.button("Pull New Model") and new_model_name:
            if pull_ollama_model(new_model_name):
                model_configuration.update_ollama_models()
                st.session_state.models_by_provider = model_configuration.get_models_by_provider()
                st.rerun()

    # Model controls
    if selected_model:
        if st.sidebar.button("Pull Ollama Model"):
            if pull_ollama_model(selected_model):
                model_configuration.update_ollama_models()
                st.session_state.models_by_provider = model_configuration.get_models_by_provider()
                st.rerun()
        
        if st.sidebar.button("Remove Ollama Model"):
            if remove_ollama_model(selected_model):
                model_configuration.update_ollama_models()
                st.session_state.models_by_provider = model_configuration.get_models_by_provider()
                if 'selected_model' in st.session_state:
                    del st.session_state.selected_model
                st.rerun()

    # Service controls
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Stop Service"):
            stop_ollama_service()
    with col2:
        if st.button("Start Service"):
            start_ollama_serve()

# Translation form
with st.form("translation_form"):
    text = st.text_area(
        "Enter text to translate:",
        "What are the three key pieces of advice for learning how to code?",
    )
    language = st.selectbox("Select target language:", ["Finnish", "French", "Spanish", "German"])
    submitted = st.form_submit_button("Translate")
    if submitted:
        generate_response(text, language, selected_model)

# Display missing API keys
missing_keys = check_api_keys()
if missing_keys:
    st.sidebar.warning("Missing API Keys:")
    for key in missing_keys:
        st.sidebar.write(f"- {key}")
    st.sidebar.write("Please add these keys to your .env.local file.")
