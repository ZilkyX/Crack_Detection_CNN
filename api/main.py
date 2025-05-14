from fastapi import FastAPI, File, UploadFile
import uvicorn 
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

MODEL = tf.keras.models.load_model("../models/1")
CLASS_NAMES = ['Negative', 'POSITIVE']


@app.get("/ping")
async def ping():
    return "Hello World"

def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data)).convert("RGB")
    image = image.resize((170, 227)) 
    return np.array(image)

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())

    image_batch = np.expand_dims(image, 0)

    prediction = MODEL.predict(image_batch)

    predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])

    return {
        'class' : predicted_class,
        'confidence' : float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
