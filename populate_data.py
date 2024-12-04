import os
import django
import random
import datetime
from django.utils import timezone

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopee_analytics.settings')
django.setup()

from data_analyzer.models import Product, Order, Sales, Voucher

def populate_products(num_products=500):
    categories = [
        {"name": "Electronics", "products": ["Smartphone", "Laptop", "Tablet", "Smartwatch", "Headphones"]},
        {"name": "Fashion", "products": ["T-Shirt", "Jeans", "Sneakers", "Handbag", "Jacket"]},
        {"name": "Home Appliances", "products": ["Air Conditioner", "Vacuum Cleaner", "Refrigerator", "Microwave", "Washing Machine"]},
    ]

    products = []
    for _ in range(num_products):
        category = random.choice(categories)
        product_name = random.choice(category["products"])
        product = Product(
            name=f"{product_name} #{random.randint(1, 1000)}",  # Unique product names
            description=f"{product_name} from {category['name']} category",
            price=random.uniform(200000, 2000000),  # Random price between 200k - 2M
            category=category["name"],
            stock=random.randint(5, 500)  # Random stock between 5 and 500
        )
        products.append(product)

    Product.objects.bulk_create(products)
    print(f"{num_products} products added successfully.")

def populate_orders(num_orders=1500):
    products = Product.objects.all()
    orders = []
    for _ in range(num_orders):
        product = random.choice(products)
        customer_name = f"Customer #{random.randint(1, 500)}"  # Unique customer names
        order_date = timezone.now() - datetime.timedelta(days=random.randint(1, 365))  # Orders within the last year
        quantity = random.randint(1, 10)

        order = Order(
            customer_name=customer_name,
            product=product,
            quantity=quantity,
            order_date=order_date,
        )
        order.total_price = quantity * product.price
        orders.append(order)

    Order.objects.bulk_create(orders)
    print(f"{num_orders} orders added successfully.")

def populate_sales():
    # Generate monthly sales data for the past 12 months
    current_date = timezone.now()
    sales_data = []
    for i in range(12):  # 12 months
        month_start = current_date.replace(day=1) - datetime.timedelta(days=i * 30)
        total_orders = random.randint(200, 500)  # More orders for larger data
        total_revenue = total_orders * random.uniform(500000, 2000000)  # Average revenue per order

        sales = Sales(
            sale_date=month_start.date(),
            total_orders=total_orders,
            total_revenue=total_revenue
        )
        sales_data.append(sales)

    Sales.objects.bulk_create(sales_data)
    print("Sales data added successfully.")

def populate_vouchers():
    orders = Order.objects.all()
    vouchers = []

    for order in orders:
        if order.quantity >= 5:  # Apply Voucher if order quantity >= 5
            voucher_code = f"VOUCHER-{order.id}-{random.randint(1000, 9999)}"
            discount_value = random.uniform(50000, 200000)  # Random discount between 50k - 200k
            voucher = Voucher(
                code=voucher_code,
                order=order,
                discount_value=discount_value,
                expiration_date=timezone.now() + datetime.timedelta(days=30)  # Valid for 30 days
            )
            vouchers.append(voucher)

    Voucher.objects.bulk_create(vouchers)
    print(f"{len(vouchers)} vouchers added successfully.")

if __name__ == '__main__':
    populate_products(500)  # 500 products
    populate_orders(1500)  # 1500 orders
    populate_sales()       # 12 months of sales data
    populate_vouchers()    # Vouchers for eligible orders
