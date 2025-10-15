import os
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# 1) Connect to MongoDB locally
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["energy_db"]

# Creating collections if they don't exist
if "energy_measurements" not in db.list_collection_names():
    db.create_collection("energy_measurements")
if "energy_predictions" not in db.list_collection_names():
    db.create_collection("energy_predictions")

# Loading data from CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "../data/smart_meter_data.csv")
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print(f" CSV file '{csv_path}' not found! Make sure it is in the same folder as this script file.")
    exit(1)

# Adjust column names and types if needed
rename_map = {
    "temperature": "Temperature",
    "humidity": "Humidity",
    "wind_speed": "Wind_Speed",
    "avg_past_consumption": "Avg_Past_Consumption",
    "timestamp": "Timestamp"
}
df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

# Convert Timestamp to datetime
if "Timestamp" in df.columns:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

# Put all data into MongoDB
records = df.to_dict(orient="records")
if not records:
    print("CSV file is empty or the format is invalid.")
    exit(1)

db.energy_measurements.delete_many({})
db.energy_measurements.insert_many(records)

print(f"Successfully inserted {len(records)} records into the collection 'energy_measurements'!")
print("Collections 'energy_measurements' and 'energy_predictions' are ready!")
print("MongoDB setup finished successfully.")