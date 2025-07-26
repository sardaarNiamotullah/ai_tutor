from django.db import models
from pgvector.django import VectorField


# Define a model to represent chunks of PDF data
class PDFChunk(models.Model):
    text = models.TextField()  # The text content of the PDF chunk
    embedding = VectorField(dimensions=384)  # Vector representation of the text
    language = models.CharField(
        max_length=10
    )  # Language of the text (e.g., 'en', 'bn')
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the chunk was created
    source_file = models.CharField(
        max_length=255, default="banglaboi.pdf"
    )  # Source file name
