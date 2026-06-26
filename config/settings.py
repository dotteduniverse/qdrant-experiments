import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Qdrant Connection
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_URL = os.getenv("QDRANT_URL", f"http://{QDRANT_HOST}:{QDRANT_PORT}")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

# Default Collection
DEFAULT_COLLECTION = os.getenv("DEFAULT_COLLECTION", "experiment_collection")

# Vector Configuration
VECTOR_SIZE = 384  # all-MiniLM-L6-v2 embedding size

# Embedding Model
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Distance Metric
DISTANCE_METRIC = "Cosine"  # Options: Cosine, Dot, Euclid