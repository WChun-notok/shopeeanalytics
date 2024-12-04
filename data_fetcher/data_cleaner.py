# data_cleaner.py

import pandas as pd
import numpy as np

# Hàm để loại bỏ các bản ghi trùng lặp
def remove_duplicates(data):
    """
    Loại bỏ các bản ghi trùng lặp trong dữ liệu.
    """
    data = data.drop_duplicates()
    return data

# Hàm để xử lý dữ liệu thiếu
def handle_missing_values(data, strategy="mean"):
    """
    Xử lý các giá trị thiếu trong dữ liệu.
    strategy: Chiến lược xử lý ('mean', 'median', 'mode' hoặc 'drop')
    """
    if strategy == "mean":
        data = data.fillna(data.mean())
    elif strategy == "median":
        data = data.fillna(data.median())
    elif strategy == "mode":
        data = data.fillna(data.mode().iloc[0])
    elif strategy == "drop":
        data = data.dropna()
    return data

# Hàm để chuẩn hóa dữ liệu (loại bỏ khoảng trắng, chuyển chữ thường)
def normalize_text(data, column):
    """
    Chuẩn hóa văn bản: loại bỏ khoảng trắng và chuyển về chữ thường.
    column: Tên cột cần chuẩn hóa.
    """
    data[column] = data[column].str.strip().str.lower()
    return data

# Hàm để phát hiện và loại bỏ các giá trị ngoại lai
def remove_outliers(data, column, threshold=1.5):
    """
    Loại bỏ các giá trị ngoại lai trong cột dựa trên IQR.
    threshold: Ngưỡng phát hiện giá trị ngoại lai (mặc định là 1.5)
    """
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    return data
