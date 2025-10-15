#!/bin/bash

# Detect OS
OS="$(uname -s)"
echo "Detected OS: $OS"

# ---- Set JAVA_HOME ----
if [[ "$OS" == "Darwin" ]]; then
    export JAVA_HOME=$(/usr/libexec/java_home -v 17)
elif [[ "$OS" == "Linux" ]]; then
    export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
else
    echo "Unsupported OS for this script. Use Windows batch file instead."
    exit 1
fi
export PATH=$JAVA_HOME/bin:$PATH
echo "JAVA_HOME set to $JAVA_HOME"
java -version

# ---- Start MongoDB ----
DB_PATH="./data/db"
LOG_PATH="./data/mongo.log"
mkdir -p $DB_PATH
echo "Starting MongoDB..."
mongod --dbpath "$DB_PATH" --logpath "$LOG_PATH" --fork

# ---- Activate Python venv ----
if [[ "$OS" == "Darwin" || "$OS" == "Linux" ]]; then
    VENV_ACTIVATE="./venv/bin/activate"
else
    VENV_ACTIVATE="./venv/Scripts/activate"
fi

if [ ! -f "$VENV_ACTIVATE" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source "$VENV_ACTIVATE"

# ---- Install dependencies ----
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# ---- Run MongoDB setup ----
echo "Running MongoDB setup..."
python setup/setup_mongo.py

# ---- Start FastAPI app ----
echo "Starting FastAPI server..."
uvicorn fastapi_app.main:app --host 127.0.0.1 --port 8000 --reload