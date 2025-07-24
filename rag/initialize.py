import os
from django.conf import settings
from .services.pdf_processor import process_pdf
from .embeddings.embedder import generate_embeddings
from .models import PDFChunk

def initialize_embeddings():
    file_name = "HSC26-Bangla1st-Paper.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if not os.path.exists(file_path):
        print(f"[Startup] ❌ File not found: {file_path}")
        return
    
    if PDFChunk.objects.filter(source_file=file_name).exists():
        print(f"[Startup] ⚠️ Embeddings for {file_name} already exist.")
        return    

    print(f"[Startup] 📄 Processing {file_name}...")
    chunks, language = process_pdf(file_path)

    if not chunks:
        print("[Startup] ❌ No chunks generated.")
        return

    for chunk, embedding in zip(chunks, generate_embeddings(chunks)):
        PDFChunk.objects.create(
            text=chunk,
            embedding=embedding,
            language=language
        )
    
    print(f"[Startup] ✅ {len(chunks)} chunks saved to DB.")
