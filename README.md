# Capstone-Project
Pengerjaan Project TIM CC26-PSU386
# 📊 SentiVest — Platform Analisis Sentimen Berita Ekonomi
> Big Bank Sentiment & Investment Signal Dashboard

---

## 📌 Deskripsi Proyek

**SentiVest** adalah platform analisis sentimen berbasis berita ekonomi yang dirancang untuk membantu investor memahami kondisi pasar saham perbankan besar di Indonesia (IDX). Sistem ini mengumpulkan berita dari Google News, menganalisis sentimen teks secara otomatis, menggabungkannya dengan data harga saham historis, lalu menyajikan hasilnya dalam dashboard interaktif berbasis Streamlit.

---

## 🏗️ Struktur Proyek

```
├── dashboard.py          # Aplikasi dashboard Streamlit (SentiVest)
├── Readme.md             # Tata cara menjalankan proyek
├── requirements.txt      # Daftar dependensi Python
└── Dataset/
    ├── berita.py         # Scraper berita dari Google News RSS
    └── mainn.py          # Pipeline: sentimen + data saham + pembuatan dataset final
```

---

## ⚙️ Cara Kerja

### 1. Pengumpulan Data Berita (`Dataset/berita.py`)
- Mengambil berita dari **Google News RSS** menggunakan kata kunci per ticker saham
- Mendukung **15 ticker saham** IDX (BBCA, BBRI, BMRI, BBNI, TLKM, ASII, UNVR, ICBP, INDF, ANTM, ADRO, PTBA, GOTO, AMRT, KLBF)
- Rentang data: **2024 – 2026**, dibagi per kuartal
- Output: `data/berita.csv`

### 2. Pemrosesan & Pembuatan Dataset (`Dataset/mainn.py`)
- **Analisis Sentimen** berbasis kamus kata (Bahasa Indonesia):
  - Kata positif: *naik, menguat, tumbuh, laba, dividen, ekspansi*, dll.
  - Kata negatif: *turun, anjlok, rugi, tekanan, merosot*, dll.
  - Skor: `+0.6` (positif), `-0.6` (negatif), `0.0` (netral)
- **Download data harga saham** via `yfinance` (BBCA, BBRI, BMRI, BBNI)
- **Target Label** dibuat dari pergerakan harga keesokan hari (`1` = naik, `0` = turun)
- **Merge** berita + saham berdasarkan tanggal & ticker
- Output: `output/final_dataset.csv`

### 3. Dashboard Interaktif (`dashboard.py`)
- Dibangun dengan **Streamlit** dan **Plotly**
- Dataset dimuat dari GitHub repository secara langsung

---

## 📊 Fitur Dashboard

| Fitur | Deskripsi |
|---|---|
| **Sinyal Rekomendasi** | BUY / HOLD / SELL berdasarkan MA5 sentimen |
| **KPI Cards** | Harga penutupan, MA5 sentimen, total berita, dominasi label |
| **Chart Harga vs Sentimen** | Perbandingan harga saham & sentimen harian (30 hari) |
| **Distribusi Sentimen** | Pie chart Positif / Netral / Negatif |
| **Volume Perdagangan** | Bar chart volume dengan gradasi warna sentimen |
| **Berita Positif per Ticker** | Horizontal bar chart + rata-rata harga (2026) |
| **Proporsi Target Label** | Stacked bar per kategori sentimen |
| **Sinyal Semua Ticker** | Kartu sinyal untuk seluruh ticker sekaligus |
| **Tabel Berita Terbaru** | 15 berita terbaru dengan label sentimen & skor |

### Filter Sidebar
- Pilihan **Ticker Saham**
- **Rentang Tanggal** (dari – sampai)
- **Kategori Sentimen** (Semua / Positif / Netral / Negatif)

---

## 🚀 Instalasi & Menjalankan

### Prasyarat
- Python 3.9+
- pip

### Langkah-langkah

```bash
# 1. Clone repository branch DS
git clone -b DS https://github.com/Benhard121/Capstone-Project.git
cd Capstone-Project

# 2. (Opsional) Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Install dependensi
pip install -r requirements.txt
```

**4. Kumpulkan data berita dari Google News**
```bash
python Dataset/berita.py
```
> Menghasilkan file `data/berita.csv` berisi berita per ticker saham.

**5. Proses sentimen & gabungkan dengan data saham**
```bash
python Dataset/mainn.py
```
> Menghasilkan file `output/final_dataset.csv` yang siap digunakan dashboard.

**6. (Opsional) Eksplorasi data di Notebook**

Buka file `notebook.ipynb` menggunakan Jupyter Notebook atau VS Code untuk melihat proses analisis data secara lengkap.

```bash
jupyter notebook notebook.ipynb
```

**7. Jalankan dashboard**
```bash
streamlit run dashboard.py
```

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`.
---

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`.

## 🛠️ Teknologi yang Digunakan

| Kategori | Library |
|---|---|
| Dashboard UI | `streamlit`, `plotly` |
| Manipulasi Data | `pandas`, `numpy` |
| Data Saham | `yfinance` |
| Scraping Berita | `feedparser` |
| Machine Learning (opsional) | `scikit-learn` |
| Visualisasi Tambahan | `matplotlib`, `seaborn` |

---

## 📈 Ticker Saham yang Didukung

| Ticker | Perusahaan |
|---|---|
| BBCA.JK | Bank Central Asia |
| BBRI.JK | Bank Rakyat Indonesia |
| BMRI.JK | Bank Mandiri |
| BBNI.JK | Bank Negara Indonesia |
| TLKM.JK | Telkom Indonesia |
| ASII.JK | Astra International |
| UNVR.JK | Unilever Indonesia |
| ICBP.JK | Indofood CBP |
| INDF.JK | Indofood |
| ANTM.JK | Aneka Tambang |
| ADRO.JK | Adaro Energy |
| PTBA.JK | Bukit Asam |
| GOTO.JK | GoTo |
| AMRT.JK | Alfamart |
| KLBF.JK | Kalbe Farma |

> Dashboard saat ini menampilkan sinyal untuk **BBCA, BBRI, BMRI, BBNI** (sesuai dataset final yang tersedia).

---

## 📁 Format Dataset Final

File `final_dataset.csv` memiliki kolom berikut:

| Kolom | Tipe | Keterangan |
|---|---|---|
| `Tanggal` | Date | Tanggal berita & perdagangan |
| `Ticker` | String | Kode saham (misal: `BBCA.JK`) |
| `Teks_Berita` | String | Judul berita |
| `Nilai_Sentimen` | Float | Skor sentimen (`-0.6`, `0.0`, `+0.6`) |
| `Harga_Penutupan_Saham` | Float | Harga penutupan (IDR) |
| `Volume` | Integer | Volume perdagangan |
| `Target_Label` | Integer | `1` = harga naik esok hari, `0` = turun |

---

## 👤 Informasi Proyek

- **Kode Proyek:** CC26-PSU386  
- **Tim:** Pengerjaan Project TIM CC26-PSU386  
- **Repository:** [Benhard121/Capstone-Project](https://github.com/Benhard121/Capstone-Project) · branch `DS`  
- **Platform:** Dicoding Capstone Project  
- **Sumber Data Berita:** Google News RSS (Bahasa Indonesia)  
- **Sumber Data Saham:** Yahoo Finance (`yfinance`)
