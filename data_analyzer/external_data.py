import requests

def fetch_data_from_api():
    """
    Lấy dữ liệu từ API bên ngoài và trả về JSON.
    Xử lý các lỗi có thể xảy ra khi kết nối đến API.
    """
    api_url = "https://api.example.com/products"  # Thay đổi URL API
    headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}  # Nếu API yêu cầu xác thực

    try:
        response = requests.get(api_url, headers=headers, timeout=10)  # Thời gian chờ 10 giây

        # Kiểm tra mã trạng thái của phản hồi
        response.raise_for_status()
        data = response.json()

        # Kiểm tra tính hợp lệ của dữ liệu
        if isinstance(data, list) and all('name' in item and 'price' in item and 'stock' in item for item in data):
            return data
        else:
            print("Dữ liệu không hợp lệ: Thiếu trường cần thiết")
            return None

    except requests.exceptions.Timeout:
        print("Lỗi: Quá thời gian chờ khi kết nối đến API")
    except requests.exceptions.ConnectionError:
        print("Lỗi: Không thể kết nối đến API")
    except requests.exceptions.HTTPError as http_err:
        print(f"Lỗi HTTP: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Lỗi không xác định khi gọi API: {req_err}")

    return None
