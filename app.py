from flask import Flask, render_template, request, url_for
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
import uuid

app = Flask(__name__)

# Load model
model = load_model('model/fine_tuned_model.h5')

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
    image = image.resize((224, 224))          # Ukuran input model
    image = np.array(image) / 255.0           # Normalisasi
    image = image.reshape(1, 224, 224, 3)      # Tambah dimensi batch, ukuran benar
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
            # Simpan gambar ke folder static/uploads dengan nama unik
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            # Proses gambar untuk prediksi
            img = Image.open(filepath).convert('RGB')
            processed_img = preprocess_image(img)
            pred = model.predict(processed_img)[0]
            predicted_class = classes[np.argmax(pred)]
            prediction = predicted_class
            confidence = round(np.max(pred) * 100, 2)
            explanation = explanations.get(predicted_class, '')

            # URL gambar untuk ditampilkan di template
            image_url = url_for('static', filename='uploads/' + filename)

    return render_template('index.html', prediction=prediction, confidence=confidence, explanation=explanation, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
