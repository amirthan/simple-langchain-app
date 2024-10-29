import subprocess
import shutil
import streamlit as st
import time
import os

def check_ollama_installed():
    return shutil.which('ollama') is not None

def run_ollama_setup():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    setup_script = os.path.join(project_root, '../models/ollama/setup_ollama.sh')
    subprocess.run(['bash', setup_script], check=True)

def start_ollama_serve():
    subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_ollama_service():
    try:
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 '../models/ollama/stop_ollama.sh')
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
        time.sleep(2)
        success_message.empty()
        output_message.empty()
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