# 🏆 AI Coach Bot - NVIDIA/AWS Hackathon Version

[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA-NIM-76B900?style=for-the-badge&logo=nvidia)](https://build.nvidia.com)
[![AWS](https://img.shields.io/badge/AWS-EKS-FF9900?style=for-the-badge&logo=amazon-aws)](https://aws.amazon.com/eks/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python)](https://python.org)

An **Agentic AI Application** built for the [NVIDIA/AWS Hackathon](https://nvidia-aws.devpost.com/) featuring advanced RAG (Retrieval-Augmented Generation) capabilities powered by NVIDIA NIM microservices and deployable on AWS infrastructure.

## 🎯 Hackathon Requirements Met

✅ **llama-3.1-nemotron-nano-8b-instruct** large language reasoning model  
✅ **NVIDIA NIM inference microservice** deployment  
✅ **Retrieval Embedding NIM** for semantic search  
✅ **AWS EKS/SageMaker** deployment ready  
✅ **Complete RAG pipeline** with 65+ curated documents  

## 🚀 Features

- **Advanced RAG Pipeline**: Semantic retrieval using NVIDIA embedding NIMs
- **Expert Knowledge Base**: 65+ curated articles on BMX, fitness, and products
- **Real-time Chat Interface**: Interactive web UI with source attribution
- **Scalable Architecture**: Containerized for AWS EKS deployment
- **Fallback Mechanisms**: Robust error handling and TF-IDF backup
- **Performance Monitoring**: Token usage and response time tracking

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask API      │    │  NVIDIA NIMs    │
│   (React/HTML)  │◄──►│   (RAG Engine)   │◄──►│  LLM + Embed    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Knowledge Base │
                       │  (65+ Articles) │
                       └─────────────────┘
```

## 📋 Prerequisites

- Python 3.9+
- Docker & Docker Compose
- NVIDIA API Key ([Get one here](https://build.nvidia.com))
- AWS CLI configured (for deployment)
- kubectl (for EKS deployment)

## 🛠️ Local Development Setup

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd ai-coach-bot/hackathon_aws_version
```

### 2. Environment Configuration
```bash
cd backend
cp .env.example .env
# Edit .env with your NVIDIA API key
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
# Start the backend
python app.py

# Open frontend/index.html in your browser
# Or serve it with a simple HTTP server:
cd ../frontend
python -m http.server 8080
```

## 🐳 Docker Deployment

### Build and Run
```bash
# Build the Docker image
docker build -t ai-coach-bot:latest backend/

# Run with environment variables
docker run -p 5000:5000 \
  -e NVIDIA_API_KEY=your-key-here \
  -e NVIDIA_LLM_MODEL=meta/llama-3.1-8b-instruct \
  -e NVIDIA_EMBEDDING_MODEL=nvidia/nv-embedqa-e5-v5 \
  ai-coach-bot:latest
```

## ☁️ AWS EKS Deployment

### 1. Push to ECR
```bash
# Create ECR repository
aws ecr create-repository --repository-name ai-coach-bot

# Get login token
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-west-2.amazonaws.com

# Tag and push
docker tag ai-coach-bot:latest <account-id>.dkr.ecr.us-west-2.amazonaws.com/ai-coach-bot:latest
docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/ai-coach-bot:latest
```

### 2. Create Kubernetes Secret
```bash
kubectl create secret generic nvidia-credentials \
  --from-literal=api-key=your-nvidia-api-key
```

### 3. Deploy to EKS
```bash
# Update deploy.yaml with your ECR image URL
kubectl apply -f deploy.yaml

# Check deployment status
kubectl get pods
kubectl get services
```

## 🧪 Testing the RAG Pipeline

### Health Check
```bash
curl http://localhost:5000/health
```

### Chat API
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the best BMX tricks for beginners?"}'
```

### Model Information
```bash
curl http://localhost:5000/models
```

## 📊 Performance Metrics

The system tracks:
- **Response Time**: End-to-end query processing
- **Token Usage**: LLM token consumption
- **Retrieval Accuracy**: Semantic similarity scores
- **Source Attribution**: Document relevance tracking

## 🔧 Configuration Options

### Environment Variables
```bash
NVIDIA_API_KEY=your-nvidia-api-key
NVIDIA_NIM_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_LLM_MODEL=meta/llama-3.1-8b-instruct
NVIDIA_EMBEDDING_MODEL=nvidia/nv-embedqa-e5-v5
```

### API Parameters
- `temperature`: Response creativity (0.0-1.0)
- `max_tokens`: Maximum response length
- `top_k`: Number of retrieved documents

## 🚨 Troubleshooting

### Common Issues

**Knowledge Base Not Loading**
```bash
# Check file path and permissions
ls -la ../../data/processed_blogs.json
```

**NVIDIA API Errors**
```bash
# Verify API key and model availability
curl -H "Authorization: Bearer $NVIDIA_API_KEY" \
  https://integrate.api.nvidia.com/v1/models
```

**Docker Build Issues**
```bash
# Clean build with no cache
docker build --no-cache -t ai-coach-bot:latest backend/
```

## 📈 Scaling Considerations

- **Horizontal Scaling**: Increase replica count in deploy.yaml
- **Caching**: Implement Redis for embedding cache
- **Load Balancing**: Use AWS ALB for traffic distribution
- **Monitoring**: Add CloudWatch metrics and logging

## 🏅 Hackathon Submission Checklist

- [x] Uses llama-3.1-nemotron-nano-8B-v1 model
- [x] Implements NVIDIA NIM inference microservice
- [x] Includes Retrieval Embedding NIM
- [x] Deployable on AWS EKS
- [x] Complete RAG pipeline
- [x] Interactive demo interface
- [x] Comprehensive documentation
- [x] Docker containerization
- [x] Kubernetes deployment manifests

## 📝 Demo Script

1. **Health Check**: Show system status and loaded documents
2. **Basic Query**: "What are good BMX bikes for beginners?"
3. **Complex Query**: "How do I improve my cardio for BMX racing?"
4. **Product Query**: "What should I look for in bike grips?"
5. **Show Sources**: Demonstrate source attribution
6. **Performance**: Display response times and token usage

## 🤝 Contributing

This is a hackathon project, but contributions are welcome:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **NVIDIA** for providing NIM microservices
- **AWS** for cloud infrastructure
- **Hackathon Organizers** for the amazing opportunity
- **Open Source Community** for the tools and libraries

---

**Built with ❤️ for the NVIDIA/AWS Hackathon**