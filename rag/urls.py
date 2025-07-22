from django.urls import path
from .views import PDFUploadView, StaticPDFProcessView

urlpatterns = [
    path("upload-pdf/", PDFUploadView.as_view(), name="upload-pdf"),
    path("static-process/", StaticPDFProcessView.as_view(), name="static-process"),
]
