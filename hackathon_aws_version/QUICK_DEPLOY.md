# ⚡ QUICK DEPLOYMENT - Get This Running NOW

**Time estimate: 20-30 minutes**
**Cost: ~$100 in AWS credits**

## 🚨 Prerequisites Check

```bash
# Verify you have these installed
aws --version
docker --version
kubectl version --client
eksctl version
```

If missing anything:
- AWS CLI: https://aws.amazon.com/cli/
- Docker: https://docs.docker.com/get-docker/
- kubectl: `aws eks install kubectl`
- eksctl: https://eksctl.io/installation/

## 🎯 Step-by-Step Deployment

### 1. Set Your Variables (2 min)

```bash
export AWS_REGION=us-west-2
export CLUSTER_NAME=ai-coach-bot
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export ECR_REPO=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ai-coach-bot
export NVIDIA_API_KEY=your-actual-nvidia-api-key-here
```

### 2. Create EKS Cluster (15 min - this is the slow part)

```bash
eksctl create cluster \
  --name $CLUSTER_NAME \
  --region $AWS_REGION \
  --nodegroup-name workers \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed
```

**Go get coffee. This takes 15 minutes.**

### 3. Build & Push Docker Image (3 min)

```bash
# Create ECR repo
aws ecr create-repository --repository-name ai-coach-bot --region $AWS_REGION

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO

# Build and push
cd hackathon_aws_version
docker build -t ai-coach-bot:latest backend/
docker tag ai-coach-bot:latest $ECR_REPO:latest
docker push $ECR_REPO:latest
```

### 4. Deploy to Kubernetes (2 min)

```bash
# Create secret with your NVIDIA API key
kubectl create secret generic nvidia-credentials \
  --from-literal=api-key=$NVIDIA_API_KEY

# Update deploy.yaml with your ECR image
sed -i "s|your-ecr-repo|$ECR_REPO|g" deploy.yaml

# Deploy
kubectl apply -f deploy.yaml

# Wait for it to be ready
kubectl wait --for=condition=available --timeout=300s deployment/ai-coach-bot
```

### 5. Get Your URL (1 min)

```bash
# Get the LoadBalancer URL (may take 2-3 minutes to provision)
kubectl get service ai-coach-bot-service -w

# Once you see EXTERNAL-IP, test it:
export APP_URL=$(kubectl get service ai-coach-bot-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Test health
curl http://$APP_URL/health

# Test chat
curl -X POST http://$APP_URL/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are good BMX bikes for beginners?"}'
```

### 6. Update Frontend (1 min)

Edit `frontend/script.js` and replace the API URL:

```javascript
const API_URL = 'http://YOUR-LOADBALANCER-URL-HERE';
```

Then open `frontend/index.html` in your browser and test!

## 🎥 Record Your Demo

1. Open the frontend in browser
2. Start screen recording
3. Show these queries:
   - "What are good BMX bikes for beginners?"
   - "How do I improve my cardio for BMX racing?"
   - "What should I look for in bike grips?"
4. Show the sources being cited
5. Show the health endpoint in browser
6. Keep it under 3 minutes!

## 📤 Submit to GitHub

```bash
# Make sure you're in the repo root
cd ..

# Add everything
git add .
git commit -m "Hackathon submission - AI Coach Bot with NVIDIA NIMs on AWS EKS"
git push origin main

# Make repo public on GitHub
```

## 🧹 Cleanup (AFTER submission)

```bash
# Delete everything to stop charges
kubectl delete -f deploy.yaml
eksctl delete cluster --name $CLUSTER_NAME --region $AWS_REGION
aws ecr delete-repository --repository-name ai-coach-bot --force --region $AWS_REGION
```

## 🚨 Troubleshooting

**Cluster creation fails:**
- Check AWS quotas for EKS
- Try a different region

**Image won't push:**
- Verify ECR repo exists: `aws ecr describe-repositories`
- Check Docker is running

**LoadBalancer stuck pending:**
- Wait 5 minutes, it's slow
- Check security groups allow port 80

**NVIDIA API errors:**
- Verify API key: `curl -H "Authorization: Bearer $NVIDIA_API_KEY" https://integrate.api.nvidia.com/v1/models`
- Check you have credits at build.nvidia.com

## ⏱️ Credit Usage Monitor

```bash
# Check your AWS costs
aws ce get-cost-and-usage \
  --time-period Start=2025-10-18,End=2025-10-19 \
  --granularity DAILY \
  --metrics BlendedCost
```

**Expected costs:**
- EKS cluster: ~$0.10/hour
- EC2 nodes (2x t3.medium): ~$0.08/hour
- LoadBalancer: ~$0.025/hour
- **Total: ~$0.20/hour or ~$5/day**

You have $100, so you can run this for about 20 days. But deploy, test, record, and tear down ASAP!
