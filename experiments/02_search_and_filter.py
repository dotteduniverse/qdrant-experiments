"""
Experiment 02: Search and Filter
- Insert 100 random points
- Perform a similarity search
- Perform a filtered search (must filter)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client_factory import get_client
from src.synthetic_data import generate_points
from qdrant_client import models
from config.settings import DEFAULT_COLLECTION, VECTOR_SIZE


def main():
    print("\n" + "="*50)
    print("🔍 EXPERIMENT 02: SEARCH AND FILTER")
    print("="*50 + "\n")
    
    client = get_client()
    collection_name = f"{DEFAULT_COLLECTION}_02"
    
    # Setup collection
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": VECTOR_SIZE, "distance": "Cosine"},
    )
    print("✅ Collection created.\n")
    
    # Insert 100 points
    print("📥 Inserting 100 points...")
    ids, vectors, payloads = generate_points(100)
    points = [
        {"id": ids[i], "vector": vectors[i], "payload": payloads[i]}
        for i in range(100)
    ]
    client.upsert(collection_name=collection_name, points=points)
    print("✅ 100 points inserted.\n")
    
    # 1. Basic search (UPDATED to query_points)
    query_vector = vectors[0]
    print(f"🔎 Searching for vectors similar to ID=0...")
    response = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=5,
    )
    results = response.points
    
    print("Top 5 results (basic search):")
    for hit in results:
        print(f"   ID: {hit.id}, Score: {hit.score:.4f}, Category: {hit.payload.get('category')}")
    print()
    
    # 2. Filtered search (only "electronics")
    print(f"🔎 Searching with filter: category = 'electronics'...")
    filtered_response = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        query_filter=models.Filter(
            must=[models.FieldCondition(
                key="category",
                match=models.MatchValue(value="electronics")
            )]
        ),
        limit=3,
    )
    filtered_results = filtered_response.points
    
    print("Top 3 results (filtered by 'electronics'):")
    for hit in filtered_results:
        print(f"   ID: {hit.id}, Score: {hit.score:.4f}, Category: {hit.payload.get('category')}")
    print()
    
    # 3. Cleanup
    client.delete_collection(collection_name=collection_name)
    print("🧹 Collection deleted.\n")
    print("🏁 Experiment 02 completed!")


if __name__ == "__main__":
    main()