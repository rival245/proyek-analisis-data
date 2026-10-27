# Dashboard Analisis E-Commerce Olist

Dashboard Streamlit ini menyajikan visualisasi yang mengikuti pertanyaan bisnis dan analisis pada `Proyek_Analisis_Data.ipynb`.

## Pertanyaan analisis

1. Kategori produk apa yang menghasilkan total revenue tertinggi dan terendah sepanjang 2017?
2. Bagaimana tren jumlah pesanan bulanan dari Januari 2017 hingga Agustus 2018, dan pada bulan apa terjadi puncak pesanan?

Dashboard juga menampilkan analisis tambahan lima state dengan pelanggan terbanyak.

## Struktur file

- `dashboard_ecommerce.py` — aplikasi Streamlit
- `Proyek_Analisis_Data.ipynb` — notebook analisis proyek
- `customers_dataset.csv` — data pelanggan
- `orders_dataset.csv` — data pesanan
- `order_items_dataset.csv` — detail item pesanan
- `products_dataset.csv` — data produk
- `order_reviews_dataset.csv` — data ulasan
- `requirements.txt` — daftar dependensi Python

## Cara menjalankan

Dari folder proyek, instal dependensi:

```bash
python -m pip install -r requirements.txt
```

Kemudian jalankan dashboard:

```bash
python -m streamlit run dashboard_ecommerce.py
```

Buka URL lokal yang ditampilkan Streamlit, biasanya `http://localhost:8501`.

## Catatan perhitungan

- Revenue mengikuti notebook: penjumlahan kolom `price` pada item pesanan tahun 2017, tidak termasuk biaya pengiriman.
- Tren bulanan mencakup Januari 2017 sampai Agustus 2018 secara penuh.