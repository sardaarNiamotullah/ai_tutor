from django.apps import AppConfig
from django.db.utils import OperationalError
import threading
import os


class RagConfig(AppConfig):
    # Use BigAutoField as the default primary key type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The name of this Django app (must match the folder name)
    name = 'rag'

    def ready(self):
        """
        This method runs when the Django app registry is fully loaded.

        We use it to perform initialization logic like:
        - Deleting existing vector DB entries
        - Re-ingesting the PDF file into the database

        To avoid running multiple times due to Django’s auto-reloader,
        we check the RUN_MAIN flag before continuing.
        """
        if os.environ.get('RUN_MAIN') != 'true':
            return  # Skip during the first phase of auto-reload

        # Import dependencies here to avoid issues during startup
        from .pipeline.ingest_pipeline import ingest_pdf_data
        from .models import PDFChunk

        def run_on_start():
            """
            Runs in a separate thread to avoid blocking Django startup.
            Deletes all existing PDF chunks and reprocesses the target PDF.
            """
            try:
                # 🔥 Step 1: Delete old vector data
                deleted_count, _ = PDFChunk.objects.all().delete()
                print(f"[AppConfig] 🗑️ Deleted {deleted_count} PDFChunk(s) at startup.")

                # 📘 Step 2: Re-ingest fresh data from the specified PDF
                ingest_pdf_data("HSC26-Bangla1st-Paper.pdf") # ingest_pdf_data("englishboi.pdf") use this for english book
                
            except OperationalError:
                # This can happen if DB is not ready yet (e.g., during migrations)
                print("[AppConfig] ⚠️ Database not ready yet...")

        # Run the startup logic in a background thread
        threading.Thread(target=run_on_start).start()
