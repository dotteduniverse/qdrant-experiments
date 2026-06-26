"""
Experiment 08: RAG with Text Embeddings
- Load a small text corpus
- Generate embeddings using Sentence-Transformers
- Build a mini RAG pipeline: Query → Retrieve → Context → Response
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client_factory import get_client
from src.embedding_utils import embed_text, get_vector_size
from qdrant_client import models
from config.settings import DEFAULT_COLLECTION


# Sample text corpus
CORPUS = [
    "The elephant is the largest living land animal. They are known for their large ears and trunks.",
    "Penguins are flightless birds that live mostly in the Southern Hemisphere. They are excellent swimmers.",
    "The Great Wall of China is one of the most famous landmarks in the world, stretching over 13,000 miles.",
    "Coffee is a brewed drink prepared from roasted coffee beans. It is one of the most popular drinks globally.",
    "The Amazon Rainforest is the largest tropical rainforest in the world, covering much of South America.",
    "Albert Einstein developed the theory of relativity and is considered one of the greatest physicists.",
    "Mars is the fourth planet from the Sun and is often called the 'Red Planet' due to its iron oxide-rich soil.",
    "Shakespeare wrote 37 plays and 154 sonnets, including Hamlet, Romeo and Juliet, and Macbeth.",
    "The iPhone was first released by Apple in 2007, revolutionizing the smartphone industry.",
    "Mount Everest is the highest mountain in the world, standing at 29,029 feet above sea level.",
    "Photosynthesis is the process by which green plants use sunlight to synthesize nutrients from carbon dioxide and water.",
    "The internet is a global network of interconnected computers that communicates using standardized protocols.",
    "Beethoven was a German composer and pianist who was a crucial figure in the transition between Classical and Romantic eras.",
    "The Pacific Ocean is the largest and deepest ocean on Earth, covering more than 63 million square miles.",
    "Artificial intelligence (AI) is the simulation of human intelligence processes by computer systems.",
]


def main():
    print("\n" + "="*50)
    print("🧠 EXPERIMENT 08: RAG TEXT EMBEDDINGS")
    print("="*50 + "\n")
    
    client = get_client()
    collection_name = f"{DEFAULT_COLLECTION}_08"
    
    # Setup collection
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)
    
    vector_size = get_vector_size()
    client.create_collection(
        collection_name=collection_name,
        vectors_config={"size": vector_size, "distance": "Cosine"},
    )
    print("✅ Collection created.\n")
    
    # 1. Chunk and embed the corpus
    print(f"📚 Embedding {len(CORPUS)} text chunks...")
    embeddings = embed_text(CORPUS)
    print(f"✅ Embeddings generated (dimension: {len(embeddings[0])})\n")
    
    # 2. Upsert to Qdrant
    print("📥 Upserting chunks to Qdrant...")
    points = []
    for i, (text, vec) in enumerate(zip(CORPUS, embeddings)):
        points.append({
            "id": i,
            "vector": vec,
            "payload": {"text": text, "chunk_id": i},
        })
    client.upsert(collection_name=collection_name, points=points)
    print(f"✅ {len(points)} chunks upserted.\n")
    
    # 3. RAG Query Pipeline
    query = "What is the largest ocean on Earth?"
    print(f"❓ User Query: '{query}'")
    
    query_embedding = embed_text(query)[0]
    
    # Retrieve top-k relevant chunks (UPDATED to query_points)
    response = client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=3,
    )
    results = response.points
    
    context = "\n".join([hit.payload["text"] for hit in results])
    
    print("\n📄 Retrieved Context:")
    print("-" * 40)
    print(context)
    print("-" * 40)
    
    print("\n🤖 Mock LLM Response:")
    print("-" * 40)
    print(f"Based on the retrieved documents: '{query}'")
    print("The Pacific Ocean is the largest and deepest ocean on Earth.")
    print("-" * 40)
    print("\n💡 In a real RAG system, this context would be sent to an LLM like GPT-4!")
    
    # Cleanup
    client.delete_collection(collection_name=collection_name)
    print("\n🧹 Collection deleted.\n")
    print("🏁 Experiment 08 completed!")


if __name__ == "__main__":
    main()