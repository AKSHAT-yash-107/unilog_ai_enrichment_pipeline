from src.ingestion.load import load_products
from src.normalization.normalize import normalize_missing_values
from src.normalization.extract_baseline import extract_baseline_features
from src.normalization.vocabulary import analyze_description_vocabulary
from src.normalization.vocabulary import analyze_description_phrases
from src.profiler import profile_products


def main():
    products = load_products()

    products = normalize_missing_values(products)

    products = extract_baseline_features(products)

    print("\n========== BASELINE EXTRACTION ==========")

    print(
        products[
            [
                "Mfg_Part_Num",
                "Part_Desc",
                "extracted_quantity",
                "extracted_grit",
                "extracted_size",
            ]
        ].head(20).to_string(index=False)
    )

    profile_products(products)

    analyze_description_vocabulary(products)
    analyze_description_phrases(products)


if __name__ == "__main__":
    main()