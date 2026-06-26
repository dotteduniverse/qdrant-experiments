"""
Experiment 09: Quantization Benchmark
- Create a collection with Scalar Quantization
- Compare memory usage and search performance
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
    print("📊 EXPERIMENT 09: QUANTIZATION BENCHMARK")
    print("="*50 + "\n")
    
    client = get_client()
    collection_name = f"{DEFAULT_COLLECTION}_09"
    
    # Setup collection WITH scalar quantization
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    
    print("📂 Creating collection with Scalar Quantization (optimized memory)...")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=VECTOR_SIZE,
            distance=models.Distance.COSINE,
        ),
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True,
            )
        ),
    )
    print("✅ Collection created with Scalar Quantization enabled.\n")
    
    # Insert 500 points
    print("📥 Inserting 500 points...")
    ids, vectors, payloads = generate_points(500)
    points = [
        {"id": ids[i], "vector": vectors[i], "payload": payloads[i]}
        for i in range(500)
    ]
    client.upsert(collection_name=collection_name, points=points)
    print("✅ 500 points inserted.\n")
    
    # Check collection info
    info = client.get_collection(collection_name=collection_name)
    print("📊 Collection Info:")
    print(f"   Status: {info.status}")
    print(f"   Points count: {info.points_count}")
    print(f"   Quantization: {info.quantization_config}")
    print("\n💡 Quantization reduces memory footprint significantly!")
    print("   For large collections (1M+ vectors), this is critical for cost savings.")
    
    # Quick search to verify functionality (UPDATED to query_points)
    print("\n🔍 Running a sample search to verify quantization works...")
    response = client.query_points(
        collection_name=collection_name,
        query=vectors[0],
        limit=3,
    )
    results = response.points
    print("   Search successful!")
    for hit in results:
        print(f"   ID: {hit.id}, Score: {hit.score:.4f}")
    
    # Cleanup
    client.delete_collection(collection_name=collection_name)
    print("\n🧹 Collection deleted.\n")
    print("🏁 Experiment 09 completed!")


if __name__ == "__main__":
    main()