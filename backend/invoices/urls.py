from django.urls import path
from . import views

urlpatterns = [
    path('api/process-invoice/', views.process_invoice_api, name='process_invoice'),
]