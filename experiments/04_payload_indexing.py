"""
Experiment 04: Payload Indexing
- Create an index on the 'timestamp' field
- Compare search speed (conceptually) with and without index
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client_factory import get_client
from src.synthetic_data import generate_points
from qdrant_client import models
from config.settings import DEFAULT_COLLECTION, VECTOR_SIZE
import time


def main():
    print("\n" + "="*50)
    print("⚡ EXPERIMENT 04: PAYLOAD INDEXING")
    print("="*50 + "\n")
    
    client = get_client()
    collection_name = f"{DEFAULT_COLLECTION}_04"
    
    # Setup collection
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": VECTOR_SIZE, "distance": "Cosine"},
    )
    print("✅ Collection created.\n")
    
    # Insert 500 points
    print("📥 Inserting 500 points...")
    ids, vectors, payloads = generate_points(500)
    points = [
        {"id": ids[i], "vector": vectors[i], "payload": payloads[i]}
        for i in range(500)
    ]
    client.upsert(collection_name=collection_name, points=points)
    print("✅ 500 points inserted.\n")
    
    # 1. Search WITHOUT index
    print("🔍 Running filtered search WITHOUT index...")
    start = time.time()
    response_no_index = client.query_points(
        collection_name=collection_name,
        query=vectors[0],
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="timestamp",
                    range=models.Range(gte=1640995200)
                )
            ]
        ),
        limit=5,
    )
    results_no_index = response_no_index.points
    time_no_index = time.time() - start
    print(f"   Query took: {time_no_index:.4f} seconds\n")
    
    # 2. Create payload index on timestamp
    print("📇 Creating payload index on 'timestamp' field...")
    client.create_payload_index(
        collection_name=collection_name,
        field_name="timestamp",
        field_type=models.FieldType.INTEGER,
    )
    print("✅ Index created.\n")
    
    time.sleep(0.5)
    
    # 3. Search WITH index
    print("🔍 Running filtered search WITH index...")
    start = time.time()
    response_with_index = client.query_points(
        collection_name=collection_name,
        query=vectors[0],
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="timestamp",
                    range=models.Range(gte=1640995200)
                )
            ]
        ),
        limit=5,
    )
    results_with_index = response_with_index.points
    time_with_index = time.time() - start
    print(f"   Query took: {time_with_index:.4f} seconds\n")
    
    print("📊 Note: Indexing significantly improves performance on large datasets!")
    print(f"   Speed improvement factor (approx): {time_no_index / time_with_index:.2f}x\n")
    
    # Cleanup
    client.delete_collection(collection_name=collection_name)
    print("🧹 Collection deleted.\n")
    print("🏁 Experiment 04 completed!")


if __name__ == "__main__":
    main()