"""
Experiment 05: Geo Filtering
- Insert points with geographical coordinates
- Query points within a radius and bounding box
"""

import sys
import os
import random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client_factory import get_client
from src.synthetic_data import generate_points
from qdrant_client import models
from config.settings import DEFAULT_COLLECTION, VECTOR_SIZE


def main():
    print("\n" + "="*50)
    print("🌍 EXPERIMENT 05: GEO FILTERING")
    print("="*50 + "\n")
    
    client = get_client()
    collection_name = f"{DEFAULT_COLLECTION}_05"
    
    # Setup collection
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": VECTOR_SIZE, "distance": "Cosine"},
    )
    print("✅ Collection created.\n")
    
    # Insert 200 points with geo coordinates centered around New York
    print("📥 Inserting 200 points with geo coordinates...")
    ids, vectors, payloads = generate_points(200)
    
    # Override geo coordinates to cluster around NYC
    for i in range(200):
        payloads[i]["geo"] = {
            "lat": 40.7128 + random.uniform(-2, 2),
            "lon": -74.0060 + random.uniform(-2, 2),
        }
    
    points = [
        {"id": ids[i], "vector": vectors[i], "payload": payloads[i]}
        for i in range(200)
    ]
    client.upsert(collection_name=collection_name, points=points)
    print("✅ 200 points inserted.\n")
    
    # 1. Radius search (points within 50km of NYC)
    print("🔍 Searching for points within 50km of New York City...")
    radius_response = client.query_points(
        collection_name=collection_name,
        query=vectors[0],
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="geo",
                    geo_radius=models.GeoRadius(
                        center=models.GeoPoint(
                            lat=40.7128,
                            lon=-74.0060,
                        ),
                        radius=50.0,
                    )
                )
            ]
        ),
        limit=10,
    )
    radius_results = radius_response.points
    print(f"   Found {len(radius_results)} points within 50km.")
    for hit in radius_results[:3]:
        geo = hit.payload.get("geo")
        print(f"   ID: {hit.id}, Lat: {geo['lat']:.4f}, Lon: {geo['lon']:.4f}")
    print()
    
    # 2. Bounding box search
    print("🔍 Searching for points within a bounding box around NYC...")
    bbox_response = client.query_points(
        collection_name=collection_name,
        query=vectors[0],
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="geo",
                    geo_bounding_box=models.GeoBoundingBox(
                        top_left=models.GeoPoint(lat=41.0, lon=-75.0),
                        bottom_right=models.GeoPoint(lat=40.0, lon=-73.0),
                    )
                )
            ]
        ),
        limit=10,
    )
    bbox_results = bbox_response.points
    print(f"   Found {len(bbox_results)} points in the bounding box.\n")
    
    # Cleanup
    client.delete_collection(collection_name=collection_name)
    print("🧹 Collection deleted.\n")
    print("🏁 Experiment 05 completed!")


if __name__ == "__main__":
    main()