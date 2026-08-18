import re
import pandas as pd


def extract_baseline_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract high-confidence structured attributes from Part_Desc.

    This is the deterministic baseline layer of the enrichment pipeline.
    It intentionally avoids guessing. Values that cannot be extracted
    confidently remain NaN and are handled by later enrichment stages.
    """

    result = df.copy()

    descriptions = result["Part_Desc"].astype("string")

    # ------------------------------------------------------------------
    # Quantity
    # ------------------------------------------------------------------
    # Match quantities such as:
    #   6pc
    #   50 pcs
    #   10 pieces
    #   2 boxes
    #   5 pack
    #   12 pk
    #   20 ct
    #
    # IMPORTANT:
    # Do not interpret "5" in '5" sanding disc' as quantity.
    # A quote immediately after the number indicates a dimension.
    quantity_pattern = (
        r'(?<![\d.])'
        r'(\d+)'
        r'(?!["\'])'
        r'\s*'
        r'(?:pc|pcs|piece|pieces|disc|discs|box|boxes|'
        r'pack|packs|pk|ct|count)'
        r'\b'
    )

    result["extracted_quantity"] = pd.to_numeric(
        descriptions.str.extract(
            quantity_pattern,
            flags=re.I,
            expand=False,
        ),
        errors="coerce",
    )

    # ------------------------------------------------------------------
    # Grit
    # ------------------------------------------------------------------
    # High-confidence FEPA notation:
    #   P80
    #   P120
    #   P150
    #   P320
    #
    # Also support contextual forms:
    #   grit 120
    #   grit #120
    #   #120
    #   120 grit
    #
    # We prefer the explicit P-number form because it is less ambiguous.

    fepa_grit = descriptions.str.extract(
        r"\b(P\d{2,4})\b",
        flags=re.I,
        expand=False,
    )

    grit_before_number = descriptions.str.extract(
        r"(?:\bgrit\s*#?|#)\s*(\d{2,4})\b",
        flags=re.I,
        expand=False,
    )

    grit_after_number = descriptions.str.extract(
        r"\b(\d{2,4})\s*grit\b",
        flags=re.I,
        expand=False,
    )

    contextual_grit = grit_before_number.combine_first(
        grit_after_number
    )

    result["extracted_grit"] = (
        fepa_grit
        .combine_first(contextual_grit)
        .str.upper()
    )

    # ------------------------------------------------------------------
    # Two-dimensional size
    # ------------------------------------------------------------------
    # Supports:
    #   1/2"x18"
    #   2.75x30
    #   4-1/2 x 7/8
    #   4 1/2 x 7/8
    #   5x10
    #
    # We intentionally do NOT extract single dimensions such as:
    #   125mm
    #   5"
    #
    # Those require semantic interpretation because they could represent
    # diameter, length, width, height, arbor size, etc.

    dimension = (
        r'\d+'
        r'(?:'
        r'\.\d+'
        r'|/\d+'
        r'|[-\s]\d+/\d+'
        r')?'
        r'["\']?'
    )

    size_pattern = (
        rf'(?<![\d.])'
        rf'({dimension}\s*x\s*{dimension})'
        rf'(?![\d.])'
    )

    result["extracted_size"] = descriptions.str.extract(
        size_pattern,
        flags=re.I,
        expand=False,
    )

    return result