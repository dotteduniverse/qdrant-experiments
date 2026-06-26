from qdrant_client import QdrantClient
from config.settings import QDRANT_URL, QDRANT_API_KEY


def get_client(use_memory: bool = False) -> QdrantClient:
    """
    Factory function to get a Qdrant client.
    
    Args:
        use_memory: If True, uses in-memory mode (data lost on restart).
                   If False, connects to the configured URL (local or cloud).
    
    Returns:
        QdrantClient instance
    """
    if use_memory:
        print("🔁 Using in-memory Qdrant client (data will not persist).")
        return QdrantClient(":memory:")
    
    print(f"🔌 Connecting to Qdrant at: {QDRANT_URL}")
    
    if QDRANT_API_KEY:
        return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    else:
        return QdrantClient(url=QDRANT_URL)