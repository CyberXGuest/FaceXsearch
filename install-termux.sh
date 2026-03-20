#!/data/data/com.termux/files/usr/bin/bash
# Installation script for Facesearch on Termux

echo -e "\e[32m[*] Installing Facesearch for Termux...\e[0m"

# Update packages
pkg update -y

# Install required packages
pkg install -y python git

# Install required Python packages
pip install colorama requests google-auth google-auth-oauthlib google-auth-httplib2

# Make the main script executable
chmod +x facesearch.py

echo -e "\e[32m[✓] Installation complete! Run: python facesearch.py\e[0m"