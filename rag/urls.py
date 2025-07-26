from django.urls import path
from .views import RAGQueryView

# ---------------------------------------------------------------------
# 🔗 URL Configuration for RAG (Retrieval-Augmented Generation) System
#
# This file defines all the REST API endpoints for interacting with
# the RAG pipeline — including sending queries and resetting/reloading data.
# ---------------------------------------------------------------------

urlpatterns = [ 
    # ---------------------------------------------------------------
    # POST /api/rag/query/
    # ---------------------------------------------------------------
    # 🔹 Main endpoint for interacting with the RAG system.
    # 🔹 Accepts a user query (English or Bangla) and returns:
    #     - A generated answer from the LLM
    #     - Cosine similarity evaluation scores for the retrieved chunks
    # 🔹 Uses: `RAGQueryView`
    path("query/", RAGQueryView.as_view(), name="rag-query"),

    # ---------------------------------------------------------------
    # POST /api/rag/reset/  used on rapid testing purposes during development
    # ---------------------------------------------------------------
    # 🔄 Utility endpoint to reinitialize the vector DB:
    #     - Deletes all existing chunks from the database
    #     - Reprocesses the given PDF (clean → chunk → embed)
    #     - Then answers a fresh query using the new data
    # 🔹 Useful during development or for updating the knowledge base
    # 🔹 Uses: `RAGResetView`
    # path("reset/", RAGResetView.as_view(), name="rag-reset"),
]