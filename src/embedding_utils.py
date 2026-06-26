from typing import List, Union
from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL, VECTOR_SIZE

_model = None


def get_embedder(model_name: str = None) -> SentenceTransformer:
    """
    Lazy-loads the SentenceTransformer model.
    
    Args:
        model_name: Optional override for the model name.
    
    Returns:
        SentenceTransformer instance
    """
    global _model
    if _model is None:
        name = model_name or EMBEDDING_MODEL
        print(f"📦 Loading embedding model: {name}...")
        _model = SentenceTransformer(name)
        print("✅ Embedding model loaded.")
    return _model


def embed_text(texts: Union[str, List[str]]) -> List[List[float]]:
    """
    Embed a single string or a list of strings.
    
    Args:
        texts: String or list of strings to embed.
    
    Returns:
        List of embedding vectors (list of floats).
    """
    if isinstance(texts, str):
        texts = [texts]
    
    model = get_embedder()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()


def get_vector_size() -> int:
    """Returns the configured vector size."""
    return VECTOR_SIZE