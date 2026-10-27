# Dashboard Analisis Data E-Commerce Olist

Dashboard interaktif ini dibuat untuk menganalisis performa penjualan, tren pesanan, serta faktor-faktor yang memengaruhi kepuasan pelanggan dari dataset E-Commerce Olist. Proyek ini merupakan bagian dari submission kelas **Belajar Fundamental Analisis Data** di Dicoding.

## Struktur Direktori
Struktur folder proyek ini diatur sebagai berikut:
```text
submission
├───dashboard
│   ├───main_data.csv
│   └───dashboard_ecommerce.py
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt

## Setup Environment - Shell / Terminal
Untuk menjalankan proyek ini secara lokal di komputer Anda, ikuti langkah-langkah berikut:

1. Clone repository ini atau unduh seluruh file proyek ke komputer lokal Anda.
2. Buka terminal atau command prompt, lalu masuk ke direktori proyek.
3. Instal seluruh library yang dibutuhkan menggunakan file requirements.txt:

pip install -r requirements.txt

## Cara Menjalankan Dashboard Streamlit

1. Pastikan Anda berada di direktori utama proyek.
2. Jalankan perintah berikut di terminal:
streamlit run dashboard/dashboard_ecommerce.py
3. Buka tautan lokal (http://localhost:8501) yang muncul di terminal melalui browser Anda.

## Catatan
-Pastikan file main_data.csv berada di dalam folder dashboard/ agar dapat terbaca dengan baik oleh script dashboard_ecommerce.py.
-Aplikasi ini mendukung filter interaktif untuk menganalisis data berdasarkan parameter tertentu.
