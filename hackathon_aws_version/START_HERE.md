# 🚀 START HERE - Hackathon Deployment Guide

## What You Have
A complete AI Coach Bot with:
- ✅ 65+ curated blog posts (BMX, fitness, products)
- ✅ RAG pipeline with NVIDIA NIMs
- ✅ Correct model: llama-3.1-nemotron-nano-8b-instruct
- ✅ Flask backend + HTML frontend
- ✅ Docker containerization
- ✅ Kubernetes deployment manifests
- ✅ Automated deployment scripts

## What You Need
- [ ] NVIDIA API key from https://build.nvidia.com
- [ ] AWS account with $100 promotional credits
- [ ] 2-3 hours of time
- [ ] Screen recording software for demo

## Quick Start (5 Steps)

### Step 1: Setup Environment (5 min)
```bash
cd hackathon_aws_version

# Copy environment template
cp backend/.env.example backend/.env

# Edit backend/.env and add your NVIDIA API key
# Change: NVIDIA_API_KEY=your-nvidia-api-key-here
# To: NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxx
```

### Step 2: Test Locally (5 min)
```bash
# Test NVIDIA API works
python test_nvidia_api.py

# Test all prerequisites
python test_before_deploy.py
```

If both tests pass, continue. If not, fix the issues first.

### Step 3: Deploy to AWS (30 min)
```bash
# Make script executable
chmod +x deploy.sh

# Run deployment (this takes 15-20 minutes)
./deploy.sh
```

The script will:
1. Create EKS cluster (15 min - go get coffee)
2. Build and push Docker image (3 min)
3. Deploy to Kubernetes (2 min)
4. Give you a URL to test

### Step 4: Test Deployment (5 min)
```bash
# Get your URL
kubectl get service ai-coach-bot-service

# Test it
curl http://YOUR-URL/health
curl -X POST http://YOUR-URL/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are good BMX bikes for beginners?"}'
```

Update `frontend/script.js` with your URL and test in browser.

### Step 5: Record & Submit (30 min)
1. Record demo video (under 3 minutes)
2. Push to GitHub
3. Submit to DevPost

See [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) for details.

## File Guide

| File | Purpose |
|------|---------|
| `START_HERE.md` | This file - your starting point |
| `ACTION_PLAN.md` | Detailed timeline and steps |
| `QUICK_DEPLOY.md` | Manual deployment commands |
| `SUBMISSION_CHECKLIST.md` | Everything needed for submission |
| `deploy.sh` | Automated deployment script |
| `cleanup.sh` | Delete everything after judging |
| `test_nvidia_api.py` | Test NVIDIA API before deploying |
| `test_before_deploy.py` | Test all prerequisites |

## Cost Warning ⚠️

Running on AWS costs ~$5/day:
- EKS cluster: $0.10/hour
- EC2 nodes: $0.08/hour
- LoadBalancer: $0.025/hour

With $100 credits, you can run for ~20 days. But:
1. Deploy
2. Test
3. Record demo
4. Cleanup immediately

You can always redeploy later if needed.

## Troubleshooting

**"NVIDIA API key not set"**
- Edit `backend/.env` and add your key

**"AWS CLI not configured"**
- Run: `aws configure`
- Add your AWS access key and secret

**"eksctl not found"**
- Install from: https://eksctl.io/installation/

**"Deployment failed"**
- Check AWS quotas
- Try different region
- Check error logs: `kubectl logs -f deployment/ai-coach-bot`

## Next Steps

1. Read [ACTION_PLAN.md](ACTION_PLAN.md) for detailed timeline
2. Run `python test_nvidia_api.py` to verify API works
3. Run `python test_before_deploy.py` to check prerequisites
4. Run `./deploy.sh` to deploy to AWS
5. Follow [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) to submit

## Need Help?

- AWS Issues: Check AWS CloudWatch logs
- NVIDIA Issues: https://forums.developer.nvidia.com/
- Kubernetes Issues: `kubectl describe pod <pod-name>`

## After Submission

Keep deployment running until judging completes, then:
```bash
./cleanup.sh
```

This deletes everything and stops AWS charges.

---

**Ready? Let's go! 🚀**

```bash
python test_nvidia_api.py
```
