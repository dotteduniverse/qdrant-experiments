"""
Experiment 10: Snapshots & Backup
- Create a snapshot of a collection
- Delete the collection
- Restore the collection from the snapshot
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client_factory import get_client
from src.synthetic_data import generate_points
from config.settings import DEFAULT_COLLECTION, VECTOR_SIZE


def main():
    print("\n" + "="*50)
    print("💾 EXPERIMENT 10: SNAPSHOTS & BACKUP")
    print("="*50 + "\n")
    
    client = get_client()
    collection_name = f"{DEFAULT_COLLECTION}_10"
    snapshot_collection = f"{collection_name}_restored"
    
    # Setup original collection
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": VECTOR_SIZE, "distance": "Cosine"},
    )
    print("✅ Original collection created.\n")
    
    # Insert 100 points
    print("📥 Inserting 100 points into original collection...")
    ids, vectors, payloads = generate_points(100)
    points = [
        {"id": ids[i], "vector": vectors[i], "payload": payloads[i]}
        for i in range(100)
    ]
    client.upsert(collection_name=collection_name, points=points)
    print(f"✅ {len(points)} points inserted.\n")
    
    # 1. Create a snapshot
    print("📸 Creating snapshot of the collection...")
    snapshot = client.create_snapshot(collection_name=collection_name)
    print(f"✅ Snapshot created: {snapshot.name}")
    print(f"   Snapshot URL: {snapshot.url}\n")
    
    time.sleep(1)
    
    # 2. List snapshots
    print("📋 Listing snapshots for the collection...")
    snapshots = client.list_snapshots(collection_name=collection_name)
    for snap in snapshots:
        print(f"   - {snap.name} (Created: {snap.created_at})")
    
    # 3. Delete the original collection
    print(f"\n🗑️ Deleting original collection: {collection_name}...")
    client.delete_collection(collection_name=collection_name)
    print("✅ Collection deleted.\n")
    
    # 4. Restore from snapshot to a NEW collection
    print(f"♻️ Restoring snapshot to new collection: {snapshot_collection}...")
    try:
        snapshot_path = f"/qdrant/storage/snapshots/{collection_name}/{snapshot.name}"
        client.recover_snapshot(
            collection_name=snapshot_collection,
            location=snapshot_path,
        )
        print(f"✅ Collection restored from snapshot: {snapshot_collection}")
        
        count = client.count(collection_name=snapshot_collection).count
        print(f"📊 Restored collection has {count} points.")
        
        client.delete_collection(collection_name=snapshot_collection)
        print("🧹 Restored collection cleaned up.")
        
    except Exception as e:
        print(f"⚠️ Snapshot restore requires the actual file path in Docker.")
        print(f"   Error: {e}")
        print("   To restore manually, use the Qdrant API or dashboard.")
    
    print("\n🏁 Experiment 10 completed!")


if __name__ == "__main__":
    main()