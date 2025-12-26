import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

# -------------------- TITLE --------------------
st.title("Sales Performance Dashboard")

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")  # make sure file is in same folder
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# -------------------- KPIs --------------------
st.header("Key Metrics")

col1, col2, col3 = st.columns(3)

total_revenue = df["Total"].sum()
total_sales = df.shape[0]
avg_sale = df["Total"].mean()

with col1:
    st.metric("Total Revenue", f"${total_revenue:,.0f}")

with col2:
    st.metric("Total Sales", f"{total_sales:,}")

with col3:
    st.metric("Average Sale", f"${avg_sale:,.0f}")

st.divider()

# -------------------- REVENUE BY PRODUCT --------------------
st.header("Revenue by Product")

product_revenue = (
    df.groupby("Product", as_index=False)["Total"]
    .sum()
    .sort_values("Total", ascending=True)
)

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=product_revenue,
    x="Total",
    y="Product",
    hue="Product",
    palette="viridis",
    legend=False,
    ax=ax1
)

ax1.set_xlabel("Revenue ($)")
ax1.set_ylabel("Product")
ax1.set_title("Revenue by Product")

st.pyplot(fig1)

st.write("As we can see Laptop is the highest revenue generating product.")
st.divider()

# -------------------- MONTHLY SALES TREND --------------------
st.header("Monthly Sales Trend")

df["Month"] = df["Date"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("Month")["Total"].sum()

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(monthly_sales.index, monthly_sales.values, marker="o")

ax2.set_xlabel("Month")
ax2.set_ylabel("Revenue ($)")
ax2.set_title("Monthly Revenue Trend")
ax2.grid(alpha=0.3)
ax2.tick_params(axis="x", rotation=45)

st.pyplot(fig2)

st.divider()

# -------------------- SALES BY REGION --------------------
st.header("Sales by Region")

region_sales = df.groupby("Region")["Total"].sum()

fig3, ax3 = plt.subplots(figsize=(8, 8))
ax3.pie(
    region_sales.values,
    labels=region_sales.index,
    autopct="%1.1f%%",
    startangle=90
)
ax3.set_title("Revenue Distribution by Region")

st.pyplot(fig3)

st.divider()

# -------------------- RAW DATA --------------------
st.header("Raw Data")
st.dataframe(df, use_container_width=True)
