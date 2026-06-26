"""
Experiment 01: Basic CRUD Operations
- Create a collection
- Upsert points
- Fetch a point by ID
- Delete the collection
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client_factory import get_client
from src.synthetic_data import generate_points
from config.settings import DEFAULT_COLLECTION, VECTOR_SIZE


def main():
    print("\n" + "="*50)
    print("🚀 EXPERIMENT 01: BASIC CRUD OPERATIONS")
    print("="*50 + "\n")
    
    client = get_client()
    collection_name = f"{DEFAULT_COLLECTION}_01"
    
    # 1. Create collection
    print(f"📂 Creating collection: {collection_name}")
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": VECTOR_SIZE, "distance": "Cosine"},
    )
    print("✅ Collection created.\n")
    
    # 2. Upsert points
    print("📥 Upserting 5 points...")
    ids, vectors, payloads = generate_points(5)
    
    points = []
    for idx, vec, payload in zip(ids, vectors, payloads):
        points.append({
            "id": idx,
            "vector": vec,
            "payload": payload,
        })
    
    client.upsert(collection_name=collection_name, points=points)
    print("✅ Points upserted.\n")
    
    # 3. Fetch point by ID (FIX: added with_vectors=True)
    print(f"🔍 Fetching point ID=2...")
    fetched = client.retrieve(
        collection_name=collection_name, 
        ids=[2], 
        with_vectors=True
    )
    if fetched:
        print(f"   ID: {fetched[0].id}")
        print(f"   Payload: {fetched[0].payload}")
        print(f"   Vector (first 5 dims): {fetched[0].vector[:5]}...\n")
    else:
        print("   Point not found.\n")
    
    # 4. Count points
    count = client.count(collection_name=collection_name).count
    print(f"📊 Total points in collection: {count}\n")
    
    # 5. Cleanup (optional - comment out to keep data)
    print("🧹 Cleaning up: Deleting collection...")
    client.delete_collection(collection_name=collection_name)
    print("✅ Collection deleted.\n")
    
    print("🏁 Experiment 01 completed successfully!")


if __name__ == "__main__":
    main()