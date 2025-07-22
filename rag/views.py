from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
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
