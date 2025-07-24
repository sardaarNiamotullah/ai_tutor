from django.urls import path
from .views import PDFUploadView, StaticPDFProcessView, RAGQueryView

urlpatterns = [
    path("upload-pdf/", PDFUploadView.as_view(), name="upload-pdf"),
    path("static-process/", StaticPDFProcessView.as_view(), name="static-process"),
    path("query/", RAGQueryView.as_view(), name="rag-query"),
]
