from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PDFChunk
from .pipeline.ingest_pipeline import ingest_pdf_data
from .core.query_handler import handle_query

class RAGQueryView(APIView):
    def post(self, request):
        query = request.data.get("query")
        if not query:
            return Response({"error": "Missing 'query' in request."}, status=status.HTTP_400_BAD_REQUEST)

        print(f"[RAGQueryView] 🔍 Received query: {query}")
        answer, chunks = handle_query(query)

        return Response({
            "answer": answer,
            "chunks": chunks
        })

class RAGResetView(APIView):
    def post(self, request):
        query = request.data.get("query")
        book_name = request.data.get("book")

        if not query or not book_name:
            return Response({"error": "Missing 'query' or 'book' in request."}, status=status.HTTP_400_BAD_REQUEST)

        print(f"[RAGResetView] 🔁 Resetting with book: {book_name}")

        # Step 1: Delete all existing chunks
        deleted_count, _ = PDFChunk.objects.all().delete()
        print(f"[RAGResetView] 🗑️ Deleted {deleted_count} PDFChunk(s)")

        # Step 2: Re-run embedding from scratch
        ingest_pdf_data(book_name)

        # Step 3: Handle the query like normal
        print(f"[RAGResetView] 🔍 Processing query: {query}")
        answer, chunks = handle_query(query)

        return Response({
            "message": f"Reset done. Processed book: {book_name}",
            "answer": answer,
            "chunks": chunks
        })