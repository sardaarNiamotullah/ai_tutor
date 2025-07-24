from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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