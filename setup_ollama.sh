#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Ollama setup...${NC}"

# Check if Ollama is already installed
if command -v ollama >/dev/null 2>&1; then
    echo -e "${GREEN}Ollama is already installed${NC}"
else
    # Install Ollama
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install Ollama${NC}"
        exit 1
    fi
fi

# Create a systemd service file for Ollama
echo "Setting up Ollama service..."
sudo tee /etc/systemd/system/ollama.service > /dev/null << EOL
[Unit]
Description=Ollama Service
After=network.target

[Service]
Environment="OLLAMA_PORT=11434"
ExecStart=/usr/local/bin/ollama serve
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd daemon
sudo systemctl daemon-reload

# Enable and start Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama

# Wait for Ollama service to start
sleep 5

# Pull the Llama model
echo "Pulling Llama model..."
#this pulls the model we want to use from ollama
ollama pull llama3.2
#this starts the ollama server after this we can use it in our main.py file
ollama serve
#ollama run llama2

# Create requirements.txt
#echo "Creating requirements.txt..."
#cat > requirements.txt << EOL
#langchain-ollama>=0.0.1
#python-dotenv>=0.19.0
#langchain>=0.1.0
#EOL

echo -e "${GREEN}Setup completed!${NC}"
echo "You can check Ollama service status with: sudo systemctl status ollama"
echo "The service is running on "

