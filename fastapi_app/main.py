import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Query
from fastapi.responses import FileResponse
from pydantic import BaseModel

from fastapi_app.spark_predict import predict_energy
from .database import db           
from .models import Measurement    
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from datetime import datetime

app = FastAPI(title="Energy Consumption API")

# Defining paths for static files (images and css/js)
BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
IMAGES_DIR = os.path.join(BASE_DIR, "images")  # fastapi_app/images

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

# MongoDB setup
pymongo_client = MongoClient("mongodb://127.0.0.1:27017/")
pymongo_db = pymongo_client["energy_db"]
collection = pymongo_db["energy_predictions"]

# Allowinf CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500", 
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SPARK_RESULTS_PATH = os.path.join(os.path.dirname(__file__), "spark_results.json")

def load_spark_results():
    try:
        with open(SPARK_RESULTS_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Spark results file not found.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format in Spark results file.")

@app.get("/results")
def get_results():
    return load_spark_results()

# Defining input model for prediction
class PredictionInput(BaseModel):
    Temperature: float
    Humidity: float
    Wind_Speed: float
    Avg_Past_Consumption: float
    hour: int
    dayofweek: int

@app.get("/")
def root():
    # Redirect root to index.html
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    return FileResponse(index_path)

# Save predictions to MongoDB predictions collection
def save_prediction_to_mongo(pred_dict, input_data):
    doc = {
        "Temperature": input_data.Temperature,
        "Humidity": input_data.Humidity,
        "Wind_Speed": input_data.Wind_Speed,
        "Avg_Past_Consumption": input_data.Avg_Past_Consumption,
        "hour": input_data.hour,
        "dayofweek": input_data.dayofweek,
        "predicted_consumption_lr": pred_dict["LinearRegression"] * 1000,
        "predicted_consumption_rf": pred_dict["RandomForest"] * 1000,
        "created_at": datetime.utcnow()
    }
    collection.insert_one(doc)

@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        preds = predict_energy(
            input_data.Temperature,
            input_data.Humidity,
            input_data.Wind_Speed,
            input_data.Avg_Past_Consumption,
            input_data.hour,
            input_data.dayofweek
        )

        save_prediction_to_mongo(preds, input_data)

        return {
            "predicted_consumption_lr": preds["LinearRegression"],
            "predicted_consumption_rf": preds["RandomForest"]
        }
    except Exception as e:
        import traceback
        print("Prediction error:", e)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))