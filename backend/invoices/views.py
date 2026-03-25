import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage
from dotenv import load_dotenv
from django.http import FileResponse

from .models import Invoice
from .serializers import InvoiceSerializer

from src.image_processing import ImagePreprocessor
from src.processor import InvoiceExtractor

load_dotenv()

@api_view(['POST'])
def process_invoice_api(request):
    if 'invoice_image' not in request.FILES:
        return Response({"error": "Brak zdjęcia faktury w żądaniu."}, status=400)

    file_obj = request.FILES['invoice_image']
    
    file_name = default_storage.save(f"data/uploads/{file_obj.name}", file_obj)
    full_path = default_storage.path(file_name)

    try:
        preprocessor = ImagePreprocessor()
        clean_path = preprocessor.clean_invoice(full_path)

        extractor = InvoiceExtractor(os.getenv("GROQ_API_KEY"))
        ai_result = extractor.extract_data(clean_path)

        if "error" in ai_result:
            return Response({"error": ai_result["error"]}, status=400)

        invoice = Invoice.objects.create(
            invoice_number=ai_result.get('nr_faktury'),
            vendor_nip=ai_result.get('sprzedawca_nip'),
            buyer_nip=ai_result.get('nabywca_nip'),
            total_brutto=ai_result.get('total_brutto'),
            image_path=full_path,
            is_processed=True
        )

        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data, status=201)

    except Exception as e:
        return Response({"error": f"Błąd serwera: {str(e)}"}, status=500)
    
@api_view(['GET'])
def get_invoices(request):
    invoices = Invoice.objects.all().order_by('-created_at')
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def invoice_detail_api(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return Response({"error": "Nie znaleziono faktury"})
    
    if request.method == 'GET':
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = InvoiceSerializer(invoice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        invoice.delete()
        return Response(status=204)
    
@api_view(['GET'])
def get_invoice_image(request, pk):
    try:
        invoice = Invoice.objects.get(pk=pk)
        if invoice.image_path and os.path.exists(invoice.image_path):
            return FileResponse(open(invoice.image_path, 'rb'))
        return Response({"error": "Brak pliku na serwerze"}, status=404)
    except Invoice.DoesNotExist:
        return Response({"error": "Nie znaleziono faktury"}, status=404)