# 🧠 AI Backend - EcoNomic Sentiment Analyzer

Repositori ini memuat seluruh *source code*, model *Deep Learning*, dan konfigurasi API untuk modul Kecerdasan Buatan (AI) pada platform **EcoNomic**. Modul ini berfungsi untuk memproses teks berita ekonomi yang dikirim oleh Frontend (Laravel) dan mengembalikan hasil prediksi sentimen serta rangkuman teks.

## ⚙️ Spesifikasi Model & Tech Stack
* **Framework Utama:** TensorFlow, Keras 3
* **Arsitektur Model:** Bidirectional LSTM (Long Short-Term Memory) dengan *Custom Attention Layer*.
* **Metode Pelatihan:** *Custom Training Loop* menggunakan `tf.GradientTape` dan dimonitor melalui **TensorBoard**.
* **API Framework:** FastAPI & Uvicorn
* **Generative AI:** Google Gemini API (fitur sekunder untuk *Summarization*)
* **Deployment / Tunneling:** Google Colab & Ngrok

## 📂 Struktur Repositori
* `main_api.py` - Skrip utama FastAPI yang berisi logika *inference* dan konfigurasi *endpoint*.
* `economic_sentiment_model.keras` - File model Deep Learning yang sudah dilatih secara penuh (Akurasi >85%).
* `tokenizer.pkl` - File kamus tokenisasi untuk mengubah teks berita menjadi sekuens angka yang dipahami model.
* `Notebook_Training_Deployment.ipynb` - Dokumen Jupyter Notebook proses *preprocessing*, *training loop*, hingga metrik evaluasi.

## 🚀 Cara Menjalankan Server AI (Inference)
Karena model Deep Learning membutuhkan komputasi yang intensif, backend AI ini dijalankan di Google Colab dan diekspos ke internet menggunakan Ngrok agar bisa ditembak oleh Laravel.

1. Buka file `Notebook_Training_Deployment.ipynb` di Google Colab.
2. Unggah file `economic_sentiment_model.keras` dan `tokenizer.pkl` ke dalam penyimpanan sesi Colab.
3. Jalankan sel kode inisialisasi Ngrok dan masukkan token autentikasi Anda:
   ```python
   ngrok.set_auth_token("TOKEN_NGROK_ANDA")
4. Jalankan seluruh sel kode (Run All).
5. Salin URL publik Ngrok yang muncul di log paling bawah (misal: https://xxxx.ngrok-free.dev). URL ini adalah Base URL yang harus dimasukkan ke konfigurasi .env Laravel.

📡 Panduan REST API (Endpoints)
Dokumentasi interaktif Swagger UI dapat diakses secara langsung dengan menambahkan rute /docs pada URL Ngrok yang sedang aktif.

1. POST /predict
- Kegunaan: Mengklasifikasikan teks berita ekonomi ke dalam kategori sentimen.
- Format Request Body (JSON):

JSON
{
  "teks_berita": "Teks berita ekonomi yang ingin diuji..."
}

- Format Response (JSON): Mengembalikan label sentimen (Positif, Negatif, atau Netral) beserta skor kepercayaan (confidence score).

2. POST /analyze-and-summarize
- Kegunaan: Mendeteksi arah sentimen sekaligus menghasilkan poin-poin ringkasan berita menggunakan Gemini API.
- Format Request Body (JSON): Sama seperti /predict.

🛑 Catatan Penting untuk Integrasi:
Setiap permintaan HTTP dari aplikasi Frontend (Laravel) wajib menyertakan header 'ngrok-skip-browser-warning': 'true' agar komunikasi data tidak terhambat oleh halaman peringatan standar dari Ngrok.

Developed by Benhard Simamora dan Gamaliel (Machine Learning Engineer)
