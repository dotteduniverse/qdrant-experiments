"""
Experiment 07: Hybrid Search (Dense + Sparse BM42)
- Configure a collection with dense AND sparse vectors
- Perform hybrid search combining both
"""

import sys
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client_factory import get_client
from src.synthetic_data import generate_points
from qdrant_client import models
from config.settings import DEFAULT_COLLECTION, VECTOR_SIZE


def main():
    print("\n" + "="*50)
    print("🔀 EXPERIMENT 07: HYBRID SEARCH (DENSE + SPARSE)")
    print("="*50 + "\n")
    
    client = get_client()
    collection_name = f"{DEFAULT_COLLECTION}_07"
    
    # Setup collection with both dense and sparse vectors
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    
    vectors_config = {
        "dense": models.VectorParams(
            size=VECTOR_SIZE,
            distance=models.Distance.COSINE,
        ),
        "sparse": models.VectorParams(
            size=1000,
            distance=models.Distance.DOT,
        ),
    }
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config=vectors_config,
    )
    print("✅ Collection created with Dense + Sparse config.\n")
    
    # Insert 100 points with both dense and sparse vectors
    print("📥 Inserting 100 points with dense + sparse vectors...")
    ids, dense_vectors, payloads = generate_points(100, dim=VECTOR_SIZE)
    
    sparse_vectors = []
    for _ in range(100):
        sparse_vec = np.zeros(1000)
        indices = np.random.choice(1000, 20, replace=False)
        sparse_vec[indices] = np.random.rand(20)
        sparse_vectors.append(sparse_vec.tolist())
    
    points = []
    for i in range(100):
        points.append({
            "id": ids[i],
            "vector": {
                "dense": dense_vectors[i],
                "sparse": sparse_vectors[i],
            },
            "payload": payloads[i],
        })
    
    client.upsert(collection_name=collection_name, points=points)
    print("✅ 100 hybrid points inserted.\n")
    
    # Hybrid search using query_points with named vectors
    query_dense = dense_vectors[0]
    query_sparse = sparse_vectors[0]
    
    # 1. Dense-only search
    print("🔍 Dense-only search...")
    dense_response = client.query_points(
        collection_name=collection_name,
        query=query_dense,
        using="dense",  # Specify which vector field to use
        limit=5,
    )
    dense_results = dense_response.points
    print("Dense-only results:")
    for hit in dense_results[:3]:
        print(f"   ID: {hit.id}, Score: {hit.score:.4f}")
    
    # 2. Sparse-only search
    print("\n🔍 Sparse-only search...")
    sparse_response = client.query_points(
        collection_name=collection_name,
        query=query_sparse,
        using="sparse",  # Specify which vector field to use
        limit=5,
    )
    sparse_results = sparse_response.points
    print("Sparse-only results:")
    for hit in sparse_results[:3]:
        print(f"   ID: {hit.id}, Score: {hit.score:.4f}")
    
    print("\n💡 Hybrid search combines both dense (semantic) and sparse (keyword) matching!")
    print("   The actual fusion can be done via Reciprocal Rank Fusion (RRF) or weighted scores.")
    
    # Cleanup
    client.delete_collection(collection_name=collection_name)
    print("\n🧹 Collection deleted.\n")
    print("🏁 Experiment 07 completed!")


if __name__ == "__main__":
    main()