from flask import Flask, render_template, request, url_for
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
import uuid
import gdown

app = Flask(__name__)

# === Unduh model dari Google Drive jika belum ada ===
model_path = 'model/fine_tuned_model.h5'
if not os.path.exists(model_path):
    os.makedirs('model', exist_ok=True)
    drive_file_id = '1-5zytuGVuCB51ikCA3DCuT8KpGqX9HWZ'
    url = f'https://drive.google.com/uc?id={drive_file_id}'
    gdown.download(url, model_path, quiet=False)

# Load model
model = load_model(model_path)

# Daftar label
classes = ['Lily', 'Lotus', 'Orchid', 'Sunflower', 'Tulip']

# Penjelasan bunga
explanations = {
    'Lily': 'Lily adalah bunga yang melambangkan kemurnian dan keindahan.',
    'Lotus': 'Lotus adalah bunga yang sering melambangkan pencerahan dan kesucian.',
    'Orchid': 'Orchid adalah bunga yang dikenal dengan keindahan dan keanggunannya.',
    'Sunflower': 'Sunflower adalah bunga yang melambangkan kebahagiaan dan energi positif.',
    'Tulip': 'Tulip adalah bunga yang melambangkan cinta dan kehangatan.'
}

# Preprocessing gambar
def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = image.reshape(1, 224, 224, 3)
    return image

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = None
    explanation = None
    image_url = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            img = Image.open(filepath).convert('RGB')
            processed_img = preprocess_image(img)
            pred = model.predict(processed_img)[0]
            predicted_class = classes[np.argmax(pred)]
            prediction = predicted_class
            confidence = round(np.max(pred) * 100, 2)
            explanation = expl
