import pytest
from src.client_factory import get_client
from src.synthetic_data import generate_points
from config.settings import VECTOR_SIZE


def test_crud_flow():
    """Test a basic CRUD flow with in-memory client."""
    client = get_client(use_memory=True)
    collection_name = "test_flow"
    
    # Create
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": VECTOR_SIZE, "distance": "Cosine"},
    )
    assert client.collection_exists(collection_name)
    
    # Upsert
    ids, vectors, payloads = generate_points(10)
    points = [
        {"id": ids[i], "vector": vectors[i], "payload": payloads[i]}
        for i in range(10)
    ]
    client.upsert(collection_name=collection_name, points=points)
    
    # Count
    count = client.count(collection_name=collection_name).count
    assert count == 10
    
    # Search
    results = client.search(
        collection_name=collection_name,
        query_vector=vectors[0],
        limit=3,
    )
    assert len(results) == 3
    
    # Cleanup
    client.delete_collection(collection_name=collection_name)
    assert not client.collection_exists(collection_name)
    
    print("✅ Basic flow test passed!")


if __name__ == "__main__":
    pytest.main(["-v"])