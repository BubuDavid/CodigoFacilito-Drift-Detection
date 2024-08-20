import pickle

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
    x1, x2 = input_data.x1, input_data.x2
    X_new = [[x1, x2]]
    predictions = model.predict(X_new)

    return {
        "message": "Prediction successful",
        "input_data": input_data.model_dump(),
        "prediction": predictions.tolist(),
    }
