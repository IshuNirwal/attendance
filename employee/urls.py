# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', EmployeeRegistrationView.as_view(), name='employee-registration'),
    path('login/', EmployeeLoginView.as_view(), name='employee-login'),
    path('scan/', ScanBarcodeView.as_view(), name='scan-barcode'),
]
