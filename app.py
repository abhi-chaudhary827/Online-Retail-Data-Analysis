# ====================================================
# ADVANCED INTERACTIVE RETAIL DASHBOARD
# ====================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ====================================================
# PAGE CONFIG
# ====================================================

st.set_page_config(
    page_title="Retail Dashboard",
    layout="wide"
)

# ====================================================
# TITLE
# ====================================================

st.title("🛒 AI-Powered Retail Analytics Dashboard")

# ====================================================
# FILE UPLOAD
# ====================================================

uploaded_file = st.file_uploader(
    "Upload Retail Dataset",
    type=['xlsx','csv']
)

if uploaded_file is not None:

    # ====================================================
    # LOAD DATA
    # ====================================================

    df = pd.read_excel(uploaded_file)

    # ====================================================
    # DATA CLEANING
    # ====================================================

    df.dropna(inplace=True)

    df['InvoiceDate'] = pd.to_datetime(
        df['InvoiceDate']
    )

    # ====================================================
    # FEATURE ENGINEERING
    # ====================================================

    df['TotalPrice'] = (
        df['Quantity'] * df['Price']
    )

    df['Month'] = (
        df['InvoiceDate'].dt.month
    )

    # ====================================================
    # SIDEBAR FILTERS
    # ====================================================

    st.sidebar.header("🔍 Filters")

    # Country Filter
    country = st.sidebar.selectbox(

        "Select Country",

        df['Country'].unique()

    )

    filtered_df = df[
        df['Country'] == country
    ]

    # ====================================================
    # KPI CARDS
    # ====================================================

    total_revenue = (
        filtered_df['TotalPrice'].sum()
    )

    total_orders = (
        filtered_df['Invoice'].nunique()
    )

    total_customers = (
        filtered_df['Customer ID'].nunique()
    )

    avg_order_value = (
        total_revenue / total_orders
    )

    # KPI Layout
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Revenue",
        f"{total_revenue:,.2f}"
    )

    col2.metric(
        "🧾 Orders",
        total_orders
    )

    col3.metric(
        "👥 Customers",
        total_customers
    )

    col4.metric(
        "📦 Avg Order Value",
        f"{avg_order_value:,.2f}"
    )

    # ====================================================
    # TOP PRODUCTS
    # ====================================================

    st.subheader("🔥 Top Selling Products")

    top_products = (

        filtered_df.groupby('Description')['Quantity']

        .sum()

        .sort_values(ascending=False)

        .head(10)

    )

    fig1, ax1 = plt.subplots(figsize=(10,5))

    top_products.plot(
        kind='bar',
        ax=ax1
    )

    plt.title("Top Products")

    st.pyplot(fig1)

    # ====================================================
    # MONTHLY SALES TREND
    # ====================================================

    st.subheader("📈 Monthly Revenue Trend")

    monthly_sales = (

        filtered_df.groupby('Month')['TotalPrice']

        .sum()

    )

    fig2, ax2 = plt.subplots(figsize=(10,5))

    monthly_sales.plot(
        marker='o',
        ax=ax2
    )

    plt.title("Monthly Sales")

    plt.xlabel("Month")

    plt.ylabel("Revenue")

    st.pyplot(fig2)

    # ====================================================
    # COUNTRY-WISE REVENUE
    # ====================================================

    st.subheader("🌍 Country Revenue Distribution")

    country_sales = (

        df.groupby('Country')['TotalPrice']

        .sum()

        .sort_values(ascending=False)

        .head(10)

    )

    fig3, ax3 = plt.subplots(figsize=(10,5))

    country_sales.plot(
        kind='bar',
        ax=ax3
    )

    plt.title("Top Countries")

    st.pyplot(fig3)

    # ====================================================
    # PIE CHART
    # ====================================================

    st.subheader("🥧 Revenue Share")

    fig4, ax4 = plt.subplots(figsize=(7,7))

    country_sales.head(5).plot(
        kind='pie',
        autopct='%1.1f%%',
        ax=ax4
    )

    plt.ylabel("")

    st.pyplot(fig4)

    # ====================================================
    # HEATMAP
    # ====================================================

    st.subheader("🔥 Correlation Heatmap")

    fig5, ax5 = plt.subplots(figsize=(8,5))

    sns.heatmap(

        filtered_df[
            ['Quantity','Price','TotalPrice']
        ].corr(),

        annot=True,

        cmap='coolwarm',

        ax=ax5

    )

    st.pyplot(fig5)

    # ====================================================
    # DATA PREVIEW
    # ====================================================

    st.subheader("📄 Dataset Preview")

    st.dataframe(filtered_df.head())

    # ====================================================
    # DOWNLOAD BUTTON
    # ====================================================

    csv = filtered_df.to_csv(index=False)

    st.download_button(

        label="⬇ Download Data",

        data=csv,

        file_name='filtered_data.csv',

        mime='text/csv'

    )

    # ====================================================
    # SUCCESS MESSAGE
    # ====================================================

    st.success(
        "Dashboard Loaded Successfully!"
    )