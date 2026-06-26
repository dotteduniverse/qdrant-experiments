"""
Experiment 03: Batch Upsert and Scroll
- Upsert 1000 vectors in batches of 100
- Use scroll() to paginate through all points
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client_factory import get_client
from src.synthetic_data import generate_points
from tqdm import tqdm
from config.settings import DEFAULT_COLLECTION, VECTOR_SIZE


def main():
    print("\n" + "="*50)
    print("📦 EXPERIMENT 03: BATCH UPSERT & SCROLL")
    print("="*50 + "\n")
    
    client = get_client()
    collection_name = f"{DEFAULT_COLLECTION}_03"
    
    # Setup collection
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": VECTOR_SIZE, "distance": "Cosine"},
    )
    print("✅ Collection created.\n")
    
    # Batch upsert 1000 points
    total_points = 1000
    batch_size = 100
    print(f"📥 Upserting {total_points} points in batches of {batch_size}...")
    
    for batch_start in tqdm(range(0, total_points, batch_size)):
        batch_end = min(batch_start + batch_size, total_points)
        n = batch_end - batch_start
        
        ids, vectors, payloads = generate_points(n)
        points = [
            {"id": batch_start + ids[i], "vector": vectors[i], "payload": payloads[i]}
            for i in range(n)
        ]
        client.upsert(collection_name=collection_name, points=points)
    
    print(f"✅ {total_points} points upserted.\n")
    
    # Scroll through all points
    print("📜 Scrolling through all points (pagination)...")
    all_points = []
    offset = None
    limit = 50
    
    while True:
        result = client.scroll(
            collection_name=collection_name,
            limit=limit,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        points, offset = result
        if not points:
            break
        all_points.extend(points)
        print(f"   Fetched {len(all_points)} points so far...")
    
    print(f"\n✅ Total points retrieved via scroll: {len(all_points)}")
    
    # Cleanup
    client.delete_collection(collection_name=collection_name)
    print("🧹 Collection deleted.\n")
    print("🏁 Experiment 03 completed!")


if __name__ == "__main__":
    main()