#!/bin/bash

# ---- 0️⃣ Set JAVA_HOME for Spark ----
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export PATH=$JAVA_HOME/bin:$PATH
echo "JAVA_HOME set to $JAVA_HOME"
java -version

# ---- 1️⃣ Start MongoDB ----
echo "Starting MongoDB..."
mongod --dbpath ./data/db --logpath ./data/mongo.log --fork

# ---- 2️⃣ Activate Python venv ----
echo "Activating virtual environment..."
source ./venv/bin/activate

# ---- 3️⃣ Run MongoDB setup script ----
echo "Running MongoDB setup..."
python setup/setup_mongo.py

# ---- 4️⃣ Start FastAPI app with Uvicorn ----
echo "Starting FastAPI server..."
uvicorn fastapi_app.main:app --host 127.0.0.1 --port 8000 --reload