"""
URL configuration for shopee_analytics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py (trong thư mục chính của dự án)

from django.contrib import admin
from django.urls import path, include
from data_analyzer.views import homepage # Import view trang chủ

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),  # Cấu hình trang chủ
    path('data-fetcher/', include('data_fetcher.urls')),  # Đường dẫn cho app data_fetcher
    path('', include('data_analyzer.urls')),  # Kết nối URL của data_analyzer vào hệ thống chính

]
