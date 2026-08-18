import pandas as pd


MISSING_VALUES = {
    "-- Unbranded --",
    "-- No Unilog Brand --",
    "-- No DIB Brand --",
    "-"
}


def normalize_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert dataset-specific placeholder values into proper missing values.
    """

    normalized = df.copy()

    for column in normalized.columns:
        normalized[column] = normalized[column].replace(MISSING_VALUES,pd.NA)

    return normalized