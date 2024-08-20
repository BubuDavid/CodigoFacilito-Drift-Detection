import pickle
import time

from fastapi import FastAPI
from middleware import LogstashMiddleware
from schemas import InputBody

# FastAPI application
app = FastAPI()

# Adding middleware to the FastAPI application
app.add_middleware(LogstashMiddleware)

# Model Configuration
with open("model.pkl", "rb") as file:
    model = pickle.load(file)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application"}


@app.post("/predict")
async def predict_model(input_data: InputBody):
    x_data = input_data.transform()

    features = [
        x_data["age"],
        x_data["fnlwgt"],
        x_data["education_num"],
        x_data["marital_status"],
        x_data["relationship"],
        x_data["race"],
        x_data["sex"],
        x_data["capital_gain"],
        x_data["capital_loss"],
        x_data["hours_per_week"],
        x_data["country"],
        x_data["employment_type"],
    ]

    prediction = model.predict([features])

    prediction_result = "Income > 50K" if prediction[0] == 0 else "Income <= 50K"
    real_income = "Income > 50K" if x_data["income"] == 0 else "Income <= 50K"

    return {
        "message": "Prediction successful",
        "input_data": input_data.model_dump(),
        "prediction": prediction_result,
        "real_income": real_income,
        "tag": input_data.tag,
    }
