# Energy Consumption Prediction Project

This project enables energy consumption prediction based on weather and historical smart meter data using Spark ML models, all accessible via a FastAPI service with a simple HTML front-end.

---

## Project Structure
```bash
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
```
  ---

## Prerequisites

- Python 3.9+
- Java OpenJDK 17 (for Spark)
- Apache Spark 3.4+  
- MongoDB installed and running locally (`mongod`)
- FastAPI (`pip install fastapi uvicorn`)
- Pandas (`pip install pandas`)
- PyMongo (`pip install pymongo`)
- PySpark (`pip install pyspark`)

---

## Project Setup

1. Start MongoDB locally:

```bash
	mongod --dbpath /path/to/your/db
```

2. Start the virtual environment that includes all the necessary packages

```bash
	source venv/bin/activate
```

3. Run setup script to resolve dependencies and start FastApi app

```bash
chmod +x setup_all.sh
bash setup_all.sh
```
   
4.	Open (Local adress)[http://127.0.0.1:8000/static/index.html] in a browser and test predictions.

## Running Spark Predictions
	•	Spark models (RandomForest and LinearRegression) are already trained and located in the models/ folder
	•	The predict_energy function in fastapi_app/spark_predict.py uses these models and normalizes features using the training dataset statistics
	•	Data does not need to be loaded from MongoDB for prediction – the CSV is used locally

  
