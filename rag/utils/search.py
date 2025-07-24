from django.db import connection
from ..models import PDFChunk
from ..utils.embedder import model

def get_relevant_chunks(query, top_k=3):
    query_embedding = model.encode([query])[0].tolist()
    sql = """
        SELECT id, text, language
        FROM rag_pdfchunk
        ORDER BY embedding <-> %s::vector
        LIMIT %s
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, [query_embedding, top_k])
        results = cursor.fetchall()

    chunks = [
        {"id": row[0], "text": row[1], "language": row[2]}
        for row in results
    ]

    print("[Search] 📌 Top chunks fetched for query:")
    for i, c in enumerate(chunks):
        print(f"  {i+1}. {c['text'][:100]}...")

    return chunks
