from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from nvidia_rag import NVIDIARAGEngine

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize NVIDIA RAG Engine
rag_engine = NVIDIARAGEngine()

@app.route('/health', methods=['GET'])
def health():
    health_status = rag_engine.health_check()
    return jsonify(health_status), 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Extract optional parameters
    temperature = data.get('temperature', 0.7)
    max_tokens = data.get('max_tokens', 1024)
    top_k = data.get('top_k', 3)
    
    try:
        # Use the RAG engine for complete pipeline
        response = rag_engine.chat(
            user_message,
            temperature=temperature,
            max_tokens=max_tokens,
            top_k=top_k
        )
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            "reply": f"I apologize, but I encountered an error: {str(e)}",
            "sources": [],
            "error": str(e)
        }), 500

@app.route('/reload', methods=['POST'])
def reload_kb():
    """Reload knowledge base and recompute embeddings."""
    count = rag_engine.load_knowledge_base()
    return jsonify({"status": "reloaded", "documents": count}), 200

@app.route('/models', methods=['GET'])
def get_models():
    """Get current model configuration."""
    return jsonify({
        "llm_model": rag_engine.llm_model,
        "embedding_model": rag_engine.embedding_model,
        "base_url": os.getenv('NVIDIA_NIM_BASE_URL')
    }), 200

if __name__ == '__main__':
    # Load knowledge base on startup
    print("Loading knowledge base...")
    count = rag_engine.load_knowledge_base()
    print(f"Loaded {count} documents")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
