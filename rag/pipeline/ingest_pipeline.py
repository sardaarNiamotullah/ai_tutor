import os
from django.conf import settings
from ..utils.pdf_reader import read_and_clean_pdf      # Responsible for extracting and cleaning raw text from PDF
from ..utils.data_embedder import chunk_and_embed      # Handles splitting + embedding the cleaned text
from ..models import PDFChunk                          # Model that stores chunks and their embeddings


def ingest_pdf_data(file_name):
    """
    🚀 Ingests and vectorizes a PDF document for retrieval in RAG pipeline.

    This function:
    1. Loads a PDF file from disk.
    2. Cleans and detects the language of the content.
    3. Chunks the text into manageable pieces.
    4. Embeds each chunk using SentenceTransformer.
    5. Stores the chunks and vectors in the PostgreSQL vector DB (via pgvector).

    Args:
        file_name (str): Name of the PDF file in MEDIA_ROOT to be processed.
    """

    # ----------------------------------------------------------------
    # 📍 Step 1: Build full file path from MEDIA_ROOT
    # ----------------------------------------------------------------
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    # ----------------------------------------------------------------
    # ❌ Step 2: Guard clause — check if file exists
    # ----------------------------------------------------------------
    if not os.path.exists(file_path):
        print(f"[Ingest] ❌ File not found: {file_path}")
        return

    # ----------------------------------------------------------------
    # ⚠️ Step 3: Skip processing if this file has already been embedded
    # - Prevents duplicate ingestion
    # ----------------------------------------------------------------
    if PDFChunk.objects.filter(source_file=file_name).exists():
        print(f"[Ingest] ⚠️ Embeddings already exist for {file_name}")
        return

    # ----------------------------------------------------------------
    # 🧼 Step 4: Extract raw text and clean it (remove noise, normalize)
    # - Also returns detected language (e.g., 'bn' for Bangla)
    # ----------------------------------------------------------------
    cleaned_text, language = read_and_clean_pdf(file_path)

    # ----------------------------------------------------------------
    # ✂️🧠 Step 5: Split text into chunks and embed them into vectors
    # - chunk_and_embed() returns:
    #     - chunks: list of small text units (approx. ~200-1000 tokens)
    #     - embeddings: their corresponding dense vector representations
    # ----------------------------------------------------------------
    chunks, embeddings = chunk_and_embed(cleaned_text, language)

    # ----------------------------------------------------------------
    # 💾 Step 6: Save each chunk + embedding into the database
    # - Uses the PDFChunk model with pgvector's VectorField
    # ----------------------------------------------------------------
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        PDFChunk.objects.create(
            text=chunk,
            embedding=embedding,
            language=language,
            source_file=file_name
        )

    # ✅ Final log message
    print(f"[Ingest] ✅ {len(chunks)} chunks saved to DB.")
