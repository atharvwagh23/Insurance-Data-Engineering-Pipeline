import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ingestion_manager import validate_file
from preprocessing_engine import preprocess_file
from transformation_engine import build_curated_and_semantic
from retention_manager import archive_file
SOURCE_FILES = [
    "customers_yyyymmdd.csv",
    "claims_yyyymmdd.csv",
    "policies_yyyymmdd.csv",
    "payments_yyyymmdd.csv",
    "agents_yyyymmdd.csv"
]
def run_pipeline():
    print("============================================")
    print("   InsureDataPipeline - Starting Pipeline   ")
    print("============================================")
    validated_files = []
    for csv_file_name in SOURCE_FILES:
        is_valid = validate_file(csv_file_name)
        if is_valid:
            validated_files.append(csv_file_name)
    print("\n--------------------------------------------")
    print("Validation complete.")
    print("Valid files: " + str(len(validated_files)))
    print("--------------------------------------------")
    preprocessed_files = []
    for csv_file_name in validated_files:
        preprocess_file(csv_file_name)
        preprocessed_files.append(csv_file_name)
    print("\n--------------------------------------------")
    print("Preprocessing complete.")
    print("--------------------------------------------")
    if len(preprocessed_files) > 0:
        build_curated_and_semantic()
        print("\n--------------------------------------------")
        print("Curated and Semantic layers complete.")
        print("--------------------------------------------")
    for csv_file_name in validated_files:
        archive_file(csv_file_name)
    print("\n--------------------------------------------")
    print("Archival complete.")
    print("--------------------------------------------")

    print("\n============================================")
    print("   InsureDataPipeline - Pipeline Complete   ")
    print("============================================")


if __name__ == "__main__":
    run_pipeline()