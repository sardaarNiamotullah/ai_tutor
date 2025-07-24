from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import os

from .services.pdf_processor import process_pdf
from .services.rag_engine import generate_answer
from .services.vector_search import semantic_search

class PDFUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES["pdf"]
        file_path = os.path.join("media", file.name)

        with open(file_path, "wb+") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        # Process uploaded PDF
        result, language = process_pdf(file_path)

        return Response({"message": "PDF uploaded and processed", "chunks": result[:5], "language": language})  # preview first 3 chunks
    
class StaticPDFProcessView(APIView):
    def get(self, _request):
        file_name = "banglaboi.pdf"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        if not os.path.exists(file_path):
            return Response({"error": f"{file_name} not found in media directory."}, status=status.HTTP_404_NOT_FOUND)

        # Process the static file
        chunks, language = process_pdf(file_path)

        return Response({
            "message": f"{file_name} processed successfully",
            "chunks": chunks[:5],
            "language": language
        })

class RAGQueryView(APIView):
    def post(self, request):
        query = request.data.get("query")
        if not query:
            return Response({"error": "Missing 'query' in request."}, status=status.HTTP_400_BAD_REQUEST)

        chunks = semantic_search(query, top_k=3)
        answer = generate_answer(query)

        return Response({
            "answer": answer,
            "chunks": [{"text": chunk["text"]} for chunk in chunks]
        })