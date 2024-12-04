# data_analyzer/utils.py

import random

def get_product_reviews(keyword):
    # Thay hàm này bằng API thật nếu có.
    reviews = [
        {"review": "Sản phẩm tuyệt vời", "rating": 5},
        {"review": "Chất lượng kém", "rating": 2},
        {"review": "Đáng giá tiền", "rating": 4},
        # Thêm các đánh giá khác nếu cần
    ]

    # Tính toán điểm đánh giá trung bình
    average_rating = sum([review["rating"] for review in reviews]) / len(reviews)
    return reviews, average_rating
def format_currency_vnd(value):
    """
    Định dạng số thành tiền tệ với đơn vị VND (dấu phẩy ngăn cách hàng nghìn).
    """
    return f"{value:,.0f} VND"  # :,.0f định dạng không có số thập phân, dấu phẩy ngăn cách.
