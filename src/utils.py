import os
from datetime import datetime
def get_today_date():
    today = datetime.now()
    today_str = today.strftime("%Y%m%d")
    return today_str
def extract_file_date(file_name):
    base_name = os.path.splitext(file_name)[0]
    parts = base_name.split("_")
    file_date = parts[-1]
    return file_date
def build_file_path(folder_path, file_name):
    full_path = os.path.join(folder_path, file_name)
    return full_path