#!/usr/bin/env python
"""
Cleanup Script: Delete all collections in Qdrant.
Use this to reset your environment between experiment runs.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.client_factory import get_client


def main():
    print("\n" + "="*50)
    print("🧹 CLEANUP: Deleting all collections")
    print("="*50 + "\n")
    
    client = get_client()
    
    try:
        collections = client.get_collections().collections
        if not collections:
            print("✅ No collections found. Nothing to delete.")
            return
        
        print(f"📋 Found {len(collections)} collection(s):")
        for coll in collections:
            print(f"   - {coll.name}")
        
        confirm = input("\n⚠️ Delete all collections? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ Aborted.")
            return
        
        for coll in collections:
            client.delete_collection(coll.name)
            print(f"   ✅ Deleted: {coll.name}")
        
        print("\n✅ All collections deleted successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure Qdrant is running and reachable.")


if __name__ == "__main__":
    main()