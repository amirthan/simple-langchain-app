#!/bin/bash

# Function to stop Ollama server
stop_ollama() {
    echo "Stopping Ollama server..."
    
    # Stop the Ollama service
    sudo systemctl stop ollama.service
    
    # Disable the Ollama service
    sudo systemctl disable ollama.service
    
    # Find and kill any remaining Ollama processes
    PID=$(sudo lsof -t -i :11434)
    if [ -n "$PID" ]; then
        sudo kill -9 $PID
        echo "Remaining Ollama processes killed."
    fi
    
    echo "Ollama server stopped and disabled."
}

# Run the stop function
stop_ollama

exit 0