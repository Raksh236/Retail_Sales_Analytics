import pandas as pd
from pathlib import Path


def clean_sales_data(
    input_path: str = "data/raw/retail_sales_dataset.csv",
    output_path: str = "data/processed/sales_clean.csv",
):
    # Load raw dataset
    df = pd.read_csv(input_path)

    # Convert Date to datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop rows with invalid or missing dates
    df = df.dropna(subset=["Date"])

    # Standardize column names: lowercase + underscores
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Validate revenue: quantity * price_per_unit should equal total_amount
    df["computed_total"] = df["quantity"] * df["price_per_unit"]
    diff = df["total_amount"] - df["computed_total"]

    # Keep rows where the difference is tiny (handles float issues)
    df = df[diff.abs() < 1e-6].copy()

    # Drop helper column
    df = df.drop(columns=["computed_total"])

    # Ensure output folder exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Save cleaned data
    df.to_csv(output_path, index=False)
    print(f"✅ Saved cleaned dataset to: {output_path}")
    return df


if __name__ == "__main__":
    clean_sales_data()
