# 🏆 AI Coach Bot - NVIDIA/AWS Hackathon Submission

[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA-NIM-76B900?style=for-the-badge&logo=nvidia)](https://build.nvidia.com)
[![AWS EKS](https://img.shields.io/badge/AWS-EKS-FF9900?style=for-the-badge&logo=amazon-aws)](https://aws.amazon.com/eks/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An **Agentic AI Application** built for the [NVIDIA/AWS Hackathon](https://nvidia-aws.devpost.com/) featuring advanced RAG (Retrieval-Augmented Generation) capabilities powered by NVIDIA NIM microservices and deployed on AWS EKS.

## 🎯 Hackathon Requirements Met

✅ **llama-3.1-nemotron-nano-8b-instruct** large language reasoning model  
✅ **NVIDIA NIM inference microservice** deployment  
✅ **Retrieval Embedding NIM** (nvidia/nv-embedqa-e5-v5)  
✅ **AWS EKS** deployment ready  
✅ **Complete RAG pipeline** with 65+ curated documents  
✅ **Agentic behavior** with autonomous retrieval and reasoning

---

## 📖 Table of Contents

- [About The Project](#about-the-project)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [Demo](#demo)
- [Architecture](#architecture)
- [License](#license)
- [Contact](#contact)

---

## 🚀 About The Project

The AI Coach Bot is an intelligent agentic application that provides expert coaching on BMX, fitness, and product knowledge. Built specifically for the NVIDIA/AWS Hackathon, it demonstrates the power of combining NVIDIA's cutting-edge NIM microservices with AWS's scalable infrastructure.

**Key Innovation:** The bot autonomously retrieves relevant information from a curated knowledge base of 65+ expert articles and uses advanced reasoning to provide contextual, source-attributed responses.

---

## ✨ Key Features

- **Advanced RAG Pipeline:** Semantic retrieval using NVIDIA embedding NIMs
- **Expert Knowledge Base:** 65+ curated articles on BMX, fitness, and products  
- **Agentic Behavior:** Autonomous information retrieval and contextual reasoning
- **Real-time Chat Interface:** Interactive web UI with source attribution
- **Scalable Architecture:** Containerized for AWS EKS deployment
- **Performance Monitoring:** Token usage and response time tracking
- **Fallback Mechanisms:** Robust error handling with TF-IDF backup

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![NVIDIA](https://img.shields.io/badge/NVIDIA-%2376B900.svg?style=for-the-badge&logo=nvidia&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

### NVIDIA NIMs Used
- **LLM:** `meta/llama-3.1-nemotron-nano-8b-instruct`
- **Embeddings:** `nvidia/nv-embedqa-e5-v5`

### AWS Services
- **Amazon EKS** - Kubernetes orchestration
- **Amazon ECR** - Container registry  
- **Application Load Balancer** - Traffic distribution

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask API      │    │  NVIDIA NIMs    │
│   (HTML/JS)     │◄──►│   (RAG Engine)   │◄──►│  LLM + Embed    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Knowledge Base │
                       │  (65+ Articles) │
                       └─────────────────┘
```

## 📂 Project Structure

```
ai-coach-bot/
├── data/                           # Knowledge base (65+ articles)
│   └── processed_blogs.json
├── scripts/                        # Data processing utilities
├── hackathon_aws_version/          # Main hackathon submission
│   ├── backend/                    # Flask API with RAG pipeline
│   │   ├── app.py                  # Main application
│   │   ├── requirements.txt        # Python dependencies
│   │   ├── Dockerfile             # Container configuration
│   │   └── .env.example           # Environment template
│   ├── frontend/                   # Web interface
│   │   ├── index.html             # Chat interface
│   │   └── script.js              # Frontend logic
│   ├── deploy.yaml                # Kubernetes deployment
│   ├── deploy.sh                  # Automated deployment script
│   └── cleanup.sh                 # Resource cleanup script
└── README.md                      # This file
```

---

## ⚡ Quick Start

### Prerequisites

- Python 3.9+
- Docker & Docker Compose
- AWS CLI configured
- kubectl and eksctl
- NVIDIA API Key ([Get one here](https://build.nvidia.com))

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-coach-bot.git
   cd ai-coach-bot/hackathon_aws_version
   ```

2. **Set up environment**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your NVIDIA API key
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run locally**
   ```bash
   python app.py
   # Open frontend/index.html in browser
   ```

### Docker Deployment

```bash
# Build and run
docker build -t ai-coach-bot:latest backend/
docker run -p 5000:5000 \
  -e NVIDIA_API_KEY=your-key-here \
  ai-coach-bot:latest
```

---

## ☁️ AWS EKS Deployment

For complete deployment instructions, see [QUICK_DEPLOY.md](hackathon_aws_version/QUICK_DEPLOY.md)

### One-Command Deploy
```bash
cd hackathon_aws_version
./deploy.sh
```

### Manual Steps
1. Create EKS cluster with eksctl
2. Build and push Docker image to ECR  
3. Deploy to Kubernetes with kubectl
4. Access via LoadBalancer URL

**Estimated Cost:** ~$5/day with $100 AWS credits

## 🎥 Demo

### Example Queries
- "What are good BMX bikes for beginners?"
- "How do I improve my cardio for BMX racing?"  
- "What should I look for in bike grips?"
- "Explain the basics of a bunny hop"

### API Endpoints
- `GET /health` - System status
- `POST /chat` - Chat with the bot
- `GET /models` - Model information

---

## 🧪 Testing

### Health Check
```bash
curl http://localhost:5000/health
```

### Chat API
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are good BMX bikes for beginners?"}'
```

## 📊 Performance Metrics

The system tracks:
- Response time and token usage
- Retrieval accuracy with similarity scores  
- Source attribution and document relevance
- Model performance monitoring

## 🏅 Hackathon Compliance

- ✅ Uses `llama-3.1-nemotron-nano-8b-instruct`
- ✅ NVIDIA NIM inference microservice
- ✅ Retrieval Embedding NIM (`nvidia/nv-embedqa-e5-v5`)
- ✅ AWS EKS deployment
- ✅ Complete RAG pipeline
- ✅ Agentic autonomous behavior

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📫 Contact

Billy Kennedy - [@billykennedybmx](https://x.com/billykennedybmx) - billykennedy@nepa-ai.com

**Built with ❤️ for the NVIDIA/AWS Hackathon**
