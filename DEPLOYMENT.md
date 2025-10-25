# Deployment Guide - AI Knowledge Assistant

Complete guide for deploying the AI Knowledge Assistant to production.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Local Docker Deployment](#local-docker-deployment)
- [Production Deployment](#production-deployment)
- [Environment Configuration](#environment-configuration)
- [Monitoring & Logging](#monitoring--logging)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required
- Docker 20.10+ and Docker Compose 2.0+
- Google API Key (Gemini)
- 2GB RAM minimum (4GB recommended)
- 5GB disk space

### Optional
- Domain name (for production)
- SSL certificate (Let's Encrypt recommended)
- Monitoring tools (Prometheus, Grafana)

## Local Docker Deployment

### Step 1: Clone & Configure

```bash
# Clone repository
git clone <repository-url>
cd <repository-directory>

# Create environment file
cp .env.production.example .env

# Edit .env and add your Google API key
nano .env
```

### Step 2: Build Embeddings

```bash
# Build embeddings before Docker (or mount volume)
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ../scripts
python build_embeddings.py
cd ..
```

### Step 3: Build and Run with Docker Compose

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 4: Verify Deployment

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost/

# View API docs
open http://localhost:8000/docs
```

### Step 5: Access the Application

- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Production Deployment

### Option 1: Docker Compose (Simple)

**Best for**: Single server deployments, small to medium scale

1. **Prepare Server**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

2. **Deploy Application**
```bash
# Clone on server
git clone <repository-url>
cd smart-doc-retriever2

# Configure environment
cp .env.production.example .env
nano .env  # Add production values

# Build embeddings
docker-compose run backend python /app/../scripts/build_embeddings.py

# Start services
docker-compose up -d

# Set up auto-restart
docker update --restart unless-stopped ai-assistant-backend ai-assistant-frontend
```

3. **Configure Reverse Proxy (Nginx)**

```nginx
# /etc/nginx/sites-available/ai-assistant
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Frontend
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout for long-running queries
        proxy_read_timeout 60s;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
    }
}
```

4. **Enable SSL with Let's Encrypt**
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Option 2: Kubernetes (Scalable)

**Best for**: Large scale deployments, high availability

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-assistant-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-assistant-backend
  template:
    metadata:
      labels:
        app: ai-assistant-backend
    spec:
      containers:
      - name: backend
        image: your-registry/ai-assistant-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: GOOGLE_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-assistant-secrets
              key: google-api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: ai-assistant-backend
spec:
  selector:
    app: ai-assistant-backend
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

### Option 3: Cloud Platforms

#### AWS (ECS)
```bash
# Build and push images
docker build -t ai-assistant-backend:latest ./backend
docker tag ai-assistant-backend:latest <account-id>.dkr.ecr.<region>.amazonaws.com/ai-assistant-backend:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ai-assistant-backend:latest

# Deploy with ECS
aws ecs update-service --cluster ai-assistant --service backend --force-new-deployment
```

#### Google Cloud (Cloud Run)
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/<project-id>/ai-assistant-backend ./backend
gcloud run deploy ai-assistant-backend \
  --image gcr.io/<project-id>/ai-assistant-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Environment Configuration

### Production Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_production_key_here
GEMINI_MODEL=gemini-pro
EMBEDDING_MODEL=Qwen/Qwen3-Embedding-0.6B

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
WORKERS=4

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Logging
LOG_LEVEL=WARNING  # INFO for debugging

# Security (generate secure values!)
SECRET_KEY=$(openssl rand -hex 32)
API_KEY=$(openssl rand -hex 16)

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Monitoring
SENTRY_DSN=your-sentry-dsn-here
ENABLE_METRICS=true
```

### Security Best Practices

1. **Never commit .env files**
2. **Use secrets management** (AWS Secrets Manager, etc.)
3. **Rotate API keys regularly**
4. **Enable HTTPS only**
5. **Implement rate limiting**
6. **Use strong authentication**

## Monitoring & Logging

### Docker Logs

```bash
# View all logs
docker-compose logs -f

# Backend logs only
docker-compose logs -f backend

# Frontend logs only
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Health Checks

```bash
# Backend health
curl https://yourdomain.com/health

# Backend status
curl https://yourdomain.com/status

# Container health
docker ps
```

### Metrics Collection

Add Prometheus for metrics:

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  prometheus-data:
  grafana-data:
```

## Troubleshooting

### Common Issues

#### 1. Backend not starting
```bash
# Check logs
docker-compose logs backend

# Common causes:
# - Missing GOOGLE_API_KEY
# - Vector store not found
# - Port 8000 already in use

# Solutions:
docker-compose down
docker-compose up -d backend
```

#### 2. Frontend can't reach backend
```bash
# Check network
docker network ls
docker network inspect smart-doc-retriever2_ai-assistant-network

# Check CORS settings in backend/.env
CORS_ORIGINS=http://localhost,https://yourdomain.com
```

#### 3. High memory usage
```bash
# Check resource usage
docker stats

# Limit resources in docker-compose.yml:
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 512M
```

#### 4. Slow query performance
```bash
# Check vector store
ls -lh backend/data/vector_store/

# Rebuild if needed
docker-compose run backend python /app/../scripts/build_embeddings.py

# Enable caching (add Redis)
```

### Debugging Commands

```bash
# Enter backend container
docker-compose exec backend bash

# Enter frontend container
docker-compose exec frontend sh

# Check backend Python
docker-compose exec backend python -c "import sys; print(sys.version)"

# Test API directly
docker-compose exec backend curl http://localhost:8000/health

# Restart specific service
docker-compose restart backend

# Rebuild specific service
docker-compose up -d --build backend
```

## Maintenance

### Updating the Application

```bash
# Pull latest code
git pull origin main

# Rebuild images
docker-compose build

# Restart with new images
docker-compose up -d

# Clean up old images
docker image prune -a
```

### Backup

```bash
# Backup vector store
tar -czf vector-store-backup-$(date +%Y%m%d).tar.gz backend/data/vector_store/

# Backup environment
cp .env .env.backup

# Restore
tar -xzf vector-store-backup-20251025.tar.gz -C backend/data/
```

### Scaling

```bash
# Scale backend replicas
docker-compose up -d --scale backend=3

# With load balancer (nginx)
# Add upstream configuration
```

---

**Deployment Checklist:**
- [ ] Environment variables configured
- [ ] Vector store built
- [ ] Docker images built
- [ ] Services running
- [ ] Health checks passing
- [ ] HTTPS configured
- [ ] Monitoring set up
- [ ] Backups configured
- [ ] Documentation reviewed
