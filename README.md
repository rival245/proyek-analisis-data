# Dashboard Analisis E-Commerce Olist

Dashboard interaktif untuk menganalisis performa penjualan, logistik, dan kepuasan pelanggan dari dataset Olist.

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
   python -m pip install streamlit pandas matplotlib seaborn
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
