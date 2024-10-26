#!/bin/bash

# Function to stop and remove the container
stop_and_remove_container() {
    echo "Stopping existing ollama container..."
    docker stop ollama 2>/dev/null
    echo "Removing existing ollama container..."
    docker rm ollama 2>/dev/null
}

# Check if the ollama container exists (running or stopped)
if [ "$(docker ps -aq -f name=ollama)" ]; then
    stop_and_remove_container
fi

# Run the ollama container
echo "Starting new ollama container..."
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# Wait for the container to start
echo "Waiting for ollama container to start..."
sleep 10

# Check if the container is running
if [ "$(docker ps -q -f name=ollama)" ]; then
    echo "Ollama container is running."
    
    # Pull the llama2 model
    echo "Pulling llama2 model..."
    docker exec ollama ollama pull llama2
    
    echo "Setup complete. You can now run your main.py script."
else
    echo "Failed to start ollama container. Please check Docker logs for more information."
fi
