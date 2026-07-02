# Big Project Website

Big Project Website adalah aplikasi web berbasis Flask untuk pengelolaan informasi dan fitur edukasi terkait pengelompokan sampah. Project ini menggabungkan halaman admin, autentikasi, upload gambar, chatbot sederhana, serta model machine learning untuk mendukung fitur klasifikasi/percakapan.

## Fitur

- Halaman landing page dan dashboard admin.
- Login dan registrasi pengguna.
- Pengelolaan data warga/admin.
- Upload gambar dan riwayat data.
- Chatbot berbasis NLP.
- Model machine learning sederhana untuk fitur klasifikasi.

## Teknologi

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- TensorFlow
- NLTK
- HTML, CSS, JavaScript

## Struktur Project

```text
application/
  auth.py          # Autentikasi
  main.py          # Route utama aplikasi
  models.py        # Model database
  templates/       # Halaman HTML
  static/          # CSS, JS, gambar, dan asset UI
training.py        # Script training chatbot/model
requirements.txt   # Dependency Python
wsgi.py            # Entry point deployment
```

## Cara Menjalankan

1. Buat virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependency:

```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi:

```bash
python wsgi.py
```

## Catatan Portofolio

Project ini menunjukkan kemampuan membangun aplikasi web full-stack dengan Flask, autentikasi, database, template HTML, serta integrasi fitur NLP/machine learning sederhana.

## Deskripsi GitHub

Aplikasi web Flask untuk edukasi/pengelolaan sampah dengan dashboard admin, upload gambar, chatbot NLP, dan model machine learning sederhana.
