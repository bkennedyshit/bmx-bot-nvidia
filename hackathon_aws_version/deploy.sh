#!/bin/bash
set -e

echo "🚀 AI Coach Bot - AWS EKS Deployment Script"
echo "============================================"

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v aws >/dev/null 2>&1 || { echo "❌ AWS CLI not found. Install it first."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker not found. Install it first."; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "❌ kubectl not found. Install it first."; exit 1; }
command -v eksctl >/dev/null 2>&1 || { echo "❌ eksctl not found. Install it first."; exit 1; }
echo "✅ All prerequisites found"

# Get configuration
read -p "Enter AWS Region (default: us-west-2): " AWS_REGION
AWS_REGION=${AWS_REGION:-us-west-2}

read -p "Enter Cluster Name (default: ai-coach-bot): " CLUSTER_NAME
CLUSTER_NAME=${CLUSTER_NAME:-ai-coach-bot}

read -p "Enter your NVIDIA API Key: " NVIDIA_API_KEY
if [ -z "$NVIDIA_API_KEY" ]; then
    echo "❌ NVIDIA API Key is required"
    exit 1
fi

# Get AWS Account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ai-coach-bot"

echo ""
echo "Configuration:"
echo "  Region: $AWS_REGION"
echo "  Cluster: $CLUSTER_NAME"
echo "  ECR Repo: $ECR_REPO"
echo ""

read -p "Continue with deployment? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "Deployment cancelled"
    exit 0
fi

# Step 1: Create EKS Cluster
echo ""
echo "📦 Step 1/5: Creating EKS Cluster (this takes ~15 minutes)..."
if eksctl get cluster --name $CLUSTER_NAME --region $AWS_REGION >/dev/null 2>&1; then
    echo "✅ Cluster already exists, skipping creation"
else
    eksctl create cluster \
        --name $CLUSTER_NAME \
        --region $AWS_REGION \
        --nodegroup-name workers \
        --node-type t3.medium \
        --nodes 2 \
        --nodes-min 1 \
        --nodes-max 3 \
        --managed
    echo "✅ Cluster created"
fi

# Step 2: Create ECR Repository
echo ""
echo "🐳 Step 2/5: Setting up ECR Repository..."
if aws ecr describe-repositories --repository-names ai-coach-bot --region $AWS_REGION >/dev/null 2>&1; then
    echo "✅ ECR repository already exists"
else
    aws ecr create-repository --repository-name ai-coach-bot --region $AWS_REGION
    echo "✅ ECR repository created"
fi

# Step 3: Build and Push Docker Image
echo ""
echo "🔨 Step 3/5: Building and pushing Docker image..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO

docker build -t ai-coach-bot:latest backend/
docker tag ai-coach-bot:latest $ECR_REPO:latest
docker push $ECR_REPO:latest
echo "✅ Image pushed to ECR"

# Step 4: Create Kubernetes Secret
echo ""
echo "🔐 Step 4/5: Creating Kubernetes secret..."
kubectl delete secret nvidia-credentials --ignore-not-found=true
kubectl create secret generic nvidia-credentials --from-literal=api-key=$NVIDIA_API_KEY
echo "✅ Secret created"

# Step 5: Deploy Application
echo ""
echo "🚀 Step 5/5: Deploying application to EKS..."

# Update deploy.yaml with ECR image
sed "s|your-ecr-repo/ai-coach-bot:latest|$ECR_REPO:latest|g" deploy.yaml > deploy-temp.yaml

kubectl apply -f deploy-temp.yaml
rm deploy-temp.yaml

echo "⏳ Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/ai-coach-bot

echo "⏳ Waiting for LoadBalancer to get external IP..."
for i in {1..60}; do
    EXTERNAL_IP=$(kubectl get service ai-coach-bot-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' 2>/dev/null || echo "")
    if [ ! -z "$EXTERNAL_IP" ]; then
        break
    fi
    echo "  Still waiting... ($i/60)"
    sleep 5
done

if [ -z "$EXTERNAL_IP" ]; then
    echo "⚠️  LoadBalancer IP not ready yet. Check with: kubectl get service ai-coach-bot-service"
else
    echo ""
    echo "✅ DEPLOYMENT COMPLETE!"
    echo ""
    echo "🌐 Your application is available at:"
    echo "   http://$EXTERNAL_IP"
    echo ""
    echo "🧪 Test it with:"
    echo "   curl http://$EXTERNAL_IP/health"
    echo "   curl -X POST http://$EXTERNAL_IP/chat -H 'Content-Type: application/json' -d '{\"message\": \"What are good BMX bikes?\"}'"
    echo ""
    echo "📝 Update frontend/script.js with this URL:"
    echo "   const API_URL = 'http://$EXTERNAL_IP';"
    echo ""
    echo "💰 Monitor costs: This will cost ~$0.20/hour (~$5/day)"
    echo ""
    echo "🧹 To cleanup later:"
    echo "   kubectl delete -f deploy.yaml"
    echo "   eksctl delete cluster --name $CLUSTER_NAME --region $AWS_REGION"
fi
