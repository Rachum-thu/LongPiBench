#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to print messages in green
function echo_success {
    echo -e "\e[32m$1\e[0m"
}

# Function to print messages in yellow
function echo_info {
    echo -e "\e[33m$1\e[0m"
}

# Function to print messages in red
function echo_error {
    echo -e "\e[31m$1\e[0m"
}

# Check if Conda is installed
if ! command -v conda &> /dev/null
then
    echo_error "Conda is not installed. Please install Conda before running this script."
    exit 1
fi

# Define download URLs
DATA_URL="https://github.com/Rachum-thu/LongPiBench/releases/download/test/data.zip"
ORIGINAL_RES_URL="https://github.com/Rachum-thu/LongPiBench/releases/download/test/original_res.zip"

# Define filenames
DATA_ZIP="data.zip"
ORIGINAL_RES_ZIP="original_res.zip"

# Download data.zip
echo_info "Downloading data.zip from $DATA_URL ..."
wget -O "$DATA_ZIP" "$DATA_URL"

# Extract data.zip
echo_info "Extracting $DATA_ZIP ..."
unzip -q "$DATA_ZIP" -d ./

# Verify extraction
if [ ! -d "data" ]; then
    echo_error "Failed to extract data.zip. 'data' directory not found."
    exit 1
fi
echo_success "'data' directory has been created."

# Download original_res.zip
echo_info "Downloading original_res.zip from $ORIGINAL_RES_URL ..."
wget -O "$ORIGINAL_RES_ZIP" "$ORIGINAL_RES_URL"

# Extract original_res.zip
echo_info "Extracting $ORIGINAL_RES_ZIP ..."
unzip -q "$ORIGINAL_RES_ZIP" -d ./

# Verify extraction
if [ ! -d "res" ]; then
    echo_error "Failed to extract original_res.zip. 'res' directory not found."
    exit 1
fi
echo_success "'res' directory has been created."

# Create res folder if it doesn't exist (redundant if extraction already created it)
if [ ! -d "res" ]; then
    echo_info "Creating 'res' directory ..."
    mkdir res
    echo_success "'res' directory has been created."
else
    echo_info "'res' directory already exists."
fi

# Create .env file with environment variables
echo_info "Creating .env file ..."
cat > .env <<EOL
YOUR_OPENAI_API_KEY=
YOUR_OPENAI_BASE_URL=
YOUR_DEEPSEEK_API_KEY=
YOUR_DEEPSEEK_BASE_URL=
YOUR_ZHIPUAI_API_KEY=
YOUR_DEEP_INF_API_KEY=
YOUR_DEEP_INF_BASE=
YOUR_BAILIAN_API_KEY=
YOUR_BAILIAN_BASE_URL=
EOL
echo_success ".env file has been created."

# Define Conda environment details
ENV_NAME="longpi"
PYTHON_VERSION="3.10.14"

# Create Conda environment
echo_info "Creating Conda environment '$ENV_NAME' with Python $PYTHON_VERSION ..."
conda create -y -n "$ENV_NAME" python="$PYTHON_VERSION"
echo_success "Conda environment '$ENV_NAME' has been created."

# Activate Conda environment
echo_info "Activating Conda environment '$ENV_NAME' ..."
# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"
echo_success "Conda environment '$ENV_NAME' is now active."

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo_error "requirements.txt not found in the current directory."
    exit 1
fi

# Upgrade pip
echo_info "Upgrading pip ..."
pip install --upgrade pip

# Install required Python packages
echo_info "Installing Python packages from requirements.txt ..."
pip install -r requirements.txt
echo_success "Python packages have been installed."

# Install the local package in editable mode
echo_info "Installing the local package using 'pip install -e .' ..."
pip install -e .
echo_success "Local package has been installed in editable mode."

echo_success "Setup completed successfully!"
echo_info "Please fill in the necessary API keys in the .env file."
