import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Configure Streamlit
st.set_page_config(layout="wide", page_title="Business Insights Dashboard")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a Page:", ["Dashboard", "RFM Analysis"])

# Load dataset
df = pd.read_csv("dashboard/datasets_cleaned.csv")

# Convert timestamps to datetime
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])
df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'])

# ===========================
# PAGE 1: BUSINESS DASHBOARD
# ===========================
if page == "Dashboard":
    st.markdown("<h1 style='text-align: center;'>Business Insights Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Brazilian E-Commerce Public Dataset</h4>", unsafe_allow_html=True)

    # Sidebar Filters
    st.sidebar.subheader("Filters")
    start_date = st.sidebar.date_input("Start Date", df['order_purchase_timestamp'].min())
    end_date = st.sidebar.date_input("End Date", df['order_purchase_timestamp'].max())
    
    df_filtered = df[(df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) & 
                     (df['order_purchase_timestamp'] <= pd.to_datetime(end_date))]
    
    product_categories = df_filtered['product_category_name_english'].dropna().unique()
    selected_category = st.sidebar.selectbox("Select Product Category", ["All"] + list(product_categories))
    if selected_category != "All":
        df_filtered = df_filtered[df_filtered['product_category_name_english'] == selected_category]
    
    states = df_filtered['customer_state'].dropna().unique()
    selected_state = st.sidebar.selectbox("Select State", ["All"] + list(states))
    if selected_state != "All":
        df_filtered = df_filtered[df_filtered['customer_state'] == selected_state]
    
    st.markdown("<hr>", unsafe_allow_html=True)

    # KPI Metrics
    total_orders = df_filtered["order_id"].nunique()
    total_revenue = df_filtered["payment_value"].sum()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    total_customers = df_filtered["customer_unique_id"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📦 Total Orders", value=f"{total_orders:,}")
    with col2:
        st.metric(label="💰 Total Revenue", value=f"${total_revenue:,.2f}")
    with col3:
        st.metric(label="📊 Avg Order Value", value=f"${avg_order_value:,.2f}")
    with col4:
        st.metric(label="👥 Total Customers", value=f"{total_customers:,}")
    
    st.markdown("<hr>", unsafe_allow_html=True)    

    # Top 5 Cities with Most Customers
    st.subheader("🏙️ Top 5 Cities with Most Customers")
    top_cities = (
        df_filtered.groupby("customer_city")["customer_unique_id"]
        .nunique()
        .sort_values(ascending=False)
        .head(5)
    )
    
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(x=top_cities.values, y=top_cities.index, palette="viridis", ax=ax)
    ax.set_title("Top 5 Cities with Most Customers")
    ax.set_xlabel("Number of Customers")
    ax.set_ylabel("City")
    st.pyplot(fig)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Payment Type Distribution
    st.subheader("💳 Payment Type Distribution")
    payment_counts = df_filtered['payment_type'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', colors=sns.color_palette("Set2"), startangle=120)
    ax.set_title("Payment Type Distribution")
    st.pyplot(fig)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Orders Trend
    st.subheader("📈 Trend of Orders per Month")
    orders_by_month = df_filtered['order_purchase_timestamp'].dt.to_period('M').value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(orders_by_month.index.astype(str), orders_by_month.values, marker='o', linestyle='-', color='teal')
    ax.set_title("Trend of Orders per Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Order Count")
    st.pyplot(fig)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Product Categories
    top_categories = df_filtered['product_category_name_english'].value_counts().head(5)
    st.subheader("🛍️ Top 5 Product Categories")
    fig4, ax4 = plt.subplots(figsize=(12, 5))
    bars = ax4.barh(top_categories.index, top_categories.values, color='royalblue')
    ax4.set_title("Top 5 Product Categories")
    ax4.set_xlabel("Number of Products Sold")
    ax4.set_ylabel("Product Category")
    ax4.invert_yaxis()
    for bar in bars:
        ax4.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, f'{bar.get_width():,}', va='center', fontsize=8)
    st.pyplot(fig4)

    st.markdown("<hr>", unsafe_allow_html=True)

# ===========================
# PAGE 2: RFM ANALYSIS
# ===========================
elif page == "RFM Analysis":
    st.markdown("<h1 style='text-align: center;'>RFM Analysis Dashboard</h1>", unsafe_allow_html=True)
    
    # Calculate RFM Metrics
    reference_date = df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (reference_date - x.max()).days,
        'order_id': 'count',
        'payment_value': 'sum'
    }).reset_index()

    rfm.columns = ['customer_unique_id', 'Recency', 'Frequency', 'Monetary']

    rfm['R_Score'] = pd.qcut(rfm['Recency'], q=4, labels=[4, 3, 2, 1])
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method="first"), q=4, labels=[1, 2, 3, 4])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method="first"), q=4, labels=[1, 2, 3, 4])
    rfm[['R_Score', 'F_Score', 'M_Score']] = rfm[['R_Score', 'F_Score', 'M_Score']].astype(int)
    rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].mean(axis=1)

    rfm['customer_segment'] = np.select([
        rfm['RFM_Score'] > 4,
        rfm['RFM_Score'] > 3,
        rfm['RFM_Score'] > 2,
        rfm['RFM_Score'] <= 2
    ], ["Top Customer", "High Value", "Medium Value", "Low Value"], default="Unknown")

    selected_segment = st.selectbox("Filter by Customer Segment:", ["All"] + list(rfm["customer_segment"].unique()))
    if selected_segment != "All":
        rfm = rfm[rfm["customer_segment"] == selected_segment]
    
    st.dataframe(rfm)
    st.write("RFM Analysis is used to segment customers based on Recency, Frequency, and Monetary metrics.")