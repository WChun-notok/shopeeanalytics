# Generated by Django 5.0.7 on 2024-11-27 03:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_analyzer', '0005_voucher'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_date', models.DateField(auto_now_add=True)),
                ('review_score', models.DecimalField(decimal_places=2, max_digits=3)),
                ('improvement_plan', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_analyzer.product')),
            ],
        ),
    ]