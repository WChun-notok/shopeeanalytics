# models.py (trong app data_fetcher)

from django.db import models


class CSVFile(models.Model):
    file_name = models.CharField(max_length=255)  # Tên tệp CSV
    upload_date = models.DateTimeField(auto_now_add=True)  # Ngày giờ upload
    processed = models.BooleanField(default=False)  # Trạng thái đã xử lý

    def __str__(self):
        return self.file_name
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name