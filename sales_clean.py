import pandas as pd
from pathlib import Path


def clean_sales_data(
    input_path="retail_sales_dataset.csv",
    output_path="data/sales_clean.csv"
):
    # Load raw dataset
    df = pd.read_csv(input_path)

    # Convert date to datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop rows with invalid or missing dates
    df = df.dropna(subset=["Date"])

    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Revenue validation
    df["computed_total"] = df["quantity"] * df["price_per_unit"]

    # Keep rows where Total Amount is correct
    df = df[abs(df["computed_total"] - df["total_amount"]) < 1e-6]

    # Drop helper column
    df = df.drop(columns=["computed_total"])

    # Ensure output folder exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Save cleaned file
    df.to_csv(output_path, index=False)
    print("Saved cleaned dataset to:", output_path)

    return df


if __name__ == "__main__":
    clean_sales_data()
