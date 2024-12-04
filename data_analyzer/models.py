# models.py (trong app data_analyzer)
from django.db import models
from django.utils.timezone import now
from decimal import Decimal
from django.db import models
from django.db.models import Sum, F

class Product(models.Model):
    id = models.AutoField(primary_key=True)  # Khóa chính tự động tăng
    name = models.CharField(max_length=255)  # Tên sản phẩm
    description = models.TextField()         # Mô tả sản phẩm
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá sản phẩm
    category = models.CharField(max_length=255)  # Loại sản phẩm
    stock = models.IntegerField()            # Số lượng tồn kho
    is_available = models.BooleanField(default=True)  # Tình trạng hàng có sẵn
    def calculate_total_revenue(self):
        """
        Tính tổng doanh thu của sản phẩm này.
        """
        return Order.objects.filter(product=self).aggregate(
            total_revenue=Sum(F('quantity') * F('price'))
        )['total_revenue'] or 0
    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=255)  # Tên khách hàng
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Sản phẩm trong đơn hàng (quan hệ nhiều-1 với Product)
    quantity = models.IntegerField()                  # Số lượng sản phẩm
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Tổng giá trị đơn hàng
    order_date = models.DateTimeField(auto_now_add=True)  # Ngày đặt hàng
    
    def save(self, *args, **kwargs):
        # Tính tổng giá trị đơn hàng khi lưu (quantity * product.price)
        self.total_price = self.quantity * self.product.price
        super(Order, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"
# models.py (trong app data_analyzer)

class Sales(models.Model):
    sale_date = models.DateField()                      # Ngày ghi nhận doanh số
    total_orders = models.IntegerField()                # Tổng số đơn hàng trong ngày
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)  # Tổng doanh thu trong ngày
    
    def __str__(self):
        return f"Sales on {self.sale_date}"
# models.py (trong app data_analyzer)

from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Liên kết với model User của Django
    address = models.CharField(max_length=255)  # Địa chỉ của khách hàng
    phone_number = models.CharField(max_length=15)  # Số điện thoại
    
    def __str__(self):
        return f"Customer {self.user.username}"
# models.py (trong app data_analyzer)

class Voucher(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="Mã voucher duy nhất")
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), help_text="Số tiền giảm giá")
    expiration_date = models.DateField(help_text="Ngày hết hạn")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True, help_text="Đơn hàng áp dụng voucher")

    def is_valid(self):
        """
        Kiểm tra xem voucher còn hiệu lực hay không.
        """
        return self.expiration_date >= now().date()

    def __str__(self):
        return f"{self.code} - {'Hết hạn' if not self.is_valid() else 'Còn hạn'}"
class UserActivity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Sản phẩm liên quan
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Người dùng thực hiện hành vi
    views = models.IntegerField(default=0)  # Số lần xem sản phẩm
    clicks = models.IntegerField(default=0)  # Số lượt click vào sản phẩm
    added_to_cart = models.IntegerField(default=0)  # Số lượt thêm vào giỏ hàng
    purchased = models.IntegerField(default=0)  # Số lần mua hàng
    
    def __str__(self):
        return f"Activity for {self.product.name} by {self.user.user.username}"
class ExternalProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name
class KeywordAnalysis(models.Model):
    keyword = models.CharField(max_length=255, unique=True)  # Từ khóa
    search_count = models.IntegerField(default=0)  # Số lần tìm kiếm từ khóa
    average_rating = models.FloatField(null=True, blank=True)  # Đánh giá trung bình
    last_searched = models.DateTimeField(auto_now=True)  # Thời điểm tìm kiếm cuối cùng

    def __str__(self):
        return f"{self.keyword} - {self.search_count} searches"    

class ProductReview(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    review_date = models.DateField(auto_now_add=True)
    review_score = models.DecimalField(max_digits=3, decimal_places=2)  # 1.0 to 5.0
    improvement_plan = models.TextField()  # Plan to enhance quality

    def __str__(self):
        return f"Review for {self.product.name} on {self.review_date}"    