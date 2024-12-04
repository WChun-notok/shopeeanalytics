# admin.py (trong app data_analyzer)

from .models import Product, Order, UserActivity, ExternalProduct, Sales, Customer
from django.contrib import admin
from .models import Product, Voucher

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_value', 'expiration_date', 'order', 'is_valid')
    search_fields = ('code', 'order__customer_name')
    list_filter = ('expiration_date',)

    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True  # Hiển thị biểu tượng true/false trong admin




class SalesAdmin(admin.ModelAdmin):
    list_display = ('sale_date', 'total_orders',
                    'total_revenue')  # Các trường hiển thị
    list_filter = ('sale_date',)  # Bộ lọc theo ngày bán hàng

# Đăng ký model Customer
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')  # Các trường hiển thị trong danh sách
    search_fields = ('name',)  # Cho phép tìm kiếm theo tên sản phẩm
    list_filter = ('price', 'stock')  # Bộ lọc theo giá và số lượng

# Tùy chỉnh giao diện admin cho model Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'order_date')  # Hiển thị thông tin đơn hàng
    list_filter = ('order_date', 'product')  # Bộ lọc theo ngày đặt hàng và sản phẩm
    search_fields = ('product__name',)  # Tìm kiếm theo tên sản phẩm (truy vấn qua quan hệ ForeignKey)

# Tùy chỉnh giao diện admin cho model UserActivity
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')  # Hiển thị người dùng, hành động và thời gian
    search_fields = ('user', 'action')  # Tìm kiếm theo người dùng và hành động
    list_filter = ('action', 'timestamp')  # Bộ lọc theo hành động và thời gian

# Tùy chỉnh giao diện admin cho model ExternalProduct
class ExternalProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'external_id', 'price', 'source')  # Hiển thị thông tin sản phẩm bên ngoài
    search_fields = ('name', 'external_id', 'source')  # Tìm kiếm theo tên, mã ID bên ngoài và nguồn
    list_filter = ('source',)  # Bộ lọc theo nguồn

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number')  # Các trường hiển thị
    # Tìm kiếm theo tên người dùng và số điện thoại
    search_fields = ('user__username', 'phone_number')


# Đăng ký các model vào admin
admin.site.register(Sales, SalesAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(UserActivity)
admin.site.register(ExternalProduct)