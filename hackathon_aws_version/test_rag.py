#!/usr/bin/env python3
"""
Test script for the NVIDIA RAG Engine
Run this to verify the system is working correctly
"""

import os
import sys
import json
import requests
import time
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_local_rag():
    """Test the RAG engine directly"""
    print("🧪 Testing NVIDIA RAG Engine locally...")
    
    try:
        from nvidia_rag import NVIDIARAGEngine
        
        # Initialize engine
        engine = NVIDIARAGEngine()
        
        # Load knowledge base
        print("📚 Loading knowledge base...")
        count = engine.load_knowledge_base()
        print(f"✅ Loaded {count} documents")
        
        # Test health check
        health = engine.health_check()
        print(f"🏥 Health Status: {health}")
        
        # Test chat
        print("\n💬 Testing chat functionality...")
        test_queries = [
            "What are good BMX bikes for beginners?",
            "How do I improve my cardio fitness?",
            "What should I look for in bike grips?"
        ]
        
        for query in test_queries:
            print(f"\n❓ Query: {query}")
            start_time = time.time()
            
            response = engine.chat(query)
            
            end_time = time.time()
            
            print(f"🤖 Response: {response['reply'][:100]}...")
            print(f"📊 Sources: {response['sources']}")
            print(f"⏱️  Time: {end_time - start_time:.2f}s")
            print(f"🔢 Tokens: {response.get('total_tokens', 'N/A')}")
            
    except Exception as e:
        print(f"❌ Local test failed: {e}")
        return False
    
    return True

def test_api_server():
    """Test the Flask API server"""
    print("\n🌐 Testing Flask API server...")
    
    base_url = "http://localhost:5000"
    
    try:
        # Test health endpoint
        print("🏥 Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test models endpoint
        print("🤖 Testing models endpoint...")
        response = requests.get(f"{base_url}/models", timeout=10)
        if response.status_code == 200:
            models_data = response.json()
            print(f"✅ Models info: {models_data}")
        else:
            print(f"⚠️  Models endpoint not available: {response.status_code}")
        
        # Test chat endpoint
        print("💬 Testing chat endpoint...")
        test_message = "What are the best BMX tricks for beginners?"
        
        chat_data = {
            "message": test_message,
            "temperature": 0.7,
            "max_tokens": 512
        }
        
        start_time = time.time()
        response = requests.post(
            f"{base_url}/chat",
            json=chat_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        end_time = time.time()
        
        if response.status_code == 200:
            chat_response = response.json()
            print(f"✅ Chat response received in {end_time - start_time:.2f}s")
            print(f"🤖 Reply: {chat_response.get('reply', 'No reply')[:100]}...")
            print(f"📊 Sources: {chat_response.get('sources', [])}")
            print(f"🔢 Context count: {chat_response.get('context_count', 0)}")
        else:
            print(f"❌ Chat request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:5000")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False
    
    return True

def check_environment():
    """Check environment configuration"""
    print("🔧 Checking environment configuration...")
    
    load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))
    
    required_vars = [
        'NVIDIA_API_KEY',
        'NVIDIA_NIM_BASE_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        print("💡 Make sure to copy .env.example to .env and fill in your API key")
        return False
    
    print("✅ Environment configuration looks good")
    return True

def main():
    """Run all tests"""
    print("🚀 AI Coach Bot - NVIDIA RAG System Test")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix configuration.")
        return
    
    # Test local RAG engine
    local_success = test_local_rag()
    
    # Test API server (optional)
    print("\n" + "=" * 50)
    print("🌐 API Server Test (optional)")
    print("Make sure the Flask server is running: python backend/app.py")
    
    try:
        api_success = test_api_server()
    except KeyboardInterrupt:
        print("\n⏹️  API test skipped by user")
        api_success = None
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"Local RAG Engine: {'✅ PASS' if local_success else '❌ FAIL'}")
    if api_success is not None:
        print(f"API Server: {'✅ PASS' if api_success else '❌ FAIL'}")
    else:
        print("API Server: ⏹️  SKIPPED")
    
    if local_success:
        print("\n🎉 Core system is working! Ready for deployment.")
    else:
        print("\n🔧 Please fix the issues above before deploying.")

if __name__ == "__main__":
    main()