import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

model = load_model("model/waste_model.h5")

classes = ['cardboard','glass','metal','paper','plastic','trash']

def predict_image(path):
    img = Image.open(path).convert("RGB")
    img = img.resize((224,224))

    arr = np.array(img)/255.0
    arr = np.expand_dims(arr, axis=0)

    pred = model.predict(arr)
    return classes[np.argmax(pred)], float(np.max(pred)), pred[0]