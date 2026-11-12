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

## Persiapan Environment

Sebelum menjalankan perintah instalasi atau Streamlit, buka terminal dan pindah ke **direktori utama proyek**, yaitu folder yang berisi `dashboard_ecommerce.py`, `requirements.txt`, dan file dataset.

Di Windows PowerShell, gunakan perintah berikut. Ganti path contoh dengan lokasi folder proyek di komputer Anda:

```powershell
cd "C:\path\ke\dashboard_ecommerce"
```

Contoh, jika proyek berada di folder Documents:

```powershell
cd "$HOME\Documents\dashboard_ecommerce"
```

Pastikan terminal sudah berada di direktori yang benar dengan memeriksa keberadaan file aplikasi:

```powershell
Test-Path .\dashboard_ecommerce.py
```

Hasilnya harus `True`. Jika `False`, pindah ke folder proyek yang benar sebelum melanjutkan.

## Instalasi Dependensi

Pilih salah satu opsi berikut dari direktori utama proyek.

### Opsi 1: Menggunakan Anaconda

```powershell
conda create --name main-ds python=3.9
conda activate main-ds
python -m pip install -r requirements.txt
```

### Opsi 2: Menggunakan Python

```powershell
python -m pip install -r requirements.txt
```

## Cara Menjalankan Dashboard secara Lokal

Pastikan terminal masih berada di direktori utama proyek, kemudian jalankan:

```powershell
python -m streamlit run dashboard_ecommerce.py
```

Jangan menjalankan perintah tersebut dari folder lain (misalnya folder instalasi VS Code), karena Streamlit tidak akan menemukan file `dashboard_ecommerce.py`. Alternatifnya, berikan path lengkap ke file aplikasi:

```powershell
python -m streamlit run "C:\path\ke\dashboard_ecommerce\dashboard_ecommerce.py"
```
