from django.apps import AppConfig
from django.db.utils import OperationalError
import threading


class RagConfig(AppConfig):
    """
    Configuration class for the 'rag' Django application.

    This class allows for app-specific initialization logic to run
    when the Django app registry is fully populated and ready.
    """

    # Use BigAutoField as the default primary key type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'

    # The name of this app (must match the folder name)
    name = 'rag'

    def ready(self):
        """
        Hook method called by Django once the app registry is fully loaded.

        This is the recommended place to perform app initialization tasks,
        such as loading initial data or starting background threads.

        Here, we trigger ingestion of a PDF file into the vector database
        upon app startup, but do it asynchronously to avoid blocking the main thread.
        """

        # Import the ingestion function here to avoid potential import side-effects
        from .pipeline.ingest_pipeline import ingest_pdf_data

        def run_on_start():
            """
            Function to run in a background thread that attempts
            to ingest the PDF data.

            If the database isn't ready yet (e.g., during migrations or initial startup),
            an OperationalError may be raised. We catch and log this gracefully.
            """
            try:
                ingest_pdf_data("HSC26-Bangla1st-Paper.pdf")
            except OperationalError:
                print("[AppConfig] ⚠️ Database not ready yet...")

        # Launch ingestion in a separate thread to avoid blocking Django's startup
        threading.Thread(target=run_on_start).start()
