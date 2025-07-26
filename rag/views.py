from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PDFChunk
from .pipeline.ingest_pipeline import ingest_pdf_data
from .core.query_handler import handle_query


# ---------------------------------------------------------------------
# 🧠 RAGQueryView handles user queries for the Retrieval-Augmented Generation (RAG) system.
# ---------------------------------------------------------------------
class RAGQueryView(APIView):
    def post(self, request):
        # 🔹 Step 1: Extract the 'query' from incoming POST request data
        query = request.data.get("query")
        if not query:
            # ❗ Return error if 'query' is missing in request
            return Response(
                {"error": "Missing 'query' in request."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔹 Step 2: Handle the query using the RAG pipeline (retrieval + LLM answer generation)
        result = handle_query(query)

        # 🔹 Step 3: Return only the final answer + evaluation scores
        return Response({
            "answer": result["answer"],             # LLM-generated answer
            # "chunks": result["chunks"],           # Can be shown for debugging or transparency
            "evaluation": result["evaluation"]      # Cosine similarity scores (relevance metric)
        })



# used on rapid testing purposes during development
# ---------------------------------------------------------------------
# 🔄 RAGResetView is for reprocessing the entire knowledge base:
#    - Clears old data
#    - Re-ingests the PDF (clean, chunk, embed)
#    - Handles a fresh query
# ---------------------------------------------------------------------

# class RAGResetView(APIView):
#     def post(self, request):
#         # 🔹 Step 1: Extract 'query' and 'book' name from request
#         query = request.data.get("query")
#         book_name = request.data.get("book")

#         if not query or not book_name:
#             # ❗ Return error if any required field is missing
#             return Response(
#                 {"error": "Missing 'query' or 'book' in request."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # 🔹 Step 2: Delete all existing PDF chunks from the DB
#         deleted_count, _ = PDFChunk.objects.all().delete()
#         print(f"[RAGResetView] 🗑️ Deleted {deleted_count} PDFChunk(s)")

#         # 🔹 Step 3: Reprocess the given PDF file (clean → chunk → embed → save)
#         ingest_pdf_data(book_name)

#         # 🔹 Step 4: Handle the query again using the newly ingested data
#         result = handle_query(query)

#         # 🔹 Step 5: Return status, answer, and similarity evaluation
#         return Response({
#             "message": f"Reset done. Processed book: {book_name}",
#             "answer": result["answer"],             # Answer after full reset
#             # "chunks": result["chunks"],           # Can be returned for review
#             "evaluation": result["evaluation"]      # Similarity evaluation scores
#         })