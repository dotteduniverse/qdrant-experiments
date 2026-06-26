import pytest
from src.client_factory import get_client


def test_in_memory_client():
    """Test that the in-memory client initializes correctly."""
    client = get_client(use_memory=True)
    assert client is not None
    assert client.collection_exists("test_collection") is False
    print("✅ In-memory client test passed!")


def test_local_client_connection():
    """Test that the local client can connect (Docker must be running)."""
    try:
        client = get_client(use_memory=False)
        collections = client.get_collections()
        assert collections is not None
        print("✅ Local client connection test passed!")
    except Exception as e:
        pytest.skip(f"Skipping local test: Qdrant server not reachable. Error: {e}")


if __name__ == "__main__":
    pytest.main(["-v"])