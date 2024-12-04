# forms.py (trong app data_fetcher)

from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV file")
    xslt_file = forms.FileField(label="Upload XSLT file (tùy chọn)", required=False)
