from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'vendor_nip', 'total_brutto', 'is_processed', 'created_at')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('invoice_number', 'vendor_nip', 'buyer_nip')