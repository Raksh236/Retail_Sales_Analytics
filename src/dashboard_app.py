import sys
import os

# Add project root to Python path (one level above /src)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from analyze_kpis import (
    load_data,
    compute_kpis,
    monthly_revenue,
    category_performance,
    gender_performance,
)

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")


@st.cache_data
def get_data():
    return load_data()


def main():
    df = get_data()

    st.title("🛍️ Retail Sales Analytics Dashboard")

    # Sidebar filters
    st.sidebar.header("Filters")

    # Date range filter
    min_date = df["date"].min()
    max_date = df["date"].max()
    date_range = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[
            (df["date"] >= pd.to_datetime(start_date))
            & (df["date"] <= pd.to_datetime(end_date))
        ]
    else:
        df_filtered = df

    # Category filter
    categories = sorted(df["product_category"].unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Product Category",
        options=categories,
        default=categories,
    )

    if selected_categories:
        df_filtered = df_filtered[df_filtered["product_category"].isin(selected_categories)]

    # KPIs
    kpis = compute_kpis(df_filtered)
    st.subheader("Key Metrics")

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric("Total Revenue", f"${kpis['total_revenue']:,.0f}")
    col2.metric("Total Transactions", f"{kpis['total_transactions']:,}")
    col3.metric("Unique Customers", f"{kpis['unique_customers']:,}")

    col4.metric("Avg Order Value", f"${kpis['avg_order_value']:.2f}")
    col5.metric("Avg Items / Transaction", f"{kpis['avg_items_per_transaction']:.2f}")
    col6.metric("Avg Customer Age", f"{kpis['avg_customer_age']:.1f}")

    # Monthly revenue chart
    st.subheader("📆 Monthly Revenue Trend")
    monthly = monthly_revenue(df_filtered)

    fig1, ax1 = plt.subplots()
    ax1.plot(monthly["date"], monthly["monthly_revenue"], marker="o")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Revenue")
    ax1.set_title("Monthly Revenue")
    st.pyplot(fig1)

    # Category performance table + bar chart
    st.subheader("🏷️ Product Category Performance")
    cat_perf = category_performance(df_filtered)
    st.dataframe(cat_perf)

    fig2, ax2 = plt.subplots()
    ax2.bar(cat_perf["product_category"], cat_perf["total_revenue"])
    ax2.set_xlabel("Product Category")
    ax2.set_ylabel("Total Revenue")
    ax2.set_title("Revenue by Product Category")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # Gender performance
    st.subheader("🧍 Gender-Based Revenue")
    gender_perf = gender_performance(df_filtered)
    st.dataframe(gender_perf)

    fig3, ax3 = plt.subplots()
    ax3.bar(gender_perf["gender"], gender_perf["total_revenue"])
    ax3.set_xlabel("Gender")
    ax3.set_ylabel("Total Revenue")
    ax3.set_title("Revenue by Gender")
    st.pyplot(fig3)


if __name__ == "__main__":
    main()
