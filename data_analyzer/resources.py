# resources.py (trong app data_analyzer)

from .models import Sales
from .models import Order
from import_export import resources
from .models import Product


from import_export import resources
from .models import Product

from import_export import resources
from .models import Product


class ProductResource(resources.ModelResource):
    
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # Thực hiện các thao tác trước khi import dữ liệu
        print("Running before_import checks")
        super().before_import(
            dataset, using_transactions=using_transactions, dry_run=dry_run, **kwargs)

    class Meta:
        model = Product
        import_id_fields = ('id',)  # ID dùng để nhận diện duy nhất khi import
        fields = ('id', 'name', 'description', 'price',
                  'category', 'stock', 'is_available')


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id', 'customer_name', 'product__name',
                  'quantity', 'total_price', 'order_date')
        export_order = ('id', 'customer_name', 'product__name',
                        'quantity', 'total_price', 'order_date')


class SalesResource(resources.ModelResource):
    class Meta:
        model = Sales
        # Các trường cần export
        fields = ('sale_date', 'total_orders', 'total_revenue')
        export_order = ('sale_date', 'total_orders',
                        'total_revenue')  # Thứ tự các trường
