#!/bin/bash
# Installation script for Facesearch on Kali Linux

echo -e "\e[32m[*] Installing Facesearch for Kali Linux...\e[0m"

# Update system
sudo apt-get update

# Install Python and pip if not present
sudo apt-get install -y python3 python3-pip git

# Install required Python packages
pip3 install -r requirements.txt

# Make the main script executable
chmod +x facesearch.py

echo -e "\e[32m[✓] Installation complete! Run: python3 facesearch.py\e[0m"