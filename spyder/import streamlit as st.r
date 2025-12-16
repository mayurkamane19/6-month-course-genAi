import streamlit as st
import pickle
import numpy as np

# Load trained model
model = pickle.load(open(
    r'C:\Users\Admin\AVSCODE\15. Machine Learnin\1.Regression\slr\linear_regression_model.pkl',
    'rb'
))

st.set_page_config(page_title="Salary Predictor", page_icon="💰")

st.title("💼 Salary Prediction App")
st.write(
    "This app predicts **Salary based on Years of Experience** "
    "using a **Simple Linear Regression** model."
)

# User input
years_experience = st.number_input(
    "Enter Years of Experience:",
    min_value=0.0,
    max_value=50.0,
    value=1.0,
    step=0.5
)

# Prediction
if st.button("Predict Salary"):
    experience_input = np.array([[years_experience]])
    prediction = model.predict(experience_input)

    st.success(
        f"💰 Predicted Salary for **{years_experience} years** experience is:\n"
        f"### ₹ {prediction[0]:,.2f}"
    )

st.markdown("---")
st.caption("📊 Model: Simple Linear Regression")
st.caption("👨‍💻 Built by: Prakash Senapati")
