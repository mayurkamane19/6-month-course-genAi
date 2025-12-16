import streamlit as st
import pickle
import numpy as np
import os

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Salary Prediction App",
    page_icon="💰",
    layout="centered"
)

# ===============================
# MODEL PATH (FINAL CONFIRMED)
# ===============================
MODEL_PATH = r"C:\Users\santo\OneDrive\Desktop\Data science\Dec2025\Salary Prediction app\linear_regression_model.pkl"

# ===============================
# LOAD MODEL (SAFE CHECK)
# ===============================
if not os.path.exists(MODEL_PATH):
    st.error("❌ Model file not found. Please check the path.")
    st.stop()

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

# ===============================
# UI
# ===============================
st.title("💰 Salary Prediction App")
st.write("Predict employee salary based on **Years of Experience**")

st.markdown("---")

# Input
experience = st.number_input(
    "Enter Years of Experience",
    min_value=0.0,
    max_value=50.0,
    step=0.5
)

# Predict
if st.button("Predict Salary"):
    input_data = np.array([[experience]])
    prediction = model.predict(input_data)

    st.success(f"💵 Predicted Salary: ₹ {int(prediction[0]):,}")

st.markdown("---")
st.caption("Built with Python • Machine Learning • Streamlit")
