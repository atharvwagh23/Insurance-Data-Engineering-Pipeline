import os
import pandas as pd
from utils import get_today_date, extract_file_date, build_file_path
from audit_logger import log_preprocess
INGESTION_FOLDER = "data\\ingestion"
PREPROCESSED_FOLDER = "data\\preprocessed"
def preprocess_file(csv_file_name):
    print("\nPreprocessing: " + csv_file_name)
    csv_file_path = build_file_path(INGESTION_FOLDER, csv_file_name)
    df = pd.read_csv(csv_file_path)
    rows_before = len(df)
    df = df.drop_duplicates()
    df = df.dropna(how="all")
    
    object_cols = df.select_dtypes(include=["object"]).columns
    for col in object_cols:
        df[col] = df[col].astype(str).str.strip()
    df.replace("", pd.NA, inplace=True)
    
    rows_after = len(df)
    duplicates_removed = rows_before - rows_after
    df["ingestion_date"] = get_today_date()
    df["file_date"] = extract_file_date(csv_file_name)
    base_name = os.path.splitext(csv_file_name)[0]
    parquet_file_name = base_name + ".parquet"
    parquet_file_path = build_file_path(PREPROCESSED_FOLDER, parquet_file_name)
    df.to_parquet(parquet_file_path, index=False)
    log_preprocess(csv_file_name, rows_before, rows_after, duplicates_removed, "Preprocessed Successfully")
    print("Saved: " + parquet_file_path)