import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Air Pollution Predictor", layout="centered")

st.title("🌫 Air Pollution Predictor (PM2.5)")
st.markdown("Predict PM2.5 levels using pollution and time data")

st.divider()

# Inputs
pm10 = st.slider("PM10 (µg/m³)", 0, 500, 100)
no2 = st.slider("NO2 (µg/m³)", 0, 200, 30)
co = st.slider("CO (mg/m³)", 0.0, 10.0, 1.0)

hour = st.slider("Hour of Day", 0, 23, 12)
month = st.slider("Month", 1, 12, 6)
day_of_week = st.slider("Day of Week (0=Mon)", 0, 6, 3)

pm25_lag1 = st.slider("Previous Hour PM2.5", 0, 500, 120)

st.divider()

if st.button("Predict PM2.5"):
    input_data = np.array([[pm10, no2, co, hour, month, day_of_week, pm25_lag1]])
    prediction = model.predict(input_data)[0]

    st.success(f"Predicted PM2.5: {prediction:.2f} µg/m³")

    # AQI interpretation
    if prediction <= 50:
        st.info("🟢 Good")
    elif prediction <= 100:
        st.info("🟡 Moderate")
    elif prediction <= 200:
        st.warning("🟠 Unhealthy")
    else:
        st.error("🔴 Very Unhealthy")