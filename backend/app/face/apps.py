from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class PineconeAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "face"  # Replace with your app's name

    def ready(self):
        """Perform app-specific initialization."""
        from .pinecone_client import PineconeClient

        try:
            # Initialize Pinecone client
            PineconeClient()
            logger.info("Pinecone client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone client: {e}")
