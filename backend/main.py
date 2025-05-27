from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import cv2
import numpy as np
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")


# Load your trained model
model = YOLO("best.pt")  # Trained for head detection

@app.post("/detect/")
async def detect_heads(file: UploadFile = File(...)):
    contents = await file.read()
    temp_path = "temp.jpg"
    with open(temp_path, "wb") as f:
        f.write(contents)

    # Inference
    results = model(temp_path)[0]  # YOLOv8 returns a list
    annotated_img = results.plot()  # Numpy image with bounding boxes

    output_path = "../frontend/static/output.jpg"
    cv2.imwrite(output_path, annotated_img)

    return FileResponse(output_path, media_type="image/jpeg")

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Head Detection</title>
        </head>
        <body>
            <h2>Upload an image to detect heads</h2>
            <form action="/detect/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """