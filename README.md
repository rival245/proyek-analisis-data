# Dashboard Analisis E-Commerce Olist

Dashboard interaktif untuk menganalisis performa penjualan, logistik, dan kepuasan pelanggan dari dataset Olist.

## Pertanyaan Bisnis
1. Kategori produk apa yang menghasilkan total pendapatan tertinggi dan terendah sepanjang tahun 2017, sebagai dasar penentuan fokus promosi?
2. Bagaimana tren jumlah pesanan bulanan dari Januari 2017 hingga Agustus 2018, dan pada bulan apa terjadi lonjakan tertinggi, sebagai dasar penentuan jadwal kampanye?

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

## Fitur
- Dashboard utama dengan visualisasi produk dan performa bisnis
- Filter berdasarkan tahun dan state pelanggan
- Analisis revenue per kategori produk
- Analisis hubungan keterlambatan pengiriman dengan review score
- Tren pesanan bulanan
- Top negara bagian pelanggan

## Struktur File
- `dashboard_ecommerce.py` — aplikasi Streamlit utama
- `customers_dataset.csv` — data pelanggan
- `orders_dataset.csv` — data pesanan
- `order_items_dataset.csv` — detail item dari pesanan
- `products_dataset.csv` — data produk
- `order_reviews_dataset.csv` — data review pelanggan

## Cara Menjalankan
1. Pastikan Python sudah terinstal.
2. Instal dependensi:
   ```bash
   python -m pip install streamlit pandas
   ```
3. Jalankan aplikasi:
   ```bash
   python -m streamlit run dashboard_ecommerce.py
   ```
4. Buka URL yang ditampilkan di browser, biasanya:
   ```text
   http://localhost:8501
   ```

## Catatan
- Dashboard sudah dikonfigurasi agar membaca file CSV dari folder yang sama dengan script.
- Aplikasi mendukung filter interaktif untuk analisis yang lebih detail.
