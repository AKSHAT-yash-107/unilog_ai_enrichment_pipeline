from src.ingestion.load import load_products
from src.normalization.normalize import normalize_missing_values
from src.normalization.extract_baseline import extract_baseline_features
from src.normalization.vocabulary import analyze_description_vocabulary
from src.normalization.vocabulary import analyze_description_phrases
from src.profiler import profile_products
from src.classification.classifier import classify_products


def main():
    products = load_products()

    products = normalize_missing_values(products)

    products = extract_baseline_features(products)

    products = classify_products(products)

    print("\n========== DOMAIN DISTRIBUTION ==========")

    print(
        products["product_domain"]
        .value_counts(dropna=False)
    )

    print("\n========== UNKNOWN PRODUCTS ==========")

    unknown = products[
        products["product_domain"] == "unknown"
        ]

    print(
        unknown[
            ["Mfg_Part_Num", "Part_Desc"]
        ].head(50).to_string(index=False)
    )
if __name__ == "__main__":
    main()