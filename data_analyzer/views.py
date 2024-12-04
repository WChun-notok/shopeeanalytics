# views.py (trong app data_analyzer)
# Ensure the correct import based on your app structure
from django.db.models import Sum, Avg
from .models import Product, Order, ProductReview
from .models import Sales
from django.http import JsonResponse
from .models import Sales
from django.http import HttpResponse
from .resources import SalesResource
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from .models import Product, Order, Sales  # Import các model cần sử dụng
from django.db.models import Sum  # Import Sum để tính tổng doanh thu
from .models import Product, Order, Sales
from .models import Order, Sales, Product, ExternalProduct
from django.shortcuts import render, get_object_or_404
import pandas as pd
from .external_data import fetch_data_from_api
from django.contrib import messages
from .models import KeywordAnalysis
from django.utils import timezone
# Giả sử bạn đã tạo hàm này để lấy đánh giá sản phẩm
from .utils import get_product_reviews
import io
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from django.utils.timezone import make_naive
from data_analyzer.models import Voucher
from django.db.models import Sum, F
import pandas as pd
from django.shortcuts import render
from .models import Order
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def sales_trends(request):
    # Use 'order_date' instead of 'date' for grouping
    monthly_sales = (
        Order.objects
        .annotate(month=TruncMonth('order_date'))
        .values('month')
        .annotate(total_revenue=Sum('total_price'))
        .order_by('month')
    )

    # Convert QuerySet to list of dictionaries
    data = {
        "months": [item['month'].strftime('%Y-%m') for item in monthly_sales],
        "revenues": [item['total_revenue'] for item in monthly_sales]
    }

    return render(request, 'data_analyzer/sales_trends.html', {'data': data})


def plot_sales_trends(request):
    # Fetch data for plotting from the sales_trends view
    monthly_sales = (
        Order.objects
        .annotate(month=TruncMonth('order_date'))
        .values('month')
        .annotate(total_revenue=Sum('total_price'))
        .order_by('month')
    )

    months = [make_naive(item['month']) for item in monthly_sales]
    revenues = [item['total_revenue'] for item in monthly_sales]

    # Plot the data using matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot_date(months, revenues, '-')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.xlabel('Month')
    plt.ylabel('Total Revenue (VND)')
    plt.title('Sales Trends by Month')
    plt.gcf().autofmt_xdate()

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Return image as a response
    return HttpResponse(buf, content_type='image/png')


def dashboard(request):
    products = Product.objects.all()
    orders = Order.objects.all()
    sales = Sales.objects.all()

    # Render dữ liệu vào template dashboard.html
    return render(request, 'data_analyzer/dashboard.html', {
        'products': products,
        'orders': orders,
        'sales': sales,
    })


def sales_list(request):
    # Lấy danh sách doanh số từ cơ sở dữ liệu
    sales = Sales.objects.all()

    # Render dữ liệu vào template sales_list.html
    return render(request, 'data_analyzer/sales_list.html', {'sales': sales})


def sales_trends(request):
    # Find the top 5 most purchased products
    top_products = (
        Order.objects
        .values('product__name')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:5]
    )

    # Find the top 5 customers who have made the most purchases
    top_customers = (
        Order.objects
        .values('customer_name')
        .annotate(total_spending=Sum('total_price'))
        .order_by('-total_spending')[:5]
    )

    # Prepare data for the pie charts
    product_labels = [product['product__name'] for product in top_products]
    product_quantities = [product['total_quantity'] for product in top_products]
    customer_labels = [customer['customer_name'] for customer in top_customers]
    customer_spending = [customer['total_spending'] for customer in top_customers]

    context = {
        'top_products': top_products,
        'top_customers': top_customers,
        'product_labels': product_labels,
        'product_quantities': product_quantities,
        'customer_labels': customer_labels,
        'customer_spending': customer_spending,
    }
    return render(request, 'data_analyzer/sales_trends.html', context)


def order_list(request):
    # Lấy danh sách tất cả các đơn hàng từ cơ sở dữ liệu
    orders = Order.objects.all()

    # Render dữ liệu vào template order_list.html
    return render(request, 'data_analyzer/order_list.html', {'orders': orders})


def product_list(request):
    # Lấy danh sách tất cả các sản phẩm từ cơ sở dữ liệu
    products = Product.objects.all()

    # Render dữ liệu vào template product_list.html
    return render(request, 'data_analyzer/product_list.html', {'products': products})


def homepage(request):
    # Lấy dữ liệu doanh thu theo tháng
    monthly_sales = Sales.objects.annotate(month=TruncMonth('sale_date')).values(
        'month').annotate(total_revenue=Sum('total_revenue')).order_by('month')

    # Lấy dữ liệu doanh thu theo quý
    quarterly_sales = Sales.objects.annotate(quarter=TruncQuarter('sale_date')).values(
        'quarter').annotate(total_revenue=Sum('total_revenue')).order_by('quarter')

    # Lấy dữ liệu doanh thu theo năm
    yearly_sales = Sales.objects.annotate(year=TruncYear('sale_date')).values(
        'year').annotate(total_revenue=Sum('total_revenue')).order_by('year')

    # Chuẩn bị dữ liệu cho biểu đồ
    # Để nguyên giá trị datetime, không định dạng ở đây
    labels = [sale['month'] for sale in monthly_sales]
    data = [sale['total_revenue'] for sale in monthly_sales]

    context = {
        'monthly_sales': monthly_sales,
        'quarterly_sales': quarterly_sales,
        'yearly_sales': yearly_sales,
        'labels': labels,
        'data': data,
    }

    return render(request, 'homepage.html', context)
# views.py (trong app data_analyzer)


def export_sales_data(request):
    sales_resource = SalesResource()
    dataset = sales_resource.export()

    # Xuất dữ liệu dưới dạng CSV
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_data.csv"'
    return response


def fetch_and_display_data(request):
    # Gọi hàm lấy dữ liệu từ API
    data = fetch_data_from_api()

    # Nếu không có dữ liệu, hiển thị thông báo lỗi
    if data is None:
        messages.error(
            request, "Không thể lấy dữ liệu từ API hoặc dữ liệu không hợp lệ.")
    else:
        # Xóa dữ liệu cũ để tránh dữ liệu trùng lặp
        ExternalProduct.objects.all().delete()

        # Lưu dữ liệu mới vào cơ sở dữ liệu
        for item in data:
            ExternalProduct.objects.update_or_create(
                name=item['name'],
                defaults={
                    'price': item['price'],
                    'stock': item['stock']
                }
            )
        messages.success(
            request, "Dữ liệu từ API đã được cập nhật thành công.")

    # Lấy tất cả dữ liệu từ ExternalProduct để hiển thị
    products = ExternalProduct.objects.all()
    return render(request, 'data_analyzer/display_data.html', {'products': products})
# data_analyzer/views.py


def search_keyword(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')

        # Tìm hoặc tạo mới từ khóa trong database
        keyword_entry, created = KeywordAnalysis.objects.get_or_create(
            keyword=keyword)

        # Cập nhật số lần tìm kiếm
        keyword_entry.search_count += 1
        keyword_entry.last_searched = timezone.now()
        keyword_entry.save()

        # Giả sử đánh giá sản phẩm được lấy từ API hoặc nguồn dữ liệu khác (ví dụ từ một hàm `get_product_reviews`)
        reviews, average_rating = get_product_reviews(keyword)

        # Cập nhật đánh giá trung bình
        keyword_entry.average_rating = average_rating
        keyword_entry.save()

        context = {
            'keyword_entry': keyword_entry,
            'reviews': reviews,
        }

        return render(request, 'data_analyzer/keyword_results.html', context)
    else:
        return render(request, 'data_analyzer/search_keyword.html')


def search_keyword(request):
    context = {}

    if request.method == 'POST':
        keyword = request.POST.get('keyword')

        # Tìm hoặc tạo từ khóa trong database
        keyword_entry, created = KeywordAnalysis.objects.get_or_create(
            keyword=keyword)

        # Cập nhật số lần tìm kiếm và thời gian tìm kiếm cuối
        keyword_entry.search_count += 1
        keyword_entry.last_searched = timezone.now()
        keyword_entry.save()

        # Lấy đánh giá sản phẩm cho từ khóa
        reviews, average_rating = get_product_reviews(keyword)

        # Cập nhật đánh giá trung bình cho từ khóa
        keyword_entry.average_rating = average_rating
        keyword_entry.save()

        # Truyền dữ liệu vào context
        context = {
            'keyword_entry': keyword_entry,
            'reviews': reviews,
        }

    return render(request, 'data_analyzer/search_keyword.html', context)

# views.py in your app


def revenue_data(request):
    # Group sales data by month and aggregate revenue
    monthly_data = (
        Sales.objects
        .annotate(month=TruncMonth('sale_date'))
        .values('month')
        .annotate(total_revenue=Sum('total_revenue'))
        .order_by('month')
    )
    # Convert QuerySet to list of dictionaries
    data = {
        "months": [item['month'].strftime('%Y-%m') for item in monthly_data],
        "revenues": [item['total_revenue'] for item in monthly_data]
    }
    return JsonResponse(data)


def revenue_chart(request):
    return render(request, 'data_analyzer/revenue_chart.html')


def voucher_list_view(request):
    query = request.GET.get('q', '')  # Lấy giá trị từ tham số 'q' trong URL
    if query:
        vouchers = Voucher.objects.filter(
            code__icontains=query  # Tìm kiếm theo mã voucher
        ) | Voucher.objects.filter(
            order__customer_name__icontains=query  # Tìm kiếm theo tên khách hàng
        )
    else:
        vouchers = Voucher.objects.all()

    return render(request, 'data_analyzer/voucher_list.html', {'vouchers': vouchers, 'query': query})


def voucher_detail(request, voucher_id):
    """
    Hiển thị chi tiết voucher và đơn hàng liên quan (nếu có).
    """
    voucher = get_object_or_404(Voucher, id=voucher_id)
    context = {
        'voucher': voucher,
        'related_order': voucher.order if voucher.order else None
    }
    return render(request, 'data_analyzer/voucher_detail.html', context)


def product_revenue_filter(request):
    """
    Hiển thị danh sách sản phẩm được lọc theo doanh thu.
    """
    # Lấy giá trị từ query parameters (nếu có)
    min_revenue = request.GET.get('min_revenue', 0)
    max_revenue = request.GET.get('max_revenue', None)

    # Query tính doanh thu của mỗi sản phẩm
    products = Product.objects.annotate(
        total_revenue=Sum(F('order__quantity') * F('price'))
    )

    # Áp dụng lọc theo doanh thu
    if min_revenue:
        products = products.filter(total_revenue__gte=float(min_revenue))
    if max_revenue:
        products = products.filter(total_revenue__lte=float(max_revenue))

    context = {
        'products': products,
        'min_revenue': min_revenue,
        'max_revenue': max_revenue
    }
    return render(request, 'data_analyzer/product_revenue_filter.html', context)


def predict_sales_trends(request):
    """
    Xử lý dữ liệu và dự đoán xu hướng mua hàng dựa trên quantity và total_price.
    """
    # Lấy dữ liệu từ model Order
    orders = Order.objects.values('quantity', 'total_price')

    if not orders:
        return render(request, 'data_analyzer/predict_sales_trends.html', {
            'error': 'Không có dữ liệu đủ để dự đoán.'
        })

    # Tạo DataFrame từ QuerySet
    df = pd.DataFrame(list(orders))

    if df.empty or len(df) < 2:
        return render(request, 'data_analyzer/predict_sales_trends.html', {
            'error': 'Dữ liệu không đủ để thực hiện dự đoán.'
        })

    # Thêm chỉ số tháng hoặc tuần tự để làm cơ sở tính toán
    df['index'] = np.arange(len(df))  # Sử dụng chỉ số tuần tự làm biến độc lập

    # Chuẩn bị dữ liệu cho mô hình
    X = df[['index']].values  # Biến độc lập là chỉ số tuần tự
    y = df['total_price'].values  # Biến phụ thuộc là tổng doanh thu

    # Huấn luyện mô hình Linear Regression
    model = LinearRegression()
    model.fit(X, y)

    # Dự đoán 12 bước tiếp theo (các khoảng dữ liệu mới)
    future_indices = np.arange(len(df), len(df) + 12).reshape(-1, 1)
    future_predictions = model.predict(future_indices)

    # Tạo biểu đồ
    plt.figure(figsize=(10, 6))
    plt.plot(df['index'], y, label='Doanh thu thực tế',
             color='blue', linewidth=2)  # Đường thực tế
    plt.plot(future_indices, future_predictions, label='Dự đoán',
             linestyle='--', color='orange', linewidth=2)  # Đường dự đoán
    plt.xlabel('Chỉ số (Index)')
    plt.ylabel('Doanh thu (VND)')
    plt.title('Dự đoán xu hướng doanh thu dựa trên quantity và total_price')
    plt.legend()

    # Chuyển đổi biểu đồ thành image để hiển thị
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    chart = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'data_analyzer/predict_sales_trends.html', {
        'chart': chart,
        'future_predictions': zip(range(len(df), len(df) + 12), future_predictions)
    })

# views.py


def evaluate_product_potential(request):
    """
    Evaluates the top 5 products with the highest revenue and provides improvement suggestions.
    """
    # Calculate revenue for each product
    product_revenues = (
        Order.objects.values('product__name')
        .annotate(total_revenue=Sum('total_price'))
        .order_by('-total_revenue')[:5]  # Limit to top 5 products
    )

    # Generate improvement suggestions for top 5 products
    suggestions = []
    for product in product_revenues:
        review_score = ProductReview.objects.filter(product__name=product['product__name']).aggregate(avg_score=Avg('review_score'))['avg_score']
        if review_score is None or review_score < 4.0:  # Threshold for improvement
            suggestions.append({
                'product_name': product['product__name'],
                'total_revenue': product['total_revenue'],
                'plan': f"Nên chủ động tập trung nâng cao chất lượng {product['product__name']} nhằm đạt tới mức đánh giá 4.0 từ khách hàng."
            })

    # Generate revenue chart for top 5 products
    product_names = [item['product__name'] for item in product_revenues]
    revenues = [item['total_revenue'] for item in product_revenues]

    plt.figure(figsize=(8, 5))
    plt.bar(product_names, revenues, color='skyblue')
    plt.xlabel('Sản phẩm')
    plt.ylabel('Doanh thu (VND)')
    plt.title('Bảng so sánh doanh thu theo 5 mặt hàng tiềm năng nhất')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Convert chart to image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return render(request, 'data_analyzer/evaluate_product_potential.html', {
        'high_potential_products': product_revenues,
        'suggestions': suggestions,
        'chart': chart,
    })