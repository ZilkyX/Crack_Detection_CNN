from fastapi import FastAPI, File, UploadFile
import uvicorn 
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import requests 
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLASS_NAMES = ['Negative', 'POSITIVE']
endpoint = "http://localhost:8501/v1/models/crack_detection_model:predict"

@app.get("/ping")
async def ping():
    return {"message": "Hello World"}

def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data)).convert("RGB")
    image = image.resize((227, 170))  
    return np.array(image)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    image_batch = np.expand_dims(image, 0) 

    json_data = {
        "instances": image_batch.tolist()
    }

    response = requests.post(endpoint, json=json_data)
    prediction = response.json()

    predicted_index = int(np.argmax(prediction['predictions'][0]))
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = float(np.max(prediction['predictions'][0]))

    return {
        'class': predicted_class,
        'confidence': confidence
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
