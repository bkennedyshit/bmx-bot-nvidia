#!/usr/bin/env python3
"""
Pre-deployment test to verify everything works locally before burning AWS credits.
"""
import os
import sys
import json
from pathlib import Path

def test_knowledge_base():
    """Test that knowledge base exists and is valid."""
    print("📚 Testing knowledge base...")
    kb_path = Path(__file__).parent.parent / "data" / "processed_blogs.json"
    
    if not kb_path.exists():
        print(f"❌ Knowledge base not found at {kb_path}")
        return False
    
    try:
        with open(kb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            blogs = data.get('blogs', [])
            
            if len(blogs) < 10:
                print(f"⚠️  Only {len(blogs)} blogs found. Expected 65+")
                return False
            
            print(f"✅ Knowledge base loaded: {len(blogs)} documents")
            return True
    except Exception as e:
        print(f"❌ Error loading knowledge base: {e}")
        return False

def test_dependencies():
    """Test that all Python dependencies are installed."""
    print("\n📦 Testing Python dependencies...")
    required = [
        'flask',
        'flask_cors',
        'openai',
        'numpy',
        'sklearn',
        'requests',
        'python-dotenv'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r backend/requirements.txt")
        return False
    
    return True

def test_env_file():
    """Test that .env file exists and has required variables."""
    print("\n🔐 Testing environment configuration...")
    env_path = Path(__file__).parent / "backend" / ".env"
    
    if not env_path.exists():
        print("⚠️  .env file not found. Copy from .env.example")
        print("   cp backend/.env.example backend/.env")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
        
        if 'your-nvidia-api-key-here' in content:
            print("❌ NVIDIA_API_KEY not set in .env file")
            return False
        
        if 'llama-3.1-nemotron-nano-8b-instruct' not in content:
            print("⚠️  Wrong model in .env. Should be: llama-3.1-nemotron-nano-8b-instruct")
            return False
    
    print("✅ Environment file configured")
    return True

def test_docker():
    """Test that Docker is available."""
    print("\n🐳 Testing Docker...")
    result = os.system("docker --version > /dev/null 2>&1")
    if result != 0:
        print("❌ Docker not found or not running")
        return False
    print("✅ Docker available")
    return True

def test_aws_cli():
    """Test that AWS CLI is configured."""
    print("\n☁️  Testing AWS CLI...")
    result = os.system("aws --version > /dev/null 2>&1")
    if result != 0:
        print("❌ AWS CLI not found")
        return False
    
    result = os.system("aws sts get-caller-identity > /dev/null 2>&1")
    if result != 0:
        print("❌ AWS CLI not configured. Run: aws configure")
        return False
    
    print("✅ AWS CLI configured")
    return True

def test_kubectl():
    """Test that kubectl is available."""
    print("\n⎈  Testing kubectl...")
    result = os.system("kubectl version --client > /dev/null 2>&1")
    if result != 0:
        print("❌ kubectl not found")
        return False
    print("✅ kubectl available")
    return True

def test_eksctl():
    """Test that eksctl is available."""
    print("\n🚀 Testing eksctl...")
    result = os.system("eksctl version > /dev/null 2>&1")
    if result != 0:
        print("❌ eksctl not found")
        print("   Install: https://eksctl.io/installation/")
        return False
    print("✅ eksctl available")
    return True

def test_model_config():
    """Test that model configuration is correct."""
    print("\n🤖 Testing model configuration...")
    
    # Check deploy.yaml
    deploy_path = Path(__file__).parent / "deploy.yaml"
    with open(deploy_path, 'r') as f:
        content = f.read()
        if 'llama-3.1-nemotron-nano-8b-instruct' not in content:
            print("❌ Wrong model in deploy.yaml")
            return False
    
    # Check nvidia_rag.py
    rag_path = Path(__file__).parent / "backend" / "nvidia_rag.py"
    with open(rag_path, 'r') as f:
        content = f.read()
        if 'llama-3.1-nemotron-nano-8b-instruct' not in content:
            print("❌ Wrong model in nvidia_rag.py")
            return False
    
    print("✅ Model configuration correct (llama-3.1-nemotron-nano-8b-instruct)")
    return True

def main():
    print("🔍 Pre-Deployment Test Suite")
    print("=" * 50)
    
    tests = [
        ("Knowledge Base", test_knowledge_base),
        ("Python Dependencies", test_dependencies),
        ("Environment File", test_env_file),
        ("Docker", test_docker),
        ("AWS CLI", test_aws_cli),
        ("kubectl", test_kubectl),
        ("eksctl", test_eksctl),
        ("Model Configuration", test_model_config),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            results.append(test_func())
        except Exception as e:
            print(f"❌ {name} test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    for (name, _), result in zip(tests, results):
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready to deploy.")
        print("\nNext steps:")
        print("  1. Run: cd hackathon_aws_version")
        print("  2. Run: chmod +x deploy.sh")
        print("  3. Run: ./deploy.sh")
        return 0
    else:
        print("\n⚠️  Some tests failed. Fix issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
