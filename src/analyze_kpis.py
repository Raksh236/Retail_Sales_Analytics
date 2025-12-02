import pandas as pd


def load_data(path: str = "data/processed/sales_clean.csv") -> pd.DataFrame:
    """Load cleaned sales data."""
    df = pd.read_csv(path, parse_dates=["date"])
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute core KPIs from the sales dataframe."""
    total_revenue = df["total_amount"].sum()
    total_transactions = df["transaction_id"].nunique()
    unique_customers = df["customer_id"].nunique()

    avg_order_value = df["total_amount"].mean()
    avg_items_per_transaction = df["quantity"].mean()
    avg_customer_age = df["age"].mean()

    return {
        "total_revenue": total_revenue,
        "total_transactions": total_transactions,
        "unique_customers": unique_customers,
        "avg_order_value": avg_order_value,
        "avg_items_per_transaction": avg_items_per_transaction,
        "avg_customer_age": avg_customer_age,
    }


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue by month."""
    monthly = (
        df.set_index("date")
        .resample("M")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"total_amount": "monthly_revenue"})
    )
    return monthly


def category_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue and volume by product category."""
    cat_perf = (
        df.groupby("product_category")
        .agg(
            total_revenue=("total_amount", "sum"),
            avg_price=("price_per_unit", "mean"),
            units_sold=("quantity", "sum"),
            num_transactions=("transaction_id", "nunique"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    return cat_perf


def gender_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue and average age by gender."""
    gender_perf = (
        df.groupby("gender")
        .agg(
            total_revenue=("total_amount", "sum"),
            avg_age=("age", "mean"),
            num_customers=("customer_id", "nunique"),
        )
        .reset_index()
    )
    return gender_perf


if __name__ == "__main__":
    # Quick manual test
    df = load_data()
    print("KPIs:")
    for k, v in compute_kpis(df).items():
        print(f"{k}: {v}")
