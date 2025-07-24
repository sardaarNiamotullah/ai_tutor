from django.apps import AppConfig
import threading

class RagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rag'

    def ready(self):
        from .initialize import initialize_embeddings
        from .models import PDFChunk

        def run_on_start():
            from django.db.utils import OperationalError
            try:
                if not PDFChunk.objects.exists():
                    initialize_embeddings()
            except OperationalError:
                print("Database not ready yet...")

        threading.Thread(target=run_on_start).start()    