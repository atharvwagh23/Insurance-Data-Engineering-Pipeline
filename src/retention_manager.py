import os
import shutil
import zipfile
from utils import get_today_date, build_file_path
from audit_logger import log_retention
INGESTION_FOLDER = "data\\ingestion"
CONTROL_FILES_FOLDER = "config\\control_files"
ARCHIVE_FOLDER = "data\\retention\\archive"

def archive_file(csv_file_name):
    print("\nArchiving: " + csv_file_name)
    today = get_today_date()
    archive_zip_name = "archive_" + today + ".zip"
    archive_zip_path = build_file_path(ARCHIVE_FOLDER, archive_zip_name)
    csv_file_path = build_file_path(INGESTION_FOLDER, csv_file_name)
    base_name = os.path.splitext(csv_file_name)[0]
    json_file_name = base_name + ".json"
    json_file_path = build_file_path(CONTROL_FILES_FOLDER, json_file_name)
    temp_csv_path = build_file_path(ARCHIVE_FOLDER, csv_file_name)
    temp_json_path = build_file_path(ARCHIVE_FOLDER, json_file_name)
    if os.path.exists(csv_file_path):
        shutil.move(csv_file_path, temp_csv_path)
        print("Moved CSV to archive folder: " + temp_csv_path)
    if os.path.exists(json_file_path):
        shutil.move(json_file_path, temp_json_path)
        print("Moved JSON to archive folder: " + temp_json_path)
    with zipfile.ZipFile(archive_zip_path, mode="a") as archive_zip:
        if os.path.exists(temp_csv_path):
            archive_zip.write(temp_csv_path, csv_file_name)
            os.remove(temp_csv_path)
        if os.path.exists(temp_json_path):
            archive_zip.write(temp_json_path, json_file_name)
            os.remove(temp_json_path)
    print("Archived into: " + archive_zip_path)
    log_retention(csv_file_name, archive_zip_path, "Archived successfully")