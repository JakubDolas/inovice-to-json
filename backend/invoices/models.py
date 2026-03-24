from django.db import models

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Numer faktury")
    vendor_nip = models.CharField(max_length=20, blank=True, null=True, verbose_name="NIP Sprzedawcy")
    buyer_nip = models.CharField(max_length=20, blank=True, null=True, verbose_name="NIP Nabywcy")
    total_brutto = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Kwota Brutto")
    
    image_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ścieżka do pliku")
    is_processed = models.BooleanField(default=False, verbose_name="Czy przetworzono przez AI?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")

    def __str__(self):
        return f"{self.invoice_number} - {self.total_brutto} PLN"