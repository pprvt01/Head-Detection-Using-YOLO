# app.py
import streamlit as st
import requests
from PIL import Image
import io

st.title("Head Detection with YOLOv8")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    if st.button("Detect Heads"):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post("http://localhost:8000/detect", files=files)

        if response.status_code == 200:
            output_img = Image.open(io.BytesIO(response.content))
            st.image(output_img, caption="Detected Heads", use_container_width=True)
        else:
            st.error("Detection failed!")