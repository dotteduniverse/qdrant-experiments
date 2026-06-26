"""
Experiment 06: Recommendation API (v1.18+ using query_points)
- Use positive and negative examples to find similar items
- "More like this, but less like that"
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client_factory import get_client
from src.synthetic_data import generate_points
from config.settings import DEFAULT_COLLECTION, VECTOR_SIZE


def main():
    print("\n" + "="*50)
    print("🎯 EXPERIMENT 06: RECOMMENDATION API")
    print("="*50 + "\n")
    
    client = get_client()
    collection_name = f"{DEFAULT_COLLECTION}_06"
    
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
    
    # 1. Basic recommendation (positive only)
    print("🔍 Recommendation: Using positive example ID=0...")
    response = client.query_points(
        collection_name=collection_name,
        positive=[0],  # Recommend based on this ID
        limit=5,
    )
    results = response.points
    print("Top 5 recommendations (positive only):")
    for hit in results:
        print(f"   ID: {hit.id}, Score: {hit.score:.4f}, Category: {hit.payload.get('category')}")
    print()
    
    # 2. Recommendation with negative example
    print("🔍 Recommendation: Positive ID=1, Negative ID=2...")
    response_neg = client.query_points(
        collection_name=collection_name,
        positive=[1],
        negative=[2],
        limit=5,
    )
    results_neg = response_neg.points
    print("Top 5 recommendations (positive=1, negative=2):")
    for hit in results_neg:
        print(f"   ID: {hit.id}, Score: {hit.score:.4f}, Category: {hit.payload.get('category')}")
    print()
    
    # 3. Multiple positives and negatives
    print("🔍 Recommendation: Positive=[5, 6], Negative=[7, 8]...")
    response_multi = client.query_points(
        collection_name=collection_name,
        positive=[5, 6],
        negative=[7, 8],
        limit=5,
    )
    results_multi = response_multi.points
    print("Top 5 recommendations (multi-pos/neg):")
    for hit in results_multi:
        print(f"   ID: {hit.id}, Score: {hit.score:.4f}, Category: {hit.payload.get('category')}")
    print()
    
    # Cleanup
    client.delete_collection(collection_name=collection_name)
    print("🧹 Collection deleted.\n")
    print("🏁 Experiment 06 completed!")


if __name__ == "__main__":
    main()