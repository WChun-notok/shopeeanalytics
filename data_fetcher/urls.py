# urls.py (trong app data_fetcher)

from .views import export_report_pdf
from django.urls import path
from .views import upload_csv, csv_history
urlpatterns = [
    path('upload-csv/', upload_csv, name='upload_csv'),
    path('csv-history/', csv_history, name='csv_history'),
    path('report-pdf/', export_report_pdf, name='report_pdf'),    
]

