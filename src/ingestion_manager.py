import os
import json
import pandas as pd
from utils import get_today_date, build_file_path, extract_file_date
from audit_logger import log_ingestion
INGESTION_FOLDER = "data\\ingestion"
CONTROL_FILES_FOLDER = "config\\control_files"
def validate_file(csv_file_name):
    print("\nValidating: " + csv_file_name)
    csv_file_path = build_file_path(INGESTION_FOLDER, csv_file_name)
    base_name = os.path.splitext(csv_file_name)[0]
    control_file_name = base_name + ".json"
    control_file_path = build_file_path(CONTROL_FILES_FOLDER, control_file_name)
    with open(control_file_path, "r") as control_file:
        control_data = json.load(control_file)
    expected_rows = control_data["expected_rows"]
    expected_columns = control_data["expected_columns"]
    expected_extension = control_data["expected_extension"]
    actual_extension = os.path.splitext(csv_file_name)[1]
    if actual_extension != expected_extension:
        remarks = "FAIL: Wrong extension. Expected " + expected_extension + " but got " + actual_extension
        print(remarks)
        log_ingestion(csv_file_name, "FAIL", expected_rows, 0, expected_columns, [], remarks)
        return False
    if not os.path.exists(csv_file_path):
        remarks = "FAIL: File does not exist at " + csv_file_path
        print(remarks)
        log_ingestion(csv_file_name, "FAIL", expected_rows, 0, expected_columns, [], remarks)
        return False
    df = pd.read_csv(csv_file_path)
    actual_rows = len(df)
    actual_columns = list(df.columns)
    if actual_rows != expected_rows:
        remarks = "FAIL: Row count mismatch. Expected " + str(expected_rows) + " but got " + str(actual_rows)
        print(remarks)
        log_ingestion(csv_file_name, "FAIL", expected_rows, actual_rows, expected_columns, actual_columns, remarks)
        return False
    if actual_columns != expected_columns:
        remarks = "FAIL: Column mismatch. Expected " + str(expected_columns) + " but got " + str(actual_columns)
        print(remarks)
        log_ingestion(csv_file_name, "FAIL", expected_rows, actual_rows, expected_columns, actual_columns, remarks)
        return False
    remarks = "All checks passed"
    print("PASS: " + csv_file_name)
    log_ingestion(csv_file_name, "PASS", expected_rows, actual_rows, expected_columns, actual_columns, remarks)
    return True