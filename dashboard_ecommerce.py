from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_MIN = pd.Timestamp("2017-01-01")
DATA_MAX = pd.Timestamp("2018-08-31")

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

    # Satukan state pelanggan ke tabel pesanan agar filter state
    # berlaku untuk semua analisis, bukan hanya analisis pelanggan.
    orders_df = orders_df.merge(
        customers_df[["customer_id", "customer_state"]],
        on="customer_id",
        how="left",
    )
    return orders_df, order_items_df, products_df


def filter_orders(orders_df, start_date, end_date, states):
    """Filter pesanan berdasarkan rentang tanggal (inklusif) dan state pelanggan."""
    end_exclusive = pd.Timestamp(end_date) + pd.Timedelta(days=1)
    mask = (
        orders_df["order_purchase_timestamp"].ge(pd.Timestamp(start_date))
        & orders_df["order_purchase_timestamp"].lt(end_exclusive)
        & orders_df["customer_state"].isin(states)
    )
    return orders_df.loc[mask]


def get_revenue_by_category(filtered_orders, order_items_df, products_df):
    """Total revenue (kolom price, tanpa ongkir) per kategori produk."""
    merged = filtered_orders[["order_id"]].merge(
        order_items_df, on="order_id", how="inner"
    ).merge(products_df, on="product_id", how="inner")
    return (
        merged.groupby("product_category_name")["price"]
        .sum()
        .sort_values(ascending=False)
        .rename("revenue")
        .rename_axis("product_category_name")
        .reset_index()
    )


def get_monthly_orders(filtered_orders, start_date, end_date):
    """Jumlah pesanan per bulan; bulan tanpa pesanan ditampilkan sebagai 0."""
    months = pd.period_range(
        pd.Timestamp(start_date).to_period("M"),
        pd.Timestamp(end_date).to_period("M"),
        freq="M",
    ).astype(str)
    counts = (
        filtered_orders.assign(
            year_month=filtered_orders["order_purchase_timestamp"]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("year_month")["order_id"]
        .count()
    )
    return (
        counts.reindex(months, fill_value=0)
        .rename("order_count")
        .rename_axis("year_month")
        .reset_index()
    )


orders_df, order_items_df, products_df = load_data()

# ---------------------------------------------------------------- Sidebar
with st.sidebar:
    st.header("Filter dashboard")
    st.caption(
        "Seluruh filter di bawah memengaruhi ringkasan metrik, grafik kategori "
        "produk, tren pesanan, dan distribusi pelanggan."
    )

    date_range = st.date_input(
        "Rentang tanggal pembelian",
        value=(DATA_MIN.date(), DATA_MAX.date()),
        min_value=DATA_MIN.date(),
        max_value=DATA_MAX.date(),
        help="Data tersedia dari Januari 2017 hingga Agustus 2018.",
    )

    available_states = sorted(orders_df["customer_state"].dropna().unique())
    selected_states = st.multiselect(
        "State pelanggan",
        options=available_states,
        default=available_states,
    )

    top_n = st.slider(
        "Jumlah kategori yang ditampilkan",
        min_value=3,
        max_value=10,
        value=5,
        help="Berlaku untuk grafik kategori tertinggi dan terendah.",
    )

# Validasi input filter
if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
    st.title("Analisis Data E-Commerce Olist")
    st.info("Pilih tanggal awal **dan** tanggal akhir pada sidebar untuk menampilkan analisis.")
    st.stop()
start_date, end_date = date_range

if not selected_states:
    st.title("Analisis Data E-Commerce Olist")
    st.info("Pilih setidaknya satu state pelanggan pada sidebar untuk menampilkan analisis.")
    st.stop()

filtered_orders = filter_orders(orders_df, start_date, end_date, selected_states)
period_label = f"{start_date:%d %b %Y} – {end_date:%d %b %Y}"

st.title("Analisis Data E-Commerce Olist")
st.markdown(
    "Dashboard ini menyajikan hasil analisis proyek: pendapatan kategori produk, "
    "tren pesanan bulanan, dan distribusi pelanggan. Semua visualisasi mengikuti "
    "filter pada sidebar."
)
st.caption(
    f"Periode: **{period_label}** · State dipilih: **{len(selected_states)}** "
    f"dari {len(available_states)} · Pesanan terfilter: **{len(filtered_orders):,}**"
)

if filtered_orders.empty:
    st.warning("Tidak ada pesanan pada kombinasi filter ini. Ubah rentang tanggal atau state.")
    st.stop()

revenue_by_category = get_revenue_by_category(
    filtered_orders, order_items_df, products_df
)
monthly_orders = get_monthly_orders(filtered_orders, start_date, end_date)

if revenue_by_category.empty:
    st.warning("Tidak ada data item pesanan pada kombinasi filter ini.")
    st.stop()

top_categories = revenue_by_category.head(top_n).sort_values("revenue")
lowest_categories = revenue_by_category.tail(top_n).sort_values("revenue")
highest_category = revenue_by_category.iloc[0]
lowest_category = revenue_by_category.iloc[-1]
peak_month = monthly_orders.loc[monthly_orders["order_count"].idxmax()]
total_revenue = revenue_by_category["revenue"].sum()

# ---------------------------------------------------------------- Ringkasan
st.header("Ringkasan temuan")
metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric(
    "Revenue kategori tertinggi",
    f"R$ {highest_category['revenue']:,.2f}",
    delta=str(highest_category["product_category_name"]),
    delta_color="off",
)
metric2.metric(
    "Revenue kategori terendah",
    f"R$ {lowest_category['revenue']:,.2f}",
    delta=str(lowest_category["product_category_name"]),
    delta_color="off",
)
metric3.metric(
    "Puncak pesanan bulanan",
    f"{int(peak_month['order_count']):,} pesanan",
    delta=str(peak_month["year_month"]),
    delta_color="off",
)
metric4.metric("Total revenue periode terpilih", f"R$ {total_revenue:,.2f}")

st.caption(
    "Revenue dihitung dari penjumlahan kolom price pada item pesanan, "
    "tanpa memasukkan biaya pengiriman."
)

# ---------------------------------------------------------------- Pertanyaan 1
st.header("Pertanyaan 1 — Kategori produk dengan revenue tertinggi dan terendah")
st.markdown(
    f"Perbandingan {top_n} kategori dengan pendapatan tertinggi dan {top_n} kategori "
    f"dengan pendapatan terendah pada periode **{period_label}**."
)

top_col, lowest_col = st.columns(2)
with top_col:
    st.subheader(f"{top_n} kategori tertinggi")
    st.bar_chart(
        top_categories,
        x="product_category_name",
        y="revenue",
        x_label="Revenue (R$)",
        y_label="Kategori produk",
        horizontal=True,
        sort=False,
        alt=f"{top_n} kategori produk dengan total revenue tertinggi pada periode terpilih.",
    )
with lowest_col:
    st.subheader(f"{top_n} kategori terendah")
    st.bar_chart(
        lowest_categories,
        x="product_category_name",
        y="revenue",
        x_label="Revenue (R$)",
        y_label="Kategori produk",
        horizontal=True,
        sort=False,
        alt=f"{top_n} kategori produk dengan total revenue terendah pada periode terpilih.",
    )

with st.expander("Lihat tabel revenue seluruh kategori"):
    st.dataframe(
        revenue_by_category,
        hide_index=True,
        column_config={
            "product_category_name": "Kategori produk",
            "revenue": st.column_config.NumberColumn("Revenue (R$)", format="R$ %.2f"),
        },
    )

# ---------------------------------------------------------------- Pertanyaan 2
st.header("Pertanyaan 2 — Tren jumlah pesanan bulanan")
st.line_chart(
    monthly_orders,
    x="year_month",
    y="order_count",
    x_label="Bulan",
    y_label="Jumlah pesanan",
    alt=(
        f"Tren jumlah pesanan bulanan pada periode {period_label}. "
        f"Puncak terjadi pada {peak_month['year_month']} dengan "
        f"{int(peak_month['order_count']):,} pesanan."
    ),
)
st.info(
    f"Puncak jumlah pesanan terjadi pada **{peak_month['year_month']}** "
    f"dengan **{int(peak_month['order_count']):,} pesanan**."
)

# ---------------------------------------------------------------- Analisis lanjutan
st.subheader("Analisis tambahan — jumlah pelanggan per state")
state_counts = (
    filtered_orders["customer_state"]
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
    x_label="Jumlah pelanggan",
    y_label="State",
    horizontal=True,
    sort=False,
    alt="Jumlah pelanggan per negara bagian pada periode dan state yang dipilih.",
)

# ---------------------------------------------------------------- Rekomendasi
st.subheader("Rekomendasi dari analisis")
st.markdown(
    f"""
- Prioritaskan stok dan promosi kategori berpendapatan tinggi, khususnya
  **{highest_category['product_category_name']}**.
- Siapkan kampanye dan kapasitas operasional menjelang **{peak_month['year_month']}**,
  bulan dengan jumlah pesanan tertinggi pada periode terpilih.
"""
)

st.divider()
st.caption("Proyek Analisis Data — Belajar Fundamental Analisis Data Dicoding")
