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

# Check if 'wget' is installed
if ! command -v wget &> /dev/null
then
    echo_error "'wget' command not found. Please install 'wget' to proceed."
    exit 1
fi

# Check if 'unzip' is installed
if ! command -v unzip &> /dev/null
then
    echo_error "'unzip' command not found. Please install 'unzip' to proceed."
    exit 1
fi

# Define download URLs (Ensure these URLs are correct and files exist)
DATA_URL="https://github.com/Rachum-thu/LongPiBench/releases/download/test/data.zip"
ORIGINAL_RES_URL="https://github.com/Rachum-thu/LongPiBench/releases/download/test/original_res.zip"

# Define filenames
DATA_ZIP="data.zip"
ORIGINAL_RES_ZIP="original_res.zip"

# Download data.zip
echo_info "Downloading data.zip from $DATA_URL ..."
wget -O "$DATA_ZIP" "$DATA_URL" || { echo_error "Failed to download data.zip"; exit 1; }

# Extract data.zip
echo_info "Extracting $DATA_ZIP ..."
unzip -q "$DATA_ZIP" -d ./

# Verify extraction
if [ ! -d "data" ]; then
    echo_info "'data' directory not found after extraction. Creating it."
    mkdir data
    echo_success "'data' directory has been created."
else
    echo_success "'data' directory exists."
fi

# Download original_res.zip
echo_info "Downloading original_res.zip from $ORIGINAL_RES_URL ..."
wget -O "$ORIGINAL_RES_ZIP" "$ORIGINAL_RES_URL" || { echo_error "Failed to download original_res.zip"; exit 1; }

# 修改部分开始：将 original_res.zip 解压到 original_res 目录
echo_info "Extracting $ORIGINAL_RES_ZIP to 'original_res' directory ..."
unzip -q "$ORIGINAL_RES_ZIP" -d "original_res" || { echo_error "Failed to extract $ORIGINAL_RES_ZIP"; exit 1; }

# 验证 extraction 是否成功
if [ ! -d "original_res" ]; then
    echo_info "'original_res' directory not found after extraction. Creating it."
    mkdir original_res
    echo_success "'original_res' directory has been created."
else
    echo_success "'original_res' directory exists."
fi

# 可选：列出解压后的目录内容以供调试
echo_info "Listing contents of 'original_res' directory:"
ls -la original_res
# 修改部分结束

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
ENV_NAME="longpibench"
PYTHON_VERSION="3.10.14"

# Check if the Conda environment already exists
if conda env list | grep -q "$ENV_NAME"; then
    echo_info "Conda environment '$ENV_NAME' already exists. Skipping creation."
else
    echo_info "Creating Conda environment '$ENV_NAME' with Python $PYTHON_VERSION ..."
    conda create -y -n "$ENV_NAME" python="$PYTHON_VERSION"
    echo_success "Conda environment '$ENV_NAME' has been created."
fi

# Activate Conda environment
echo_info "Activating Conda environment '$ENV_NAME' ..."
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

# Check if setup.py or pyproject.toml exists before installing the local package
if [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    echo_info "Installing the local package using 'pip install -e .' ..."
    pip install -e .
    echo_success "Local package has been installed in editable mode."
else
    echo_error "No setup.py or pyproject.toml found. Cannot install local package."
    exit 1
fi

echo_success "Setup completed successfully!"
echo_info "Please fill in the necessary API keys in the .env file."
