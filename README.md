# 📰 SentimenNews AI

Aplikasi web berbasis Laravel untuk menganalisis sentimen berita secara otomatis menggunakan model AI. Pengguna dapat membaca berita terkini dan melihat hasil analisis sentimen (positif, negatif, netral) dari setiap artikel.

---

## 🛠️ Tech Stack

- **Frontend:** Blade Template, CSS, Vite
- **Backend:** Laravel 11 (PHP)
- **Database:** PostgreSQL (via Neon.tech)
- **AI Service:** Python (Hugging Face Space — `abdcharis-sentimen-analisis-api`)
- **Session & Queue:** Database driver
- **Deployment:** Railway

---

## 📁 Struktur Folder

```
sentimen-news/
├── ai-service/          ← Service Python untuk analisis sentimen
├── app/                 ← Logic Laravel (Controllers, Models, dll)
├── bootstrap/           ← Bootstrap aplikasi Laravel
├── config/              ← Konfigurasi Laravel
├── database/            ← Migrations & Seeders
├── public/              ← Asset publik
├── resources/           ← Views (Blade), CSS, JS
├── routes/              ← Definisi routing web & API
├── storage/             ← File storage & logs
├── tests/               ← Unit & Feature tests
├── .env.example         ← Template environment variable
├── .gitignore
├── artisan              ← CLI Laravel
├── composer.json        ← Dependencies PHP
├── package.json         ← Dependencies JS
└── vite.config.js
```

---

## ⚙️ Petunjuk Setup (Local Development)

### Prasyarat
- PHP >= 8.2
- Composer
- Node.js >= 18
- PostgreSQL (atau gunakan koneksi Neon.tech)

### Langkah Instalasi

```bash
# 1. Clone repository
git clone https://github.com/dotcomspace/sentimen-news.git
cd sentimen-news

# 2. Install dependencies PHP
composer install

# 3. Install dependencies JavaScript
npm install

# 4. Salin file environment
copy .env.example .env

# 5. Isi variabel di .env (lihat bagian Environment Variables)

# 6. Generate application key
php artisan key:generate

# 7. Jalankan migrasi database
php artisan migrate

# 8. Build asset frontend
npm run build

# 9. Jalankan server
php artisan serve
```

Buka browser di `http://localhost:8000`

---

## 🔐 Environment Variables

Salin `.env.example` ke `.env`, lalu isi variabel berikut:

```env
APP_NAME="SentimenNews AI"
APP_ENV=local
APP_KEY=          ← generate dengan: php artisan key:generate
APP_DEBUG=true
APP_URL=http://localhost:8000

# URL AI Service (Hugging Face)
AI_API_URL=https://abdcharis-sentimen-analisis-api.hf.space

# Koneksi Database PostgreSQL
DB_CONNECTION=pgsql
DB_HOST=          ← host database kamu
DB_PORT=5432
DB_DATABASE=      ← nama database
DB_USERNAME=      ← username database
DB_PASSWORD=      ← password database
DB_SSLMODE=require
```

> **Penting:** Jangan pernah meng-upload file `.env` yang berisi password asli ke repository.

---

## 🤖 AI Service (Python)

Model analisis sentimen di-host di Hugging Face Space. Source code-nya ada di folder `ai-service/`.

- **Endpoint:** `https://abdcharis-sentimen-analisis-api.hf.space`
- **Input:** Teks artikel berita
- **Output:** Label sentimen (`positif` / `negatif` / `netral`) beserta skor kepercayaan

Untuk menjalankan AI service secara lokal:

```bash
cd ai-service
pip install -r requirements.txt
uvicorn main_api:app --host 0.0.0.0 --port 8001
```

Kemudian hapus `AI_API_URL` di `.env`.

---

## ✅ Fitur Utama

- 📖 Membaca berita dari berbagai sumber
- 🤖 Analisis sentimen otomatis tiap artikel (Positif / Negatif / Netral)
- 📊 Dashboard ringkasan sentimen berita
- 👤 Autentikasi pengguna (register & login)
- 🗄️ Riwayat berita yang telah dianalisis

---

## 🧪 Menjalankan Tests

```bash
php artisan test
```

---

## 🚀 Deployment

Aplikasi ini di-deploy ke [Railway](https://railway.app). URL produksi:  
`https://sentimen-news-production.up.railway.app/`

---

## 👥 Anggota Tim

| Nama | Role |
|------|------|
| Abdul Charis Al Fikri | Backend Developer & Deployment |
| Muhammad Aldhan Yusuf | Frontend Developer |
| Gamaliel Christian Widodo | ML / AI Engineer |
| Benhard A Simamora | ML / AI Engineer |
| Herlianeka Pratiwi | Database |
| Syafiatur Rohmah | Database | 

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan Capstone Project — Coding Camp powered by DBS Foundation.
