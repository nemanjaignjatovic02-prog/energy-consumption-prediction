from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, PolynomialExpansion
from pyspark.ml.regression import RandomForestRegressionModel, LinearRegressionModel
import numpy as np

spark = SparkSession.builder.appName("EnergyPredictAPI").getOrCreate()

# učitaj trenirane modele
rf_model = RandomForestRegressionModel.load("models/rf_model")
lr_model = LinearRegressionModel.load("models/lr_model")

# statistika iz trening skupa (mean i std za svaku kolonu)
feature_cols = ["Temperature", "Humidity", "Wind_Speed", "Avg_Past_Consumption", "hour", "dayofweek"]
feature_means = np.array([22.5, 55.0, 3.0, 250.0, 12.0, 4.0])  # primer
feature_stds  = np.array([5.0, 10.0, 1.5, 50.0, 6.0, 2.0])     # primer

def predict_energy(Temperature, Humidity, Wind_Speed, Avg_Past_Consumption, hour, dayofweek):
    # 1) Kreiraj DataFrame sa jednim redom
    data = [(Temperature, Humidity, Wind_Speed, Avg_Past_Consumption, hour, dayofweek)]
    df = spark.createDataFrame(data, feature_cols)

    # 2) Normalizuj feature-e po statistici trening skupa
    import pyspark.sql.functions as F
    for i, c in enumerate(feature_cols):
        df = df.withColumn(c, (F.col(c) - feature_means[i]) / feature_stds[i])

    # 3) VectorAssembler
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    df_features = assembler.transform(df)

    # 4) Polynomial features za Linear Regression
    poly = PolynomialExpansion(degree=2, inputCol="features", outputCol="polyFeatures")
    df_poly = poly.transform(df_features)

    # 5) Predikcije
    lr_pred = lr_model.transform(df_poly).collect()[0]["prediction"]
    rf_pred = rf_model.transform(df_features).collect()[0]["prediction"]

    # 6) Ograniči negativne vrednosti na 0
    lr_pred = max(0.0, lr_pred)
    rf_pred = max(0.0, rf_pred)

    return {
        "LinearRegression": round(float(lr_pred), 4),
        "RandomForest": round(float(rf_pred), 4)
    }