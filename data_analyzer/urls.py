# urls.py (trong app data_analyzer)

from django.urls import path
from . import views
from .views import homepage, fetch_and_display_data


urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('orders/', views.order_list, name='order_list'),
    path('sales/', views.sales_list, name='sales_list'),
    path('dashboard/', views.dashboard, name='dashboard'),        
    path('', homepage, name='homepage'),  # Trang chủ hiển thị tại root '/'
    path('fetch-display-data/', fetch_and_display_data, name='fetch_display_data'),
    path('export_sales/', views.export_sales_data, name='export_sales'),
    path('search-keyword/', views.search_keyword, name='search_keyword'),
    path('revenue-chart/', views.revenue_chart, name='revenue_chart'),
    path('revenue-data/', views.revenue_data, name='revenue_data'),  # Data endpoint
    path('sales_trends/', views.sales_trends, name='sales_trends'),
    path('plot_sales_trends/', views.plot_sales_trends, name='plot_sales_trends'),
    path('vouchers/', views.voucher_list_view, name='voucher_list'),
    path('vouchers/<int:voucher_id>/', views.voucher_detail, name='voucher_detail'),
    path('products/filter-by-revenue/', views.product_revenue_filter, name='product_revenue_filter'),
    path('predict-sales-trends/', views.predict_sales_trends, name='predict_sales_trends'),
    path('evaluate-product-potential/', views.evaluate_product_potential, name='evaluate_product_potential'),

]
