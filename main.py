from src.ingestion.load import load_products
from src.profiler import profile_products
from src.normalization.normalize import normalize_missing_values
from src.normalization.extract_baseline import extract_baseline_features

def main():
    products = load_products()

    products=normalize_missing_values(products)
    products=extract_baseline_features(products)

    print("\n========== BASELINE EXTRACTION ==========")

    print(
        products[
            [
                "Mfg_Part_Num",
                "Part_Desc",
                "extracted_quantity",
                "extracted_grit",
                "extracted_size"
            ]
        ].head(10).to_string(index=False)
    )
    profile_products(products)



if __name__ == "__main__":
    main()