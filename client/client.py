import numpy as np
from scipy.stats import multivariate_normal


def true_model(X, slope=-1):
    z = slope * X[:, 0]
    idx = np.argwhere(X[:, 1] > z)
    y = np.zeros(X.shape[0])
    y[idx] = 1
    return y


true_slope = -1

# Reference distribution
sigma = 0.8
phi1 = 0.5
phi2 = 0.5
ref_norm_0 = multivariate_normal([-1, -1], np.eye(2) * sigma**2)  # type: ignore
ref_norm_1 = multivariate_normal([1, 1], np.eye(2) * sigma**2)  # type: ignore

# Reference data (to initialise the detectors)
N_ref = 240
X_0 = ref_norm_0.rvs(size=int(N_ref * phi1), random_state=1)
X_1 = ref_norm_1.rvs(size=int(N_ref * phi2), random_state=1)
X_ref = np.vstack([X_0, X_1])
y_ref = true_model(X_ref, true_slope)

# Training data (to train the classifer)
N_train = 240
X_0 = ref_norm_0.rvs(size=int(N_train * phi1), random_state=0)
X_1 = ref_norm_1.rvs(size=int(N_train * phi2), random_state=0)
X_train = np.vstack([X_0, X_1])
y_train = true_model(X_train, true_slope)

# Test No Drift
N_test = 120
X_0 = ref_norm_0.rvs(size=int(N_test * phi1), random_state=2)
X_1 = ref_norm_1.rvs(size=int(N_test * phi2), random_state=2)
X_test = np.vstack([X_0, X_1])

# Send data to the server to predict, the predictions are 1 by 1
import requests as req

url = "http://localhost:8080/predict"
predictions = []
for i in range(N_test):
    x1, x2 = X_test[i]
    data = {"x1": x1, "x2": x2, "tag": "test_no_drift"}
    response = req.post(url, json=data)
    json_response = response.json()
    prediction = json_response["prediction"]
    predictions.append(prediction)

# Test Drift
shift_norm_0 = multivariate_normal([2, -4], np.eye(2) * sigma**2)  # type: ignore
X_0 = shift_norm_0.rvs(size=int(N_test * phi1), random_state=2)
X_1 = ref_norm_1.rvs(size=int(N_test * phi2), random_state=2)
X_test = np.vstack([X_0, X_1])

# Check for drift in covariates
predictions = []
for i in range(N_test):
    x1, x2 = X_test[i]
    data = {"x1": x1, "x2": x2, "tag": "test_drift"}
    response = req.post(url, json=data)
    prediction = response.json()["prediction"]
    predictions.append(prediction)
