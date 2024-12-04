# data_analyzer.py

import pandas as pd

# Hàm tính toán số liệu thống kê cơ bản
def calculate_statistics(data):
    """
    Tính toán các số liệu thống kê cơ bản từ dữ liệu.
    data: DataFrame của dữ liệu.
    """
    statistics = {
        "total_products": len(data),
        "total_revenue": data['price'].sum(),
        "average_price": data['price'].mean(),
        "max_price": data['price'].max(),
        "min_price": data['price'].min(),
    }
    return statistics

# Hàm chuẩn bị dữ liệu cho biểu đồ doanh thu theo sản phẩm
def revenue_per_product(data):
    """
    Chuẩn bị dữ liệu doanh thu theo sản phẩm để biểu diễn biểu đồ.
    """
    revenue_data = data.groupby('name')['price'].sum().reset_index()
    return revenue_data
