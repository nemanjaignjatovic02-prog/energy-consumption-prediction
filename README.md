# Energy Consumption Prediction Project

This project enables energy consumption prediction based on weather and historical smart meter data using Spark ML models, all accessible via a FastAPI service with a simple HTML front-end.

---

## 📁 Project Structure
  .
  └── energy_consumption_prediction/
      ├── data/
      │   └── smart_meter_data.csv
      ├── fastapi_app/
      │   ├── static/
      │   │   ├── lr_prediction.png
      │   │   └── rf_prediction.png
      │   ├── database.py
      │   ├── main.py
      │   ├── models.py
      │   ├── spark_predict.py
      │   ├── requirements.txt
      │   └── spark_results.json
      ├── frontend/
      │   ├── index.html
      │   ├── style.css
      │   └── script.js
      ├── models
      ├── setup/
      │   └── setup_mongo.py
      ├── venv
      ├── analysis.ipynb
      └── requirements.txt
      └── README.md

  ---

## Prerequisites

- Python 3.9+
- Java 11+ (for Spark)
- Apache Spark 3.4+  
- MongoDB installed and running locally (`mongod`)
- FastAPI (`pip install fastapi uvicorn`)
- Pandas (`pip install pandas`)
- PyMongo (`pip install pymongo`)
- PySpark (`pip install pyspark`)

---

## MongoDB Setup and CSV Data Import

1. Start MongoDB locally:

mongod --dbpath /path/to/your/db

2.	Load data from the CSV file into MongoDB:

python scripts/setup_mongo.py

This will:
	•	Create the energy_db database
	•	Create energy_measurements and energy_predictions collections if they don’t exist
	•	Clear all previous data from energy_measurements
	•	Insert data from data/smart_meter_data.csv

3.	Start FastAPI + front-end:

   uvicorn fastapi_app.main:app --reload

4.	Open (Local adress)[http://127.0.0.1:8000/static/index.html] in a browser and test predictions.

## Running Spark Predictions
	•	Spark models (RandomForest and LinearRegression) are already trained and located in the models/ folder
	•	The predict_energy function in fastapi_app/spark_predict.py uses these models and normalizes features using the training dataset statistics
	•	Data does not need to be loaded from MongoDB for prediction – the CSV is used locally

  
