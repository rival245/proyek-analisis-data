from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="Dashboard Analisis E-Commerce", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #f5f7ff 0%, #eef4ff 100%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        div[data-testid="stSidebar"] {
            background: #0f172a;
            color: white;
        }
        h1, h2, h3 {
            color: #0f172a;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    customers_df = pd.read_csv(BASE_DIR / "customers_dataset.csv")
    orders_df = pd.read_csv(BASE_DIR / "orders_dataset.csv")
    order_items_df = pd.read_csv(BASE_DIR / "order_items_dataset.csv")
    products_df = pd.read_csv(BASE_DIR / "products_dataset.csv")
    order_reviews_df = pd.read_csv(BASE_DIR / "order_reviews_dataset.csv")
    return customers_df, orders_df, order_items_df, products_df, order_reviews_df


customers_df, orders_df, order_items_df, products_df, order_reviews_df = load_data()

orders_df["order_purchase_timestamp"] = pd.to_datetime(orders_df["order_purchase_timestamp"], errors="coerce")
orders_df["order_estimated_delivery_date"] = pd.to_datetime(orders_df["order_estimated_delivery_date"], errors="coerce")
orders_df["order_delivered_customer_date"] = pd.to_datetime(orders_df["order_delivered_customer_date"], errors="coerce")

st.title("📊 Dashboard Analisis E-Commerce Olist")
st.markdown("Selamat datang di dashboard interaktif untuk melihat performa penjualan, logistik, dan kepuasan pelanggan.")

with st.sidebar:
    st.header("Filter Dashboard")
    years = sorted(orders_df["order_purchase_timestamp"].dropna().dt.year.unique().tolist())
    selected_year = st.selectbox("Pilih tahun", options=years)
    states = ["Semua"] + sorted(customers_df["customer_state"].dropna().unique().tolist())
    selected_state = st.selectbox("Pilih state pelanggan", options=states)
    top_n = st.slider("Jumlah kategori yang ditampilkan", min_value=3, max_value=10, value=5)

filtered_orders = orders_df[orders_df["order_purchase_timestamp"].dt.year == selected_year].copy()
if selected_state != "Semua":
    customer_ids = customers_df.loc[customers_df["customer_state"] == selected_state, "customer_id"]
    filtered_orders = filtered_orders[filtered_orders["customer_id"].isin(customer_ids)]

orders_items_df = pd.merge(filtered_orders, order_items_df, on="order_id", how="inner")
complete_order_df = pd.merge(orders_items_df, products_df, on="product_id", how="inner")

revenue_by_category = (
    complete_order_df.groupby("product_category_name", as_index=False)["price"].sum().rename(columns={"price": "revenue"})
)
revenue_by_category = revenue_by_category.sort_values("revenue", ascending=False).head(top_n)

orders_reviews_df = pd.merge(filtered_orders, order_reviews_df, on="order_id", how="inner")
orders_reviews_df["delivery_latency"] = (
    orders_reviews_df["order_delivered_customer_date"] - orders_reviews_df["order_estimated_delivery_date"]
).dt.days
orders_reviews_df = orders_reviews_df.dropna(subset=["delivery_latency", "review_score"])
latency_vs_review = orders_reviews_df.groupby("review_score")["delivery_latency"].mean().reset_index()

filtered_customers = customers_df
if selected_state != "Semua":
    filtered_customers = filtered_customers[filtered_customers["customer_state"] == selected_state]

state_counts = filtered_customers["customer_state"].value_counts().head(top_n).reset_index()
state_counts.columns = ["customer_state", "customer_count"]

monthly_orders = filtered_orders.set_index("order_purchase_timestamp").resample("ME").size().reset_index()
monthly_orders.columns = ["month", "order_count"]

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"R$ {complete_order_df['price'].sum():,.0f}")
col2.metric("Jumlah Pesanan", f"{len(filtered_orders):,}")
col3.metric("Rata-rata Review", f"{orders_reviews_df['review_score'].mean():.2f} / 5")

st.markdown("---")

st.subheader(f"🏆 Top {top_n} Kategori Produk dengan Revenue Terbesar ({selected_year})")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="revenue",
    y="product_category_name",
    data=revenue_by_category,
    palette="Blues_r",
    legend=False,
    ax=ax,
)
ax.set_title(f"Top {top_n} Kategori Produk Berdasarkan Revenue", fontsize=12, fontweight="bold")
ax.set_xlabel("Total Pendapatan (Revenue)")
ax.set_ylabel("Kategori Produk")
for label in ax.get_yticklabels():
    label.set_fontsize(9)
st.pyplot(fig)

st.markdown("""
* **Insight:** Kategori dengan revenue tertinggi biasanya menjadi fokus utama strategi promosi dan stok produk.
""")

st.markdown("---")

st.subheader(f"📦 Pengaruh Keterlambatan Pengiriman terhadap Skor Ulasan Pelanggan ({selected_year})")
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(
    x="review_score",
    y="delivery_latency",
    data=latency_vs_review,
    palette="Reds_r",
    legend=False,
    ax=ax2,
)
ax2.set_title("Rata-rata Keterlambatan (Hari) Berdasarkan Skor Ulasan", fontsize=12, fontweight="bold")
ax2.set_xlabel("Skor Ulasan (Review Score)")
ax2.set_ylabel("Rata-rata Selisih Hari dari Estimasi")
ax2.axhline(0, color="black", linewidth=1.0, alpha=0.7)
st.pyplot(fig2)

st.markdown("""
* **Insight:** Nilai negatif menunjukkan pengiriman lebih cepat dari estimasi, sedangkan nilai positif menunjukkan keterlambatan.
""")

st.markdown("---")

st.subheader(f"📈 Tren Pesanan Bulanan ({selected_year})")
fig4, ax4 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=monthly_orders, x="month", y="order_count", marker="o", ax=ax4, color="#2563eb")
ax4.set_title("Jumlah Pesanan per Bulan", fontsize=12, fontweight="bold")
ax4.set_xlabel("Bulan")
ax4.set_ylabel("Jumlah Pesanan")
plt.xticks(rotation=45)
st.pyplot(fig4)

st.markdown("---")

st.subheader(f"📍 Top {top_n} Negara Bagian Asal Pelanggan Terbanyak")
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.barplot(
    x="customer_count",
    y="customer_state",
    data=state_counts,
    palette="Purples_r",
    legend=False,
    ax=ax3,
)
ax3.set_title("Top Negara Bagian Pelanggan Terbanyak", fontsize=12, fontweight="bold")
ax3.set_xlabel("Jumlah Pelanggan")
ax3.set_ylabel("Kode Negara Bagian")
st.pyplot(fig3)

st.markdown("---")
st.caption("Proyek Analisis Data - Belajar Fundamental Analisis Data Dicoding")
