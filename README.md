# Dashboard Analisis E-Commerce Olist

Dashboard interaktif ini dikembangkan untuk menganalisis performa penjualan, tren pesanan bulanan, serta sebaran pelanggan dari dataset publik E-Commerce Olist. Proyek ini merupakan bagian dari submission kelas Belajar Fundamental Analisis Data di Dicoding.

## Daftar Pertanyaan Bisnis
1. Kategori produk apa yang menghasilkan total pendapatan tertinggi dan terendah sepanjang tahun 2017, sebagai dasar penentuan fokus promosi?
2. Bagaimana tren jumlah pesanan bulanan dari Januari 2017 hingga Agustus 2018, dan pada bulan apa terjadi lonjakan tertinggi, sebagai dasar penentuan jadwal kampanye?

## Struktur Folder Proyek
```text
submission
├───dashboard
│   ├───main_data.csv
│   └───dashboard_ecommerce.py
├───Proyek_Analisis_Data.ipynb
├───README.md
├───requirements.txt
└───url.txt
Setup Environment & Instalasi
```

Anda dapat memilih salah satu cara di bawah ini untuk menyiapkan lingkungan proyek di komputer lokal Anda:

Opsi 1: Menggunakan Anaconda (Rekomendasi)
Buka Anaconda Prompt atau terminal Anda, lalu jalankan perintah berikut:

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

Opsi 2: Menggunakan Terminal / Command Prompt Biasa
Buka terminal di direktori proyek Anda, lalu jalankan perintah:

## Setup Environment - Shell/Terminal
```
pip install -r requirements.txt
```

Cara Menjalankan Dashboard secara Lokal
-Pastikan Anda sudah berada di direktori utama (root) repository proyek ini di terminal.
-Jalankan perintah Streamlit berikut:

## Run Streamlit App
```
streamlit run dashboard/dashboard_ecommerce.py
```
