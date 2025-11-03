#!/usr/bin/env python3
"""
Quick test to verify NVIDIA API works with the required hackathon model.
Run this before deploying to AWS to avoid wasting credits.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

def test_nvidia_connection():
    """Test basic connection to NVIDIA API."""
    print("🔌 Testing NVIDIA API connection...")
    
    api_key = os.getenv('NVIDIA_API_KEY')
    if not api_key or api_key == 'your-nvidia-api-key-here':
        print("❌ NVIDIA_API_KEY not set in backend/.env")
        print("   Get your key from: https://build.nvidia.com")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    return True

def test_llm_model():
    """Test the required LLM model."""
    print("\n🤖 Testing LLM model (llama-3.1-nemotron-nano-8b-instruct)...")
    
    try:
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv('NVIDIA_API_KEY')
        )
        
        response = client.chat.completions.create(
            model="meta/llama-3.1-nemotron-nano-8b-instruct",
            messages=[
                {"role": "user", "content": "Say 'Hello from NVIDIA NIM!' in one sentence."}
            ],
            max_tokens=50
        )
        
        reply = response.choices[0].message.content
        print(f"✅ LLM Response: {reply}")
        print(f"   Model: {response.model}")
        print(f"   Tokens: {response.usage.total_tokens if hasattr(response, 'usage') else 'N/A'}")
        return True
        
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        if "404" in str(e):
            print("   Model not found. Check model name is correct.")
        elif "401" in str(e):
            print("   Authentication failed. Check your API key.")
        return False

def test_embedding_model():
    """Test the embedding model."""
    print("\n🔍 Testing Embedding model (nvidia/nv-embedqa-e5-v5)...")
    
    try:
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv('NVIDIA_API_KEY')
        )
        
        response = client.embeddings.create(
            model="nvidia/nv-embedqa-e5-v5",
            input="Test embedding for BMX coaching"
        )
        
        embedding = response.data[0].embedding
        print(f"✅ Embedding generated: {len(embedding)} dimensions")
        print(f"   First 5 values: {embedding[:5]}")
        return True
        
    except Exception as e:
        print(f"❌ Embedding test failed: {e}")
        if "404" in str(e):
            print("   Model not found. Check model name is correct.")
        elif "401" in str(e):
            print("   Authentication failed. Check your API key.")
        return False

def test_rag_query():
    """Test a complete RAG query."""
    print("\n💬 Testing complete RAG query...")
    
    try:
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv('NVIDIA_API_KEY')
        )
        
        # Simulate a RAG query with context
        context = """
        BMX bikes for beginners should have:
        - Strong chromoly frame
        - 20-inch wheels
        - U-brakes or no brakes for park riding
        - Sealed bearings for durability
        """
        
        response = client.chat.completions.create(
            model="meta/llama-3.1-nemotron-nano-8b-instruct",
            messages=[
                {"role": "system", "content": "You are an expert BMX coach. Use the provided context to answer questions."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: What should I look for in a beginner BMX bike?"}
            ],
            max_tokens=200
        )
        
        reply = response.choices[0].message.content
        print(f"✅ RAG Response: {reply[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ RAG test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 NVIDIA API Test Suite")
    print("=" * 60)
    
    tests = [
        ("API Connection", test_nvidia_connection),
        ("LLM Model", test_llm_model),
        ("Embedding Model", test_embedding_model),
        ("RAG Query", test_rag_query),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            results.append(test_func())
        except Exception as e:
            print(f"❌ {name} failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 Test Results")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for (name, _), result in zip(tests, results):
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All NVIDIA API tests passed!")
        print("✅ Ready to deploy to AWS")
        return 0
    else:
        print("\n⚠️  Some tests failed. Fix issues before deploying.")
        print("\nCommon fixes:")
        print("  - Set NVIDIA_API_KEY in backend/.env")
        print("  - Get API key from: https://build.nvidia.com")
        print("  - Check model names are correct")
        print("  - Verify you have API credits")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
