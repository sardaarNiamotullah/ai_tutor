from django.apps import AppConfig
from django.db.utils import OperationalError
import threading


class RagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rag'

    def ready(self):
        from .pipeline.ingest_pipeline import ingest_pdf_data
        def run_on_start():
            try:
                ingest_pdf_data("banglaboi.pdf")
            except OperationalError:
                print("[AppConfig] ⚠️ Database not ready yet...")

        threading.Thread(target=run_on_start).start()