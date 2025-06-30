# BLOM
# 🌸 Flower Classifier Web App

A simple deep learning-powered web app built with **Flask** and **TensorFlow** to classify flower types from images. Upload a picture of a flower and instantly get a prediction with a short explanation.

![preview](static/logo.png)

---

## ✨ Features

- 🔍 Classifies flowers into:
  - Lily
  - Lotus
  - Orchid
  - Sunflower
  - Tulip
- 🧠 Built with a fine-tuned CNN model (`.h5`)
- 📸 Upload your own flower image
- 📜 Gives prediction + confidence + explanation
- ☁️ Auto-downloads model from Google Drive if missing

---


---

## 🧩 Project Structure

```bash
flower-classifier/
├── app.py                  # Flask application
├── templates/
│   └── index.html          # Main UI
├── static/
│   └── uploads/            # Uploaded images
├── model/
│   └── fine_tuned_model.h5 # (auto-downloaded)
├── requirements.txt
└── README.md

##🛠️ Installation
git clone https://github.com/yourusername/flower-classifier.git
cd flower-classifier

pip install -r requirements.txt

python app.py
