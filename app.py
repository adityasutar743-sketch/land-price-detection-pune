import os
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Pune Land Price Detection",
    page_icon="🏠"
)

MODEL_PATH = "models/land_price_model.pkl"

st.title("🏠 Pune Land Price Detection")
st.write("Get an estimated land price based on property details.")

if not os.path.exists(MODEL_PATH):
    st.error("Model not found. Run `python train_model.py` first.")
    st.stop()

model = joblib.load(MODEL_PATH)

localities = [
    "Baner", "Wakad", "Hinjewadi", "Kharadi", "Hadapsar",
    "Kothrud", "Aundh", "Viman Nagar", "Pimpri", "Chinchwad"
]

with st.form("prediction_form"):
    locality = st.selectbox("Locality", localities)

    area_sqft = st.number_input(
        "Land area (square feet)",
        min_value=100,
        value=1000,
        step=100
    )

    road_access = st.selectbox(
        "Road access available?",
        ["Yes", "No"]
    )

    nearby_amenities = st.selectbox(
        "Nearby amenities available?",
        ["Yes", "No"]
    )

    predict_button = st.form_submit_button("Predict Price")

if predict_button:
    input_data = pd.DataFrame({
        "locality": [locality],
        "area_sqft": [area_sqft],
        "road_access": [1 if road_access == "Yes" else 0],
        "nearby_amenities": [1 if nearby_amenities == "Yes" else 0]
    })

    prediction = model.predict(input_data)[0]

    st.success("Estimated Land Price")
    st.metric("Predicted Price", f"₹ {prediction:,.0f}")

    st.caption(
        "This is a model estimate only. Actual market prices can differ."
    )
