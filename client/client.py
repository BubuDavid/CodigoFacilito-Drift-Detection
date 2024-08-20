import pandas as pd
import requests

# Load the CSV file
data = None
try:
    data = pd.read_csv("client/test_data.csv")
except FileNotFoundError:
    data = pd.read_csv("test_data.csv")

if data is None:
    raise FileNotFoundError("File not found")

# Define the API endpoint
url = "http://localhost:8080/predict"  # Adjust the URL if needed

# Iterate over each row in the dataframe and send a POST request
for index, row in data.iterrows():
    # Prepare the payload for the POST request
    for key, value in row.items():
        row[key] = str(value).strip()
    payload = {
        "age": int(row["age"]),
        "workclass": row["workclass"],
        "fnlwgt": int(row["fnlwgt"]),
        "education": row["education"],
        "education_num": int(row["education-num"]),
        "marital_status": row["marital-status"],
        "occupation": row["occupation"],
        "relationship": row["relationship"],
        "race": row["race"],
        "sex": row["sex"],
        "capital_gain": int(row["capital-gain"]),
        "capital_loss": int(row["capital-loss"]),
        "hours_per_week": int(row["hours-per-week"]),
        "native_country": row["country"],
        "income": 40000 if row["income"] == "<=50K" else 60000,
        "tag": "test_no_drift"
    }

    # Send the POST request
    response = requests.post(url, json=payload)

    # Print the response from the server
    json_response = response.json()
    print(f"Prediction for row {index}: {json_response['prediction']}")
