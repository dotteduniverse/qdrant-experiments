import random
import numpy as np
from typing import List, Dict, Any, Tuple
from config.settings import VECTOR_SIZE


def generate_random_vectors(n: int, dim: int = None) -> List[List[float]]:
    """
    Generate n random vectors of specified dimension.
    
    Args:
        n: Number of vectors.
        dim: Dimensionality of each vector. Defaults to VECTOR_SIZE.
    
    Returns:
        List of vectors.
    """
    if dim is None:
        dim = VECTOR_SIZE
    
    # Generate random vectors and normalize them for better similarity behavior
    vectors = np.random.randn(n, dim).astype(np.float32)
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    vectors = vectors / norms  # Normalize to unit length
    
    return vectors.tolist()


def generate_fake_payloads(n: int) -> List[Dict[str, Any]]:
    """
    Generate fake metadata payloads for n points.
    
    Args:
        n: Number of payloads to generate.
    
    Returns:
        List of payload dictionaries.
    """
    categories = ["electronics", "clothing", "books", "food", "toys", "furniture"]
    colors = ["red", "blue", "green", "black", "white", "yellow"]
    cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Berlin"]
    
    payloads = []
    for i in range(n):
        payload = {
            "id_index": i,
            "category": random.choice(categories),
            "color": random.choice(colors),
            "city": random.choice(cities),
            "price": round(random.uniform(5.99, 299.99), 2),
            "in_stock": random.choice([True, False]),
            "rating": round(random.uniform(1.0, 5.0), 1),
            "timestamp": random.randint(1609459200, 1735689600),  # 2021-2025 timestamps
            "name": f"Product_{i}_{random.choice(['Alpha', 'Beta', 'Gamma'])}",
        }
        # Add geographical coordinates (latitude, longitude)
        payload["geo"] = {
            "lat": round(random.uniform(-90, 90), 6),
            "lon": round(random.uniform(-180, 180), 6),
        }
        payloads.append(payload)
    
    return payloads


def generate_points(n: int, dim: int = None) -> Tuple[List[int], List[List[float]], List[Dict[str, Any]]]:
    """
    Generate n complete points (IDs, vectors, and payloads).
    
    Args:
        n: Number of points.
        dim: Vector dimension.
    
    Returns:
        Tuple of (ids, vectors, payloads)
    """
    ids = list(range(n))
    vectors = generate_random_vectors(n, dim)
    payloads = generate_fake_payloads(n)
    return ids, vectors, payloads