import streamlit as st
import pickle
import numpy as np
import os

# Load model (robust way)
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "model.pkl")
model = pickle.load(open(model_path, "rb"))

st.set_page_config(page_title="Air Pollution Predictor", layout="centered")

# Title
st.title("🌫 Air Pollution Predictor")
st.markdown("### Predict PM2.5 levels using real-world CPCB data")

st.divider()

# Sidebar (better UX)
st.sidebar.header("📊 Input Parameters")

pm10 = st.sidebar.slider("PM10 (µg/m³)", 0, 500, 150)
no2 = st.sidebar.slider("NO2 (µg/m³)", 0, 200, 40)
co = st.sidebar.slider("CO (mg/m³)", 0.0, 10.0, 1.5)

hour = st.sidebar.slider("Hour", 0, 23, 12)
month = st.sidebar.slider("Month", 1, 12, 6)
day_of_week = st.sidebar.slider("Day of Week", 0, 6, 3)

pm25_lag1 = st.sidebar.slider("Previous PM2.5", 0, 500, 120)

st.divider()

# Predict
if st.button("🚀 Predict PM2.5"):
    input_data = np.array([[pm10, no2, co, hour, month, day_of_week, pm25_lag1]])
    prediction = model.predict(input_data)[0]

    st.subheader(f"Predicted PM2.5: {prediction:.2f} µg/m³")

    # AQI Status
    if prediction <= 50:
        st.success("🟢 Good")
    elif prediction <= 100:
        st.info("🟡 Moderate")
    elif prediction <= 200:
        st.warning("🟠 Unhealthy")
    else:
        st.error("🔴 Very Unhealthy")

    # Progress bar visualization
    st.progress(min(int(prediction / 500 * 100), 100))

st.divider()

st.markdown("📌 Model: XGBoost | Dataset: CPCB India | Features: Pollution + Time + Lag")