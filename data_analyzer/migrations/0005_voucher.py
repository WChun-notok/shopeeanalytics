# Generated by Django 5.0.7 on 2024-11-20 02:05

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_analyzer', '0004_keywordanalysis'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Mã voucher duy nhất', max_length=50, unique=True)),
                ('discount_value', models.DecimalField(decimal_places=2, default=Decimal('0.00'), help_text='Số tiền giảm giá', max_digits=10)),
                ('expiration_date', models.DateField(help_text='Ngày hết hạn')),
                ('order', models.OneToOneField(blank=True, help_text='Đơn hàng áp dụng voucher', null=True, on_delete=django.db.models.deletion.CASCADE, to='data_analyzer.order')),
            ],
        ),
    ]
