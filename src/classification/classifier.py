import pandas as pd


DOMAIN_RULES = {
    "decking": [
        "DECKING",
        "TREX",
        "AZEK",
        "TRANSCEND",
        "LINEAGE",
        "ENHANCE",
        "SELECT",
    ],
    "lighting": [
        "LED",
        "KICHLER",
        "PENDANT",
        "CHANDELIER",
        "CEILING LIGHT",
        "WALL LIGHT",
    ],
    "power_tools": [
        "DEWALT",
        "MILW",
        "MAKITA",
        "KREG",
        "20V",
        "18V",
        "M12",
        "M18",
        "SAW",
        "DRILL",
    ],
}


def classify_product_domain(description: str) -> str:
    """
    Assign a coarse product domain using catalog signals.

    Returns 'unknown' when no known domain signal is found.
    """

    text = str(description).upper()

    scores = {}

    for domain, signals in DOMAIN_RULES.items():
        score = sum(signal in text for signal in signals)
        scores[domain] = score

    best_domain = max(scores, key=scores.get)

    if scores[best_domain] == 0:
        return "unknown"

    return best_domain


def classify_products(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result["product_domain"] = result["Part_Desc"].apply(
        classify_product_domain
    )

    return result