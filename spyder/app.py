import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Salary Prediction App", page_icon="💰")

# File names
DATA_FILE = "Salary_Data.csv"
MODEL_FILE = "linear_regression_model.pkl"

# -----------------------------
# Train model if not exists
# -----------------------------
if not os.path.exists(MODEL_FILE):

    data = pd.read_csv(DATA_FILE)

    X = data[['YearsExperience']]
    y = data['Salary']

    model = LinearRegression()
    model.fit(X, y)

    # SAVE MODEL (binary mode)
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

else:
    # LOAD MODEL (binary mode)
    with open(MODEL_FILE, "rb") as f:
        model = pickle.load(f)

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("💼 Salary Prediction App")
st.write("Predict Salary based on Years of Experience")

years = st.number_input(
    "Enter Years of Experience:",
    min_value=0.0,
    max_value=50.0,
    value=1.0,
    step=0.5
)

if st.button("Predict Salary"):
    prediction = model.predict(np.array([[years]]))
    st.success(f"💰 Predicted Salary: ₹ {prediction[0]:,.2f}")

st.caption("Model: Simple Linear Regression")
