# 📋 Hackathon Submission Checklist

## Before You Deploy

- [ ] NVIDIA API key obtained from build.nvidia.com
- [ ] AWS CLI configured with valid credentials
- [ ] $100 AWS promotional credits applied to account
- [ ] All prerequisites installed (docker, kubectl, eksctl)
- [ ] Knowledge base loaded (65+ blog posts in data/processed_blogs.json)

## Deployment Steps

- [ ] Run `./deploy.sh` successfully
- [ ] EKS cluster created and running
- [ ] Docker image built and pushed to ECR
- [ ] Application deployed to Kubernetes
- [ ] LoadBalancer has external IP/hostname
- [ ] Health endpoint returns 200 OK
- [ ] Chat endpoint processes queries successfully

## Testing

- [ ] Test health endpoint: `curl http://YOUR-URL/health`
- [ ] Test chat with BMX query
- [ ] Test chat with fitness query
- [ ] Test chat with product query
- [ ] Verify sources are cited in responses
- [ ] Frontend connects to backend successfully
- [ ] All responses use correct model (llama-3.1-nemotron-nano-8b-instruct)

## Demo Video (Under 3 Minutes)

- [ ] Screen recording software ready
- [ ] Show application URL in browser
- [ ] Demonstrate health check endpoint
- [ ] Show 3-4 different queries with responses
- [ ] Highlight source attribution feature
- [ ] Show model information endpoint
- [ ] Mention AWS EKS deployment
- [ ] Mention NVIDIA NIM usage
- [ ] Keep under 3 minutes total

## GitHub Repository

- [ ] All code committed to repository
- [ ] Repository is PUBLIC
- [ ] README.md is complete and accurate
- [ ] QUICK_DEPLOY.md included
- [ ] deploy.yaml has correct model name
- [ ] .env.example has correct model name
- [ ] No sensitive keys committed (check .env is in .gitignore)
- [ ] Repository URL is accessible

## DevPost Submission

- [ ] Project title: "AI Coach Bot - Agentic RAG with NVIDIA NIMs on AWS"
- [ ] Tagline written (under 60 characters)
- [ ] Description explains the project clearly
- [ ] Demo video uploaded (under 3 minutes)
- [ ] GitHub repository URL added
- [ ] Built with: AWS EKS, NVIDIA NIM, Python, Flask, Docker, Kubernetes
- [ ] Hackathon requirements met:
  - [ ] Uses llama-3.1-nemotron-nano-8b-instruct
  - [ ] Uses NVIDIA NIM inference microservice
  - [ ] Uses Retrieval Embedding NIM (nv-embedqa-e5-v5)
  - [ ] Deployed on AWS EKS
  - [ ] Complete RAG pipeline
- [ ] Screenshots added (frontend, architecture diagram)
- [ ] Team members added (if applicable)

## Required Submission Components

### 1. Text Description
- [ ] Explains what the bot does (BMX/fitness/product coaching)
- [ ] Mentions 65+ curated articles knowledge base
- [ ] Highlights RAG architecture
- [ ] Lists NVIDIA models used
- [ ] Describes AWS deployment
- [ ] Explains agentic behavior (autonomous retrieval + reasoning)

### 2. Demo Video
- [ ] Under 3 minutes
- [ ] Shows live deployment on AWS
- [ ] Demonstrates chat functionality
- [ ] Shows source attribution
- [ ] Highlights technical stack
- [ ] Uploaded to YouTube/Vimeo

### 3. Code Repository
- [ ] Public GitHub repository
- [ ] Complete source code
- [ ] README with deployment instructions
- [ ] All necessary configuration files
- [ ] No sensitive credentials

### 4. README File
- [ ] Project overview
- [ ] Architecture description
- [ ] Prerequisites listed
- [ ] Deployment instructions (step-by-step)
- [ ] Testing instructions
- [ ] Cleanup instructions
- [ ] Hackathon requirements checklist
- [ ] Contact information

## Post-Submission

- [ ] Verify submission was received on DevPost
- [ ] Test all links in submission work
- [ ] Demo video plays correctly
- [ ] GitHub repository is accessible
- [ ] Keep AWS deployment running until judging (monitor costs!)
- [ ] Respond to any judge questions promptly

## Cleanup (AFTER Judging)

- [ ] Run `./cleanup.sh` to delete all AWS resources
- [ ] Verify EKS cluster deleted
- [ ] Verify ECR repository deleted
- [ ] Check AWS billing to confirm charges stopped
- [ ] Archive project for portfolio

## Cost Monitoring

Current spend: $______
Remaining credits: $______
Daily burn rate: ~$5/day
Days until credits exhausted: ______

**Set a billing alarm!**
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name ai-coach-bot-cost-alarm \
  --alarm-description "Alert when costs exceed $80" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 21600 \
  --evaluation-periods 1 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

## Emergency Contacts

- AWS Support: https://console.aws.amazon.com/support/
- NVIDIA Developer Forums: https://forums.developer.nvidia.com/
- Hackathon Discord/Slack: [Add link if available]

---

**Good luck! 🚀**
