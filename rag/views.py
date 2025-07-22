from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import os

from .services.pdf_processor import process_pdf

class PDFUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES["pdf"]
        file_path = os.path.join("media", file.name)

        with open(file_path, "wb+") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        # Process uploaded PDF
        result = process_pdf(file_path)

        return Response({"message": "PDF uploaded and processed", "chunks": result[:3]})  # preview first 3 chunks
    
class StaticPDFProcessView(APIView):
    def get(self, _request):
        file_name = "HSC26-Bangla1st-Paper.pdf"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        if not os.path.exists(file_path):
            return Response({"error": f"{file_name} not found in media directory."}, status=status.HTTP_404_NOT_FOUND)

        # Process the static file
        chunks = process_pdf(file_path)

        return Response({
            "message": f"{file_name} processed successfully",
            "chunks": chunks[:3]  # Preview first 3 chunks
        })
