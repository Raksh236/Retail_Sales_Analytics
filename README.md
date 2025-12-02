#  Retail Sales Analytics Dashboard

This project analyzes a retail sales dataset from Kaggle using **Pandas** and **NumPy**,
and exposes an interactive analytics dashboard built with **Streamlit**.

##  Dataset

The dataset contains 1,000 transactions with the following fields:

- `Transaction ID`
- `Date`
- `Customer ID`
- `Gender`
- `Age`
- `Product Category`
- `Quantity`
- `Price per Unit`
- `Total Amount`

After cleaning, these become:

- `transaction_id`, `date`, `customer_id`, `gender`, `age`,
  `product_category`, `quantity`, `price_per_unit`, `total_amount`

##  Project Structure

```text
Retail_Sales_Analytics/
├── data/
│   ├── raw/
│   │   └── retail_sales_dataset.csv
│   └── processed/
│       └── sales_clean.csv
├── notebooks/
│   └── 01_exploratory_analysis.ipynb
├── src/
│   ├── clean_data.py
│   ├── analyze_kpis.py
│   └── dashboard_app.py
├── reports/
│   └── insights.md
├── requirements.txt
└── README.md
