from django.db import models
from pgvector.django import VectorField

class PDFChunk(models.Model):
    text = models.TextField()
    embedding = VectorField(dimensions=384)  # 384-d for MiniLM model
    language = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)