import pandas as pd


def profile_products(df: pd.DataFrame) -> None:
    print("\n========== DATASET PROFILE ==========")

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nUnique values:")
    for column in df.columns:
        print(f"{column}: {df[column].nunique()}")

    print("\nSample records:")
    print(df.head(5).to_string(index=False))