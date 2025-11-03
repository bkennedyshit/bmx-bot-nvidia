#!/bin/bash
set -e

echo "🧹 AI Coach Bot - Cleanup Script"
echo "================================="
echo ""
echo "⚠️  WARNING: This will delete ALL resources and stop AWS charges"
echo ""

read -p "Enter AWS Region (default: us-west-2): " AWS_REGION
AWS_REGION=${AWS_REGION:-us-west-2}

read -p "Enter Cluster Name (default: ai-coach-bot): " CLUSTER_NAME
CLUSTER_NAME=${CLUSTER_NAME:-ai-coach-bot}

echo ""
echo "This will delete:"
echo "  - Kubernetes deployment and service"
echo "  - EKS cluster: $CLUSTER_NAME"
echo "  - ECR repository: ai-coach-bot"
echo ""

read -p "Are you SURE you want to continue? (type 'yes'): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "Cleanup cancelled"
    exit 0
fi

echo ""
echo "🗑️  Step 1/3: Deleting Kubernetes resources..."
kubectl delete -f deploy.yaml --ignore-not-found=true || echo "No k8s resources found"

echo ""
echo "🗑️  Step 2/3: Deleting EKS cluster (this takes ~10 minutes)..."
eksctl delete cluster --name $CLUSTER_NAME --region $AWS_REGION || echo "Cluster not found"

echo ""
echo "🗑️  Step 3/3: Deleting ECR repository..."
aws ecr delete-repository --repository-name ai-coach-bot --force --region $AWS_REGION || echo "ECR repo not found"

echo ""
echo "✅ Cleanup complete! All resources deleted."
echo "💰 AWS charges should stop within a few minutes."
