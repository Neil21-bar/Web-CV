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

# Detail bunga
flower_details = {
    'Lily': {
        'habitat': 'Tumbuh di daerah beriklim sedang dan dingin, di tanah yang gembur dan memiliki drainase baik.',
        'age': '1–2 minggu sejak mekar, tergantung jenis dan kondisi lingkungan.',
        'regions': 'Asia Timur (Jepang, Korea, Tiongkok), Eropa, dan Amerika Utara.Di Indonesia, sering dibudidayakan di dataran tinggi (Bandung, Lembang, Batu).'
    },
    'Lotus': {
        'habitat': 'Perairan dangkal dan rawa-rawa.',
        'age': '3–5 hari mekar penuh, lalu menutup dan gugur. Tapi tanaman ini bisa berbunga terus saat musimnya.',
        'regions': 'Asia Selatan dan Asia Tenggara.'
    },
    'Orchid': {
        'habitat': 'Mayoritas adalah epifit (tumbuh menempel pada pohon), menyukai lingkungan lembap, teduh, dan sirkulasi udara baik.',
        'age': '1–3 bulan untuk spesies tertentu (misalnya Phalaenopsis), tapi bisa lebih pendek pada jenis liar',
        'regions': 'Amerika Selatan dan Asia Tenggara.'
    },
    'Sunflower': {
        'habitat': 'Ladang terbuka, tanah lempung berpasir, daerah panas dengan sinar matahari penuh.',
        'age': 'Bunga Sunflower biasanya bertahan 2-3 minggu sejak mekar.',
        'regions': 'Amerika Utara dan Selatan.'
    },
    'Tulip': {
        'habitat': 'Daerah beriklim sedang dengan musim dingin yang jelas.',
        'age': 'Bunga Tulip biasanya bertahan 1-2 minggu.',
        'regions': 'Eropa dan Asia Tengah.'
    }
}

@app.route('/detail/<flower_name>')
def detail(flower_name):
    details = flower_details.get(flower_name)
    if not details:
        return "Detail bunga tidak ditemukan", 404
    return render_template('detail.html', flower_name=flower_name, details=details)

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
    detail_url = None

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
            confidence = round(np.max(pred) * 100, 2)

            if confidence < 85:
                prediction = "diluar kategori"
                explanation = ""
                detail_url = None
            else:
                prediction = predicted_class
                explanation = explanations.get(predicted_class, '')

                # Tambahkan URL ke halaman detail bunga
                detail_url = url_for('detail', flower_name=predicted_class)
            # URL gambar untuk ditampilkan di template
            image_url = url_for('static', filename='uploads/' + filename)

    return render_template('index.html', prediction=prediction, confidence=confidence, explanation=explanation, image_url=image_url, detail_url=detail_url)

if __name__ == '__main__':
    app.run(debug=True)
