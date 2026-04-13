import streamlit as st
import pandas as pd

# Page config

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Load data

df = pd.read_csv("superstore.csv")

# Clean column names (important)

df.columns = df.columns.str.strip()

# Convert date

df['Order Date'] = pd.to_datetime(df['Order Date'],dayfirst=True)

# Title

st.title("📊 Sales Dashboard")

# Sidebar filters

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
"Select Region",
options=df['Region'].unique()
)

category = st.sidebar.multiselect(
"Select Category",
options=df['Category'].unique()
)

# Filtering logic

filtered_df = df.copy()

if region:
    filtered_df = filtered_df[filtered_df['Region'].isin(region)]

if category:
    filtered_df = filtered_df[filtered_df['Category'].isin(category)]

# =========================

# KPI SECTION

# =========================

st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Orders", filtered_df.shape[0])
col3.metric("Average Sales", f"${filtered_df['Sales'].mean():,.0f}")

# =========================

# CHARTS SECTION

# =========================

st.subheader("📊 Sales Analysis")

col1, col2 = st.columns(2)

# Sales by Region

with col1:
    st.subheader("Sales by Region")
    region_sales = filtered_df.groupby('Region')['Sales'].sum()
    st.bar_chart(region_sales)

# Sales by Category

with col2:
    st.subheader("Sales by Category")
    category_sales = filtered_df.groupby('Category')['Sales'].sum()
    st.bar_chart(category_sales)

# =========================

# MONTHLY TREND

# =========================

st.subheader("📈 Monthly Sales Trend")

monthly_sales = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M'))['Sales'].sum()
monthly_sales.index = monthly_sales.index.astype(str)

st.line_chart(monthly_sales)

# =========================

# TOP PRODUCTS

# =========================

st.subheader("🏆 Top 5 Sub-Categories")

top_products = (
filtered_df.groupby('Sub-Category')['Sales']
.sum()
.sort_values(ascending=False)
.head()
)

st.bar_chart(top_products)

st.markdown("---")   # (optional but clean)

st.subheader("📌 Key Insights")

st.write("""
- West region generates highest sales  
- Technology category drives revenue  
- Sales show strong growth over time  
""")
# =========================
st.markdown("---")
st.caption("Built using Streamlit | Sales Data Analysis Project")
# =========================
