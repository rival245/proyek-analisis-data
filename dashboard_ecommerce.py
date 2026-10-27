from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
MONTHLY_START = pd.Timestamp("2017-01-01")
MONTHLY_END = pd.Timestamp("2018-09-01")

st.set_page_config(
    page_title="Analisis E-Commerce Olist",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data():
    customers_df = pd.read_csv(BASE_DIR / "customers_dataset.csv")
    orders_df = pd.read_csv(BASE_DIR / "orders_dataset.csv")
    order_items_df = pd.read_csv(BASE_DIR / "order_items_dataset.csv")
    products_df = pd.read_csv(BASE_DIR / "products_dataset.csv")

    orders_df["order_purchase_timestamp"] = pd.to_datetime(
        orders_df["order_purchase_timestamp"], errors="coerce"
    )
    return customers_df, orders_df, order_items_df, products_df


customers_df, orders_df, order_items_df, products_df = load_data()

with st.sidebar:
    st.header("Informasi proyek")
    st.caption("Dashboard untuk Proyek Analisis Data Dicoding — E-Commerce Public Dataset.")
    st.markdown(
        """
        **Cakupan analisis utama**
        - Revenue kategori produk: tahun 2017
        - Tren pesanan: Januari 2017–Agustus 2018

        Filter di bawah hanya berlaku untuk analisis tambahan pelanggan.
        """
    )
    available_states = sorted(customers_df["customer_state"].dropna().unique())
    selected_states = st.multiselect(
        "Pilih state pelanggan",
        options=available_states,
        default=available_states,
        help="Tidak mengubah hasil untuk dua pertanyaan analisis utama.",
    )

st.title("Analisis Data E-Commerce Olist")
st.markdown(
    "Dashboard ini menyajikan hasil analisis proyek: pendapatan kategori produk "
 "tahun 2017, tren pesanan Januari 2017–Agustus 2018, dan distribusi pelanggan."
)

orders_2017 = orders_df.loc[
    orders_df["order_purchase_timestamp"].dt.year.eq(2017)
]
orders_items_2017 = orders_2017.merge(order_items_df, on="order_id", how="inner")
complete_order_2017 = orders_items_2017.merge(
    products_df, on="product_id", how="inner"
)

revenue_by_category = (
    complete_order_2017.groupby("product_category_name")["price"]
    .sum()
    .sort_values(ascending=False)
    .rename("revenue")
    .rename_axis("product_category_name")
    .reset_index()
)
top_categories = revenue_by_category.head(5).sort_values("revenue")
lowest_categories = revenue_by_category.tail(5).sort_values("revenue")

monthly_orders_data = orders_df.loc[
    orders_df["order_purchase_timestamp"].ge(MONTHLY_START)
    & orders_df["order_purchase_timestamp"].lt(MONTHLY_END)
].copy()
monthly_orders_data["year_month"] = (
    monthly_orders_data["order_purchase_timestamp"].dt.to_period("M").astype(str)
)
monthly_orders = (
    monthly_orders_data.groupby("year_month")["order_id"]
    .count()
    .reindex(
        pd.period_range("2017-01", "2018-08", freq="M").astype(str),
        fill_value=0,
    )
    .rename("order_count")
    .rename_axis("year_month")
    .reset_index()
)
peak_month = monthly_orders.loc[monthly_orders["order_count"].idxmax()]
highest_category = revenue_by_category.iloc[0]
lowest_category = revenue_by_category.iloc[-1]

st.header("Ringkasan temuan")
metric1, metric2, metric3 = st.columns(3)
metric1.metric(
    "Revenue kategori tertinggi (2017)",
    f"R$ {highest_category['revenue']:,.2f}",
    delta=str(highest_category["product_category_name"]),
)
metric2.metric(
    "Revenue kategori terendah (2017)",
    f"R$ {lowest_category['revenue']:,.2f}",
    delta=str(lowest_category["product_category_name"]),
)
metric3.metric(
    "Puncak pesanan bulanan",
    f"{int(peak_month['order_count']):,} pesanan",
    delta=str(peak_month["year_month"]),
)

st.caption(
    "Revenue dihitung dari penjumlahan kolom price pada item pesanan, "
    "tanpa memasukkan biaya pengiriman."
)

st.header("Pertanyaan 1 — Kategori produk dengan revenue tertinggi dan terendah pada 2017")
st.markdown(
    "Grafik membandingkan lima kategori dengan pendapatan tertinggi dan lima "
    "kategori dengan pendapatan terendah sepanjang tahun 2017."
)

top_col, lowest_col = st.columns(2)
with top_col:
    st.subheader("Lima kategori tertinggi")
    st.bar_chart(
        top_categories,
        x="product_category_name",
        y="revenue",
        horizontal=True,
        sort=False,
        alt="Lima kategori produk dengan total revenue tertinggi sepanjang 2017.",
    )
with lowest_col:
    st.subheader("Lima kategori terendah")
    st.bar_chart(
        lowest_categories,
        x="product_category_name",
        y="revenue",
        horizontal=True,
        sort=False,
        alt="Lima kategori produk dengan total revenue terendah sepanjang 2017.",
    )

st.dataframe(
    revenue_by_category,
    hide_index=True,
    column_config={
        "product_category_name": "Kategori produk",
        "revenue": st.column_config.NumberColumn(
            "Revenue (R$)", format="R$ %.2f"
        ),
    },
    alt="Pendapatan setiap kategori produk selama tahun 2017, diurutkan dari tertinggi.",
)

st.header(
    "Pertanyaan 2 — Tren jumlah pesanan bulanan Januari 2017 hingga Agustus 2018"
)
st.line_chart(
    monthly_orders,
    x="year_month",
    y="order_count",
    x_label="Bulan",
    y_label="Jumlah pesanan",
    alt=(
        "Tren jumlah pesanan bulanan dari Januari 2017 hingga Agustus 2018. "
        f"Puncak terjadi pada {peak_month['year_month']} dengan "
        f"{int(peak_month['order_count']):,} pesanan."
    ),
)
st.info(
    f"Puncak jumlah pesanan terjadi pada **{peak_month['year_month']}** "
    f"dengan **{int(peak_month['order_count']):,} pesanan**."
)

st.subheader("Analisis tambahan — jumlah pelanggan per state")
if selected_states:
    state_counts = (
        customers_df.loc[customers_df["customer_state"].isin(selected_states)]
        ["customer_state"]
        .value_counts()
        .rename_axis("customer_state")
        .rename("customer_count")
        .reset_index()
        .sort_values("customer_count")
    )
    st.bar_chart(
        state_counts,
        x="customer_state",
        y="customer_count",
        horizontal=True,
        sort=False,
        alt="Jumlah pelanggan per negara bagian yang dipilih.",
    )
else:
    st.info("Pilih setidaknya satu state di sidebar untuk melihat analisis pelanggan.")

st.subheader("Rekomendasi dari analisis")
st.markdown(
    f"""
- Prioritaskan stok dan promosi kategori berpendapatan tinggi, khususnya
  **{highest_category['product_category_name']}**.
- Siapkan kampanye dan kapasitas operasional menjelang **{peak_month['year_month']}**,
  bulan dengan jumlah pesanan tertinggi pada periode analisis.
"""
)

st.divider()
st.caption("Proyek Analisis Data — Belajar Fundamental Analisis Data Dicoding")
