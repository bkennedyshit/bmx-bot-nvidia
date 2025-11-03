# 🚀 Deployment Guide - AI Coach Bot (NVIDIA/AWS Hackathon)

This guide walks you through deploying the AI Coach Bot on AWS infrastructure for the hackathon submission.

## 📋 Prerequisites

- AWS CLI configured with appropriate permissions
- Docker installed and running
- kubectl installed
- NVIDIA API key from [build.nvidia.com](https://build.nvidia.com)
- AWS account with EKS permissions

## 🏗️ Deployment Options

### Option 1: Amazon EKS (Recommended for Hackathon)
### Option 2: Amazon SageMaker Endpoint
### Option 3: Local Development

---

## 🎯 Option 1: Amazon EKS Deployment

### Step 1: Create EKS Cluster

```bash
# Create EKS cluster (this may take 10-15 minutes)
eksctl create cluster \
  --name ai-coach-bot-cluster \
  --region us-west-2 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 4 \
  --managed
```

### Step 2: Configure kubectl

```bash
# Update kubeconfig
aws eks update-kubeconfig --region us-west-2 --name ai-coach-bot-cluster

# Verify connection
kubectl get nodes
```

### Step 3: Build and Push Docker Image

```bash
# Create ECR repository
aws ecr create-repository --repository-name ai-coach-bot --region us-west-2

# Get ECR login
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <ACCOUNT-ID>.dkr.ecr.us-west-2.amazonaws.com

# Build image
cd hackathon_aws_version
docker build -t ai-coach-bot:latest backend/

# Tag for ECR
docker tag ai-coach-bot:latest <ACCOUNT-ID>.dkr.ecr.us-west-2.amazonaws.com/ai-coach-bot:latest

# Push to ECR
docker push <ACCOUNT-ID>.dkr.ecr.us-west-2.amazonaws.com/ai-coach-bot:latest
```

### Step 4: Create Kubernetes Secrets

```bash
# Create secret for NVIDIA API key
kubectl create secret generic nvidia-credentials \
  --from-literal=api-key=YOUR_NVIDIA_API_KEY
```

### Step 5: Update Deployment Configuration

Edit `deploy.yaml` and replace `your-ecr-repo` with your actual ECR repository URL:

```yaml
image: <ACCOUNT-ID>.dkr.ecr.us-west-2.amazonaws.com/ai-coach-bot:latest
```

### Step 6: Deploy to EKS

```bash
# Apply deployment
kubectl apply -f deploy.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# Get external IP (may take a few minutes)
kubectl get service ai-coach-bot-service
```

### Step 7: Test Deployment

```bash
# Get the external LoadBalancer URL
EXTERNAL_IP=$(kubectl get service ai-coach-bot-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Test health endpoint
curl http://$EXTERNAL_IP/health

# Test chat endpoint
curl -X POST http://$EXTERNAL_IP/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are good BMX bikes for beginners?"}'
```

---

## 🧠 Option 2: Amazon SageMaker Deployment

### Step 1: Create SageMaker Model

```python
import boto3
import sagemaker
from sagemaker.pytorch import PyTorchModel

# Initialize SageMaker session
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

# Create model
model = PyTorchModel(
    entry_point='app.py',
    source_dir='backend/',
    role=role,
    framework_version='1.12',
    py_version='py38',
    model_data='s3://your-bucket/model.tar.gz'  # Upload your code here
)

# Deploy endpoint
predictor = model.deploy(
    initial_instance_count=1,
    instance_type='ml.t3.medium'
)
```

### Step 2: Test SageMaker Endpoint

```python
# Test the endpoint
response = predictor.predict({
    "message": "What are good BMX bikes for beginners?"
})
print(response)
```

---

## 💻 Option 3: Local Development

### Step 1: Environment Setup

```bash
cd hackathon_aws_version/backend

# Copy environment template
cp .env.example .env

# Edit .env with your NVIDIA API key
nano .env
```

### Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 3: Run Application

```bash
# Start the backend
python app.py

# In another terminal, serve the frontend
cd ../frontend
python -m http.server 8080
```

### Step 4: Test Locally

```bash
# Run the test script
cd ..
python test_rag.py
```

---

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NVIDIA_API_KEY` | Your NVIDIA API key | Required |
| `NVIDIA_NIM_BASE_URL` | NVIDIA NIM base URL | `https://integrate.api.nvidia.com/v1` |
| `NVIDIA_LLM_MODEL` | LLM model name | `meta/llama-3.1-8b-instruct` |
| `NVIDIA_EMBEDDING_MODEL` | Embedding model name | `nvidia/nv-embedqa-e5-v5` |

### Kubernetes Resources

Adjust resources in `deploy.yaml` based on your needs:

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

---

## 📊 Monitoring and Logging

### CloudWatch Integration

```bash
# Install CloudWatch agent
kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/cloudwatch-namespace.yaml

# Configure logging
kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/cwagent/cwagent-daemonset.yaml
```

### Application Logs

```bash
# View application logs
kubectl logs -f deployment/ai-coach-bot

# View logs for specific pod
kubectl logs -f <pod-name>
```

---

## 🚨 Troubleshooting

### Common Issues

**Pod Not Starting**
```bash
# Check pod status
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp
```

**Image Pull Errors**
```bash
# Verify ECR permissions
aws ecr describe-repositories

# Check if image exists
aws ecr describe-images --repository-name ai-coach-bot
```

**NVIDIA API Errors**
```bash
# Test API key
curl -H "Authorization: Bearer $NVIDIA_API_KEY" \
  https://integrate.api.nvidia.com/v1/models
```

**LoadBalancer Not Getting External IP**
```bash
# Check service status
kubectl describe service ai-coach-bot-service

# Verify security groups allow traffic on port 80
```

### Performance Tuning

**Scaling Up**
```bash
# Increase replicas
kubectl scale deployment ai-coach-bot --replicas=5

# Enable horizontal pod autoscaler
kubectl autoscale deployment ai-coach-bot --cpu-percent=50 --min=2 --max=10
```

**Resource Optimization**
- Monitor CPU/memory usage with `kubectl top pods`
- Adjust resource requests/limits in deploy.yaml
- Consider using spot instances for cost savings

---

## 🧪 Testing Your Deployment

### Automated Testing

```bash
# Run the comprehensive test suite
python test_rag.py

# Test specific endpoints
curl http://your-loadbalancer-url/health
curl http://your-loadbalancer-url/models
```

### Load Testing

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Run load test
ab -n 100 -c 10 -p chat_payload.json -T application/json http://your-url/chat
```

### Frontend Testing

1. Update `frontend/script.js` with your deployment URL
2. Open `frontend/index.html` in a browser
3. Test the chat interface

---

## 🏆 Hackathon Submission Checklist

- [ ] EKS cluster created and running
- [ ] Application deployed with NVIDIA NIMs
- [ ] LoadBalancer accessible from internet
- [ ] Health endpoint returns 200
- [ ] Chat endpoint processes queries
- [ ] Frontend connects to backend
- [ ] All tests pass
- [ ] Demo video recorded
- [ ] Repository is public
- [ ] README includes deployment instructions

---

## 🔄 Cleanup

### Remove EKS Resources

```bash
# Delete application
kubectl delete -f deploy.yaml

# Delete secrets
kubectl delete secret nvidia-credentials

# Delete cluster (this will take several minutes)
eksctl delete cluster --name ai-coach-bot-cluster --region us-west-2
```

### Remove ECR Repository

```bash
aws ecr delete-repository --repository-name ai-coach-bot --force --region us-west-2
```

---

## 📞 Support

If you encounter issues during deployment:

1. Check the troubleshooting section above
2. Review AWS CloudWatch logs
3. Verify NVIDIA API key and quotas
4. Ensure all prerequisites are met

**Good luck with your hackathon submission! 🚀**