import os

import requests
import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="MLOps HW2 - Frontend", page_icon="🤖")
st.title("ML Prediction Demo")

col1, col2, col3 = st.columns(3)
with col1:
    f1 = st.number_input("f1", value=1.0, step=0.1)
with col2:
    f2 = st.number_input("f2", value=10.0, step=1.0)
with col3:
    city = st.selectbox("city", ["a", "b", "c"])

if st.button("Predict"):
    payload = {"rows": [{"f1": f1, "f2": f2, "city": city}]}
    try:
        r = requests.post(f"{BACKEND_URL}/predict", json=payload, timeout=10)
        r.raise_for_status()
        st.success(f"Prediction: {r.json()['predictions'][0]}")
    except Exception as e:
        st.error(f"Request failed: {e}")

st.caption(f"Backend: {BACKEND_URL}")
