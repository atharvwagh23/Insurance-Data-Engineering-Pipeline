import csv
import os
from utils import get_today_date, build_file_path

LOGS_FOLDER = "logs"

def log_ingestion(file_name, status, expected_rows, actual_rows, expected_columns, actual_columns, remarks):
    today = get_today_date()
    log_file_name = "ingestion_log_" + today + ".csv"
    log_file_path = build_file_path(LOGS_FOLDER, log_file_name)
    file_exists = os.path.exists(log_file_path)
    with open(log_file_path, mode="a", newline="") as log_file:
        writer = csv.writer(log_file)
        if not file_exists:
            writer.writerow([
                "file_name",
                "status",
                "expected_rows",
                "actual_rows",
                "expected_columns",
                "actual_columns",
                "remarks",
                "log_date"
            ])
        writer.writerow([
            file_name,
            status,
            expected_rows,
            actual_rows,
            expected_columns,
            actual_columns,
            remarks,
            today
        ])
    print("Ingestion log updated: " + log_file_path)

def log_preprocess(file_name, rows_before, rows_after, duplicates_removed, remarks):
    today = get_today_date()
    log_file_name = "preprocess_log_" + today + ".csv"
    log_file_path = build_file_path(LOGS_FOLDER, log_file_name)
    file_exists = os.path.exists(log_file_path)
    with open(log_file_path, mode="a", newline="") as log_file:
        writer = csv.writer(log_file)
        if not file_exists:
            writer.writerow([
                "file_name",
                "rows_before",
                "rows_after",
                "duplicates_removed",
                "remarks",
                "log_date"
            ])
        writer.writerow([
            file_name,
            rows_before,
            rows_after,
            duplicates_removed,
            remarks,
            today
        ])
    print("Preprocess log updated: " + log_file_path)

def log_retention(file_name, archive_path, remarks):
    today = get_today_date()
    log_file_name = "retention_log_" + today + ".csv"
    log_file_path = build_file_path(LOGS_FOLDER, log_file_name)
    file_exists = os.path.exists(log_file_path)
    with open(log_file_path, mode="a", newline="") as log_file:
        writer = csv.writer(log_file)
        if not file_exists:
            writer.writerow([
                "file_name",
                "archive_path",
                "remarks",
                "log_date"
            ])
        writer.writerow([
            file_name,
            archive_path,
            remarks,
            today
        ])
    print("Retention log updated: " + log_file_path)