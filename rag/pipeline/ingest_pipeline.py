import os
from django.conf import settings
from ..utils.pdf_reader import read_and_clean_pdf
from ..utils.data_embedder import chunk_and_embed
from ..models import PDFChunk

def ingest_pdf_data(file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if not os.path.exists(file_path):
        print(f"[Ingest] ❌ File not found: {file_path}")
        return

    if PDFChunk.objects.filter(source_file=file_name).exists():
        print(f"[Ingest] ⚠️ Embeddings already exist for {file_name}")
        return

    cleaned_text, language = read_and_clean_pdf(file_path)
    chunks, embeddings = chunk_and_embed(cleaned_text, language)

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        
        PDFChunk.objects.create(
            text=chunk,
            embedding=embedding,
            language=language,
            source_file=file_name
        )

    print(f"[Ingest] ✅ {len(chunks)} chunks saved to DB.")
