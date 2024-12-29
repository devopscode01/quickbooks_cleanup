#!/bin/bash

# Update the package list
sudo apt update -y

# Install Python3 and pip
sudo apt install python3 python3-pip -y

# Install required Python libraries
pip3 install pandas fuzzywuzzy python-Levenshtein
