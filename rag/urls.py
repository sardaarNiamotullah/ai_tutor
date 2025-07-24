from django.urls import path
from .views import RAGQueryView, RAGResetView

urlpatterns = [ 
    path("query/", RAGQueryView.as_view(), name="rag-query"),
    path("reset/", RAGResetView.as_view(), name="rag-reset"),
]
