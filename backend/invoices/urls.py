from django.urls import path
from . import views

urlpatterns = [
    path('api/process-invoice/', views.process_invoice_api, name='process_invoice'),
    path('api/invoices/', views.get_invoices, name='get_invoices'),
    
    path('api/invoices/<int:pk>/', views.invoice_detail_api, name='invoice_detail'),
    path('api/invoices/<int:pk>/image/', views.get_invoice_image, name='get_invoice'),
]