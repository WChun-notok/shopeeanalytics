# alerts.py
from .models import Order
from django.core.mail import send_mail
import pandas as pd


def check_sales_alerts():
    orders = Order.objects.all()
    df = pd.DataFrame(list(orders.values('date', 'total_price')))
    sales_summary = df.groupby('date')['total_price'].sum()
    
    # Example: If sales drop more than 20%
    if sales_summary.iloc[-1] < sales_summary.mean() * 0.8:
        send_mail(
            'Sales Alert: Drop Detected',
            'Sales have dropped significantly!',
            'from@example.com',
            ['admin@example.com']
        )
