from django.db import connection
from ..models import PDFChunk
from ..embeddings.embedder import model

def semantic_search(query, top_k=5):
    # 1. Generate embedding
    query_embedding = model.encode([query])[0].tolist()

    # 2. Prepare raw SQL query with cosine distance
    sql = """
        SELECT id, text, language
        FROM rag_pdfchunk
        ORDER BY embedding <-> %s::vector
        LIMIT %s
    """

    # 3. Execute SQL with vector embedding
    with connection.cursor() as cursor:
        cursor.execute(sql, [query_embedding, top_k])
        results = cursor.fetchall()

    # 4. Return as a list of dicts
    return [
        {"id": row[0], "text": row[1], "language": row[2]}
        for row in results
    ]
