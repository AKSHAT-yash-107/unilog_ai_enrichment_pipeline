import re
from collections import Counter

import pandas as pd


def analyze_description_vocabulary(
    df: pd.DataFrame,
    top_n: int = 50,
) -> None:
    """
    Analyze recurring tokens in Part_Desc.

    This is exploratory analysis only.
    It does not modify the product data.
    """

    descriptions = (
        df["Part_Desc"]
        .astype("string")
        .str.upper()
        .fillna("")
    )

    tokens = []

    for description in descriptions:
        words = re.findall(r"[A-Z0-9][A-Z0-9./#'-]*", description)
        tokens.extend(words)

    counts = Counter(tokens)

    print("\n========== TOP DESCRIPTION TOKENS ==========")

    for token, count in counts.most_common(top_n):
        print(f"{token:<25} {count}")



def analyze_description_phrases(
    df: pd.DataFrame,
    top_n: int = 50,
) -> None:
    """
    Find frequently occurring two-word phrases in product descriptions.
    """

    descriptions = (
        df["Part_Desc"]
        .astype("string")
        .str.upper()
        .fillna("")
    )

    phrase_counts = Counter()

    for description in descriptions:
        words = re.findall(
            r"[A-Z0-9][A-Z0-9./#'-]*",
            description,
        )

        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i + 1]}"
            phrase_counts[phrase] += 1

    print("\n========== TOP DESCRIPTION PHRASES ==========")

    for phrase, count in phrase_counts.most_common(top_n):
        print(f"{phrase:<35} {count}")