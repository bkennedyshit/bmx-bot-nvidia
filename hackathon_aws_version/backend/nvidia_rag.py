import os
import json
import numpy as np
from typing import List, Dict, Tuple
from openai import OpenAI
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class NVIDIARAGEngine:
    """
    RAG Engine using NVIDIA NIM microservices for both LLM and embeddings.
    Meets hackathon requirements with llama-3.1-nemotron-nano-8B-v1 and embedding NIM.
    """
    
    def __init__(self):
        # Initialize NVIDIA NIM clients
        self.llm_client = OpenAI(
            base_url=os.getenv('NVIDIA_NIM_BASE_URL', 'https://integrate.api.nvidia.com/v1'),
            api_key=os.getenv('NVIDIA_API_KEY')
        )
        
        # Model configurations for hackathon requirements
        self.llm_model = os.getenv('NVIDIA_LLM_MODEL', 'meta/llama-3.1-nemotron-nano-8b-instruct')
        self.embedding_model = os.getenv('NVIDIA_EMBEDDING_MODEL', 'nvidia/nv-embedqa-e5-v5')
        
        # Knowledge base and embeddings
        self.knowledge_base = []
        self.document_embeddings = None
        self.vectorizer = None
        
    def load_knowledge_base(self, data_path: str = None) -> int:
        """Load knowledge base from JSON file."""
        if not data_path:
            # Default path relative to backend directory
            data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed_blogs.json')
        
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.knowledge_base = data.get('blogs', [])
            
            # Pre-compute embeddings for retrieval
            self._compute_document_embeddings()
            return len(self.knowledge_base)
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            return 0
    
    def _compute_document_embeddings(self):
        """Compute embeddings for all documents using NVIDIA embedding NIM."""
        if not self.knowledge_base:
            return
        
        # Prepare document texts for embedding
        documents = []
        for doc in self.knowledge_base:
            # Combine title and content for better retrieval
            text = f"{doc.get('title', '')} {doc.get('content', '')}"
            documents.append(text)
        
        # Check if we have a real API key or if we're in test mode
        api_key = os.getenv('NVIDIA_API_KEY', '')
        if api_key and api_key != 'fake-key-for-testing' and 'fake' not in api_key.lower():
            try:
                # Use NVIDIA embedding NIM
                embeddings = self._get_embeddings(documents)
                self.document_embeddings = np.array(embeddings)
                print(f"✅ Using NVIDIA embeddings for {len(documents)} documents")
                return
            except Exception as e:
                print(f"Error computing embeddings with NVIDIA NIM: {e}")
        
        # Fallback to TF-IDF if no API key or embedding service fails
        print(f"🔄 Using TF-IDF fallback for {len(documents)} documents")
        self._compute_tfidf_embeddings(documents)
    
    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings from NVIDIA embedding NIM."""
        # Note: This uses the OpenAI-compatible embeddings endpoint
        embeddings = []
        
        for text in texts:
            try:
                response = self.llm_client.embeddings.create(
                    model=self.embedding_model,
                    input=text[:8000]  # Truncate to avoid token limits
                )
                embeddings.append(response.data[0].embedding)
            except Exception as e:
                print(f"Error getting embedding: {e}")
                # Return zero vector as fallback
                embeddings.append([0.0] * 768)  # Assuming 768-dim embeddings
        
        return embeddings
    
    def _compute_tfidf_embeddings(self, documents: List[str]):
        """Fallback TF-IDF embeddings if NVIDIA embedding service fails."""
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.document_embeddings = self.vectorizer.fit_transform(documents).toarray()    

    def retrieve_relevant_context(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve most relevant documents using semantic similarity."""
        if not self.knowledge_base or self.document_embeddings is None:
            return []
        
        try:
            # Get query embedding
            if self.vectorizer is not None:
                # Using TF-IDF fallback
                query_embedding = self.vectorizer.transform([query]).toarray()[0]
            else:
                # Using NVIDIA embeddings - check if we have real API key
                api_key = os.getenv('NVIDIA_API_KEY', '')
                if api_key and api_key != 'fake-key-for-testing' and 'fake' not in api_key.lower():
                    query_embeddings = self._get_embeddings([query])
                    query_embedding = np.array(query_embeddings[0])
                else:
                    # Fall back to keyword search if no real API key
                    return self._keyword_retrieval(query, top_k)
            
            # Compute similarities
            similarities = cosine_similarity([query_embedding], self.document_embeddings)[0]
            
            # Get top-k most similar documents
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            relevant_docs = []
            for idx in top_indices:
                if similarities[idx] > 0.05:  # Lower threshold for TF-IDF
                    doc = self.knowledge_base[idx].copy()
                    doc['similarity_score'] = float(similarities[idx])
                    relevant_docs.append(doc)
            
            return relevant_docs
            
        except Exception as e:
            print(f"Error in retrieval: {e}")
            # Fallback to keyword-based retrieval
            return self._keyword_retrieval(query, top_k)
    
    def _keyword_retrieval(self, query: str, top_k: int = 3) -> List[Dict]:
        """Fallback keyword-based retrieval."""
        query_lower = query.lower()
        scored_docs = []
        
        for doc in self.knowledge_base:
            score = 0
            content = doc.get('content', '').lower()
            title = doc.get('title', '').lower()
            
            for word in query_lower.split():
                if len(word) > 3:
                    score += content.count(word) * 1
                    score += title.count(word) * 3
            
            if score > 0:
                doc_copy = doc.copy()
                doc_copy['similarity_score'] = score
                scored_docs.append((score, doc_copy))
        
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, doc in scored_docs[:top_k]]
    
    def generate_response(self, query: str, context_docs: List[Dict], 
                         temperature: float = 0.7, max_tokens: int = 1024) -> Tuple[str, Dict]:
        """Generate response using NVIDIA LLM NIM with retrieved context."""
        
        # Build context from retrieved documents
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            title = doc.get('title', 'Unknown')
            content = doc.get('content', '')[:800]  # Limit content length
            score = doc.get('similarity_score', 0)
            context_parts.append(f"[Source {i}] {title}\nRelevance: {score:.3f}\nContent: {content}")
        
        context = "\n\n".join(context_parts)
        
        # Build the system prompt for the hackathon bot
        system_prompt = """You are an expert AI coach specializing in BMX, fitness, and product knowledge. 
        You have access to a curated knowledge base of expert articles and reviews.
        
        Instructions:
        - Use the provided context to answer questions accurately and conversationally
        - If the context doesn't contain relevant information, say so honestly
        - Provide practical, actionable advice when possible
        - Reference specific sources when making claims
        - Keep responses engaging and helpful"""
        
        # Build the user message with context
        user_message = f"""Context from knowledge base:
{context}

User Question: {query}

Please provide a helpful response based on the context above."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        try:
            # Call NVIDIA LLM NIM (llama-3.1-nemotron-nano-8B-v1)
            completion = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9
            )
            
            response_text = completion.choices[0].message.content
            
            # Prepare metadata
            metadata = {
                "model": completion.model,
                "sources": [doc.get('title', 'Unknown') for doc in context_docs],
                "context_count": len(context_docs),
                "total_tokens": getattr(completion.usage, 'total_tokens', 0) if hasattr(completion, 'usage') else 0
            }
            
            return response_text, metadata
            
        except Exception as e:
            error_msg = f"I apologize, but I encountered an error while processing your request: {str(e)}"
            metadata = {
                "model": "error",
                "sources": [],
                "context_count": 0,
                "error": str(e)
            }
            return error_msg, metadata
    
    def chat(self, query: str, **kwargs) -> Dict:
        """Main chat interface combining retrieval and generation."""
        
        # Extract parameters
        top_k = kwargs.get('top_k', 3)
        temperature = kwargs.get('temperature', 0.7)
        max_tokens = kwargs.get('max_tokens', 1024)
        
        # Retrieve relevant context
        context_docs = self.retrieve_relevant_context(query, top_k=top_k)
        
        # Generate response
        response_text, metadata = self.generate_response(
            query, context_docs, temperature=temperature, max_tokens=max_tokens
        )
        
        return {
            "reply": response_text,
            "sources": metadata.get("sources", []),
            "context_count": metadata.get("context_count", 0),
            "model": metadata.get("model", "unknown"),
            "total_tokens": metadata.get("total_tokens", 0),
            "error": metadata.get("error")
        }
    
    def health_check(self) -> Dict:
        """Health check for the RAG system."""
        return {
            "status": "healthy" if self.knowledge_base else "no_knowledge_base",
            "knowledge_base_loaded": len(self.knowledge_base) > 0,
            "documents": len(self.knowledge_base),
            "embeddings_computed": self.document_embeddings is not None,
            "llm_model": self.llm_model,
            "embedding_model": self.embedding_model
        }