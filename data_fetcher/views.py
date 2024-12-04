# views.py (trong app data_fetcher)

import os
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm
from .models import CSVFile
import csv
import requests
from .models import Product

from django.shortcuts import render
from .models import CSVFile, Product

# Upload và xử lý tệp CSV
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm
from .models import CSVFile, Product
import pandas as pd
import csv
from io import StringIO


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CSVUploadForm
from .models import CSVFile, Product
import pandas as pd
import csv
from io import StringIO


# data_fetcher/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from lxml import etree  # Thư viện để xử lý XML và XSLT
from .forms import CSVUploadForm
from .models import CSVFile, Product
import pandas as pd
from io import StringIO


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        # Lấy file XSLT nếu được tải lên cùng CSV
        xslt_file = request.FILES.get('xslt_file')

        if form.is_valid() and 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            data = pd.read_csv(StringIO(decoded_file))

            # Lưu dữ liệu từ CSV vào database
            for _, row in data.iterrows():
                Product.objects.update_or_create(
                    name=row['name'],
                    defaults={'price': row['price'], 'stock': row['stock']}
                )

            # Nếu file XSLT được tải lên, áp dụng chuyển đổi
            if xslt_file:
                try:
                    # Đọc file XSLT và chuẩn bị chuyển đổi
                    xslt_content = xslt_file.read()
                    xslt_root = etree.XML(xslt_content)
                    transform = etree.XSLT(xslt_root)

                    # Tạo XML từ dữ liệu để áp dụng XSLT
                    xml_root = etree.Element("Products")
                    for product in Product.objects.all():
                        product_el = etree.SubElement(xml_root, "Product")
                        etree.SubElement(
                            product_el, "Name").text = product.name
                        etree.SubElement(product_el, "Price").text = str(
                            product.price)
                        etree.SubElement(product_el, "Stock").text = str(
                            product.stock)

                    # Chuyển đổi XML bằng XSLT
                    transformed_xml = transform(xml_root)
                    return HttpResponse(str(transformed_xml), content_type="application/xml")

                except Exception as e:
                    messages.error(request, f"Lỗi khi xử lý file XSLT: {e}")
                    return redirect('upload_csv')

            messages.success(
                request, "Tệp CSV đã được upload và xử lý thành công.")
            return redirect('upload_csv')

    else:
        form = CSVUploadForm()

    return render(request, 'data_fetcher/upload_csv.html', {'form': form})

# views.py (trong app data_fetcher)


def csv_history(request):
    csv_files = CSVFile.objects.all().order_by('-upload_date')
    return render(request, 'data_fetcher/csv_history.html', {'csv_files': csv_files})


# views.py
def export_report_pdf(request):
    # Truy vấn dữ liệu từ model Product và chuyển thành DataFrame
    data = Product.objects.all().values('name', 'price', 'stock')
    if not data:
        return HttpResponse("Không có dữ liệu để tạo báo cáo", status=404)

    df = pd.DataFrame(list(data))

    # Kiểm tra sự tồn tại của các cột cần thiết trong DataFrame
    if 'price' not in df.columns or 'stock' not in df.columns:
        return HttpResponse("Dữ liệu không hợp lệ hoặc thiếu cột 'price' hoặc 'stock'", status=400)

    # Tính toán số liệu thống kê
    statistics = {
        "total_products": len(df),
        "total_revenue": df['price'].sum(),
        "average_price": df['price'].mean(),
        "max_price": df['price'].max(),
        "min_price": df['price'].min(),
    }

    # Render nội dung HTML từ template
    html_content = render_to_string(
        'data_fetcher/report.html', {'statistics': statistics})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Tạo PDF từ HTML
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    if pisa_status.err:
        return HttpResponse("Có lỗi khi tạo PDF", status=500)

    return response
