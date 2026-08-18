from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "input.csv"


def load_products() -> pd.DataFrame:
    """
    Load the raw UniHack product dataset.

    Returns:
        pd.DataFrame: Raw product catalog.
    """

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        raise ValueError("Input dataset is empty.")

    return df