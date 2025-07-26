from django.db import connection
from ..models import PDFChunk
from ..utils.data_embedder import model  # SentenceTransformer model for encoding text
import numpy as np
from pgvector.django import CosineDistance  # Used for vector-based similarity search


def get_relevant_chunks(query, top_k=3):
    """
    Retrieve the top-k most semantically relevant document chunks for a given query
    using cosine similarity between the query and chunk embeddings stored in the database.

    Args:
        query (str): The user query in English or Bangla.
        top_k (int): Number of top-matching chunks to return.

    Returns:
        List[Dict]: A list of dictionaries, each containing:
            - text: the chunk content
            - embedding: the chunk's vector representation
            - distance: cosine distance from the query (lower is better)
    """

    # ----------------------------------------------------------------
    # 🔹 Step 1: Embed the input query using the same model used for PDF chunks
    # - The query is prefixed with "query: " to provide context
    # - Result is a 384-dimensional vector (for the current model)
    # ----------------------------------------------------------------
    query_embedding = model.encode([f"query: {query}"])[0]

    # ----------------------------------------------------------------
    # 🔹 Step 2: Use PostgreSQL + pgvector to find top-k closest chunks
    # - CosineDistance annotates each PDFChunk with its distance from the query
    # - We order by ascending distance (i.e., most similar first)
    # ----------------------------------------------------------------
    results = (
        PDFChunk.objects
        .annotate(distance=CosineDistance("embedding", query_embedding))
        .order_by("distance")[:top_k]
    )

    # ----------------------------------------------------------------
    # 🔹 Step 3: Build and return the result list with all necessary fields
    # - Each result includes the raw chunk text
    # - The embedding is returned so we can calculate cosine similarity again later
    # - The distance is optional but useful for debugging or UI feedback
    # ----------------------------------------------------------------
    return [
        {
            "text": result.text,
            "embedding": list(result.embedding),  # convert from vector to plain list
            "distance": float(result.distance)
        }
        for result in results
    ]