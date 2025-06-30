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
│   └── fine_tuned_model.h5 # (auto-downloaded if missing)
├── requirements.txt
└── README.md

```
---
##🛠️ Installation

-1. Clone the repository

git clone https://github.com/yourusername/flower-classifier.git
cd flower-classifier

-2. Install dependencies
pip install -r requirements.txt

-3. Run the app
python app.py

---

---
##💾 Model Download
he .h5 model file is too large for GitHub (>100MB).
It will be automatically downloaded from Google Drive when the app starts.

📥 Manual download link (if needed):
https://drive.google.com/file/d/1-5zytuGVuCB51ikCA3DCuT8KpGqX9HWZ/view?usp=sharing

