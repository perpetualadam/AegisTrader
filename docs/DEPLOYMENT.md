# 🚀 AegisTrader Deployment Guide

Complete deployment instructions for local and cloud environments.

## 📋 Table of Contents

- [Local Deployment](#local-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Docker Deployment](#docker-deployment)
- [Production Configuration](#production-configuration)
- [Security Considerations](#security-considerations)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Backup and Recovery](#backup-and-recovery)
- [Scaling Considerations](#scaling-considerations)

## 💻 Local Deployment

### Windows Setup

**Prerequisites**:
- Windows 10/11
- Python 3.8+ (from [python.org](https://python.org))
- Git for Windows

**Installation Steps**:
```powershell
# 1. Clone repository
git clone https://github.com/yourusername/aegistrader.git
cd aegistrader

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Install Tesseract OCR
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install to: C:\Program Files\Tesseract-OCR\

# 5. Configure environment
copy .env.example .env
# Edit .env with your settings

# 6. Create directories
mkdir data logs models screenshots

# 7. Test installation
python main.py
```

**Windows Service Setup** (Optional):
```powershell
# Install NSSM (Non-Sucking Service Manager)
# Download from: https://nssm.cc/download

# Create service
nssm install AegisTrader
nssm set AegisTrader Application "C:\path\to\aegistrader\venv\Scripts\python.exe"
nssm set AegisTrader AppParameters "C:\path\to\aegistrader\main.py"
nssm set AegisTrader AppDirectory "C:\path\to\aegistrader"
nssm start AegisTrader
```

### macOS Setup

**Prerequisites**:
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and dependencies
brew install python@3.11 tesseract git
```

**Installation Steps**:
```bash
# 1. Clone and setup
git clone https://github.com/yourusername/aegistrader.git
cd aegistrader

# 2. Virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
# Edit .env with your settings

# 5. Create directories
mkdir -p data logs models screenshots

# 6. Test
python main.py
```

**macOS Service Setup** (LaunchAgent):
```bash
# Create service file
cat > ~/Library/LaunchAgents/com.aegistrader.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aegistrader</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/aegistrader/venv/bin/python</string>
        <string>/path/to/aegistrader/main.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/aegistrader</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load service
launchctl load ~/Library/LaunchAgents/com.aegistrader.plist
```

### Linux Setup (Ubuntu/Debian)

**Installation Steps**:
```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y python3 python3-pip python3-venv git tesseract-ocr

# 3. Clone repository
git clone https://github.com/yourusername/aegistrader.git
cd aegistrader

# 4. Virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# 6. Configure
cp .env.example .env
# Edit .env with your settings

# 7. Create directories
mkdir -p data logs models screenshots

# 8. Test
python main.py
```

**Systemd Service Setup**:
```bash
# Create service file
sudo tee /etc/systemd/system/aegistrader.service << EOF
[Unit]
Description=AegisTrader Vision-Based Trading Bot
After=network.target

[Service]
Type=simple
User=aegistrader
WorkingDirectory=/home/aegistrader/aegistrader
Environment=PATH=/home/aegistrader/aegistrader/venv/bin
ExecStart=/home/aegistrader/aegistrader/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable aegistrader
sudo systemctl start aegistrader

# Check status
sudo systemctl status aegistrader
```

## ☁️ Cloud Deployment

### AWS EC2 Deployment

**Instance Setup**:
```bash
# 1. Launch EC2 instance (t3.medium recommended)
# - Ubuntu 22.04 LTS
# - Security group: SSH (22), HTTP (80), HTTPS (443)
# - Key pair for SSH access

# 2. Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Install dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git tesseract-ocr

# 4. Clone and setup
git clone https://github.com/yourusername/aegistrader.git
cd aegistrader
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Configure for cloud
cp .env.example .env
# Edit .env with cloud-specific settings
```

**AWS-Specific Configuration**:
```env
# .env for AWS
HEADLESS_BROWSER=true
LOG_LEVEL=INFO
SAVE_DEBUG_SCREENSHOTS=false

# Use AWS Secrets Manager for API keys
BROKER_API_KEY=${AWS_SECRET_BROKER_KEY}
BROKER_API_SECRET=${AWS_SECRET_BROKER_SECRET}
```

### Google Cloud Platform

**Compute Engine Setup**:
```bash
# 1. Create VM instance
gcloud compute instances create aegistrader-vm \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --machine-type=e2-medium \
    --zone=us-central1-a

# 2. SSH to instance
gcloud compute ssh aegistrader-vm --zone=us-central1-a

# 3. Follow Linux setup steps above
```

### Azure Virtual Machine

**VM Setup**:
```bash
# 1. Create resource group
az group create --name AegisTrader --location eastus

# 2. Create VM
az vm create \
    --resource-group AegisTrader \
    --name AegisTraderVM \
    --image UbuntuLTS \
    --admin-username azureuser \
    --generate-ssh-keys

# 3. Open ports
az vm open-port --port 22 --resource-group AegisTrader --name AegisTraderVM

# 4. Connect and setup
ssh azureuser@your-vm-ip
# Follow Linux setup steps
```

### VPS Deployment (DigitalOcean, Linode, etc.)

**Droplet/VPS Setup**:
```bash
# 1. Create droplet (2GB RAM minimum)
# 2. SSH to server
ssh root@your-vps-ip

# 3. Create user
adduser aegistrader
usermod -aG sudo aegistrader
su - aegistrader

# 4. Follow Linux setup steps
```

## 🐳 Docker Deployment

### Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p data logs models screenshots

# Set environment variables
ENV PYTHONPATH=/app
ENV HEADLESS_BROWSER=true

# Expose port (if needed for monitoring)
EXPOSE 8080

# Run application
CMD ["python", "main.py"]
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  aegistrader:
    build: .
    container_name: aegistrader
    restart: unless-stopped
    environment:
      - LIVE_TRADING=false
      - HEADLESS_BROWSER=true
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./models:/app/models
      - ./.env:/app/.env
    networks:
      - aegistrader-network
    
  # Optional: Add monitoring
  prometheus:
    image: prom/prometheus
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - aegistrader-network

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana
    networks:
      - aegistrader-network

networks:
  aegistrader-network:
    driver: bridge

volumes:
  grafana-storage:
```

### Docker Deployment Commands

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f aegistrader

# Stop services
docker-compose down

# Update and restart
docker-compose pull
docker-compose up -d --force-recreate
```

## 🔧 Production Configuration

### Environment Variables for Production

```env
# Production .env template
LIVE_TRADING=false  # Set to true only when ready
LOG_LEVEL=INFO
HEADLESS_BROWSER=true
SAVE_DEBUG_SCREENSHOTS=false

# Performance settings
SCAN_INTERVAL=300
MAX_BROWSER_INSTANCES=2
SCREENSHOT_QUALITY=75

# Security
BROKER_SANDBOX=true  # Use sandbox until fully tested

# Monitoring
TTS_ENABLED=false  # Disable in headless environments
```

### Production Optimizations

**Memory Management**:
```python
# Add to main.py for production
import gc
import psutil

def monitor_resources():
    """Monitor system resources."""
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        gc.collect()  # Force garbage collection
        logger.warning(f"High memory usage: {memory.percent}%")
```

**Log Rotation**:
```python
# Already implemented in utils/logger.py
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5
```

### Health Checks

Create `health_check.py`:
```python
#!/usr/bin/env python3
"""Health check script for AegisTrader."""

import sys
import requests
import psutil
from pathlib import Path

def check_process():
    """Check if AegisTrader process is running."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'main.py' in ' '.join(proc.info['cmdline'] or []):
            return True
    return False

def check_logs():
    """Check if logs are being written."""
    log_file = Path('logs/aegistrader.log')
    if not log_file.exists():
        return False
    
    # Check if log was modified in last 10 minutes
    import time
    return (time.time() - log_file.stat().st_mtime) < 600

def main():
    """Run health checks."""
    checks = [
        ("Process running", check_process),
        ("Logs active", check_logs),
    ]
    
    all_passed = True
    for name, check_func in checks:
        try:
            result = check_func()
            status = "PASS" if result else "FAIL"
            print(f"{name}: {status}")
            if not result:
                all_passed = False
        except Exception as e:
            print(f"{name}: ERROR - {e}")
            all_passed = False
    
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
```

## 🔒 Security Considerations

### API Key Management

**Environment Variables**:
```bash
# Never commit API keys to version control
echo ".env" >> .gitignore

# Use environment-specific files
.env.development
.env.staging
.env.production
```

**Cloud Secret Management**:
```bash
# AWS Secrets Manager
aws secretsmanager create-secret \
    --name "aegistrader/broker-api" \
    --secret-string '{"api_key":"xxx","api_secret":"yyy"}'

# Google Secret Manager
gcloud secrets create broker-api-key --data-file=api_key.txt

# Azure Key Vault
az keyvault secret set --vault-name AegisTraderVault --name broker-api-key --value "xxx"
```

### Network Security

**Firewall Rules**:
```bash
# Ubuntu UFW
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow from trusted-ip to any port 22

# AWS Security Groups
# Only allow SSH from your IP
# No inbound rules needed for trading bot
```

**VPN Setup** (Optional):
```bash
# OpenVPN client setup for secure broker connections
sudo apt install openvpn
# Configure VPN connection to broker's recommended servers
```

### File Permissions

```bash
# Secure file permissions
chmod 600 .env
chmod 700 data/ logs/
chmod 755 *.py

# Create dedicated user
sudo useradd -m -s /bin/bash aegistrader
sudo chown -R aegistrader:aegistrader /opt/aegistrader
```

## 📊 Monitoring and Maintenance

### System Monitoring

**Resource Monitoring Script**:
```python
# monitoring/system_monitor.py
import psutil
import time
import json
from datetime import datetime

def collect_metrics():
    """Collect system metrics."""
    return {
        'timestamp': datetime.now().isoformat(),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'network_io': psutil.net_io_counters()._asdict()
    }

def main():
    while True:
        metrics = collect_metrics()
        with open('logs/system_metrics.log', 'a') as f:
            f.write(json.dumps(metrics) + '\n')
        time.sleep(60)  # Collect every minute

if __name__ == "__main__":
    main()
```

### Log Monitoring

**Log Analysis Script**:
```bash
#!/bin/bash
# monitoring/log_monitor.sh

# Check for errors in last hour
tail -n 1000 logs/aegistrader.log | grep -i error | tail -10

# Check trading activity
tail -n 100 logs/trades.log | jq '.data.pnl' | awk '{sum+=$1} END {print "Total PnL:", sum}'

# Check system health
python3 health_check.py
```

### Automated Maintenance

**Maintenance Script**:
```bash
#!/bin/bash
# maintenance/daily_maintenance.sh

# Rotate logs if needed
find logs/ -name "*.log" -size +100M -exec gzip {} \;

# Clean old screenshots
find screenshots/ -name "*.png" -mtime +7 -delete

# Update system packages (weekly)
if [ $(date +%u) -eq 1 ]; then
    sudo apt update && sudo apt upgrade -y
fi

# Restart service if memory usage high
MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100.0)}')
if [ $MEMORY_USAGE -gt 90 ]; then
    sudo systemctl restart aegistrader
fi
```

**Cron Setup**:
```bash
# Add to crontab
crontab -e

# Daily maintenance at 2 AM
0 2 * * * /path/to/aegistrader/maintenance/daily_maintenance.sh

# Health check every 5 minutes
*/5 * * * * /path/to/aegistrader/health_check.py || echo "Health check failed" | mail -s "AegisTrader Alert" admin@example.com
```

## 💾 Backup and Recovery

### Backup Strategy

**Data Backup Script**:
```bash
#!/bin/bash
# backup/backup_data.sh

BACKUP_DIR="/backup/aegistrader/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup configuration
cp .env $BACKUP_DIR/
cp -r data/ $BACKUP_DIR/
cp -r logs/ $BACKUP_DIR/

# Backup to cloud (AWS S3 example)
aws s3 sync $BACKUP_DIR s3://aegistrader-backups/$(basename $BACKUP_DIR)

# Keep only last 30 days of backups
find /backup/aegistrader/ -type d -mtime +30 -exec rm -rf {} \;
```

**Database Backup** (if using external DB):
```bash
# PostgreSQL backup
pg_dump aegistrader_db > backup/aegistrader_$(date +%Y%m%d).sql

# MySQL backup
mysqldump aegistrader_db > backup/aegistrader_$(date +%Y%m%d).sql
```

### Disaster Recovery

**Recovery Procedure**:
```bash
# 1. Stop services
sudo systemctl stop aegistrader

# 2. Restore from backup
RESTORE_DATE="20240115_120000"
cp -r /backup/aegistrader/$RESTORE_DATE/* /opt/aegistrader/

# 3. Verify configuration
python3 -c "from config import validate_config; print(validate_config())"

# 4. Start services
sudo systemctl start aegistrader

# 5. Verify operation
python3 health_check.py
```

## 📈 Scaling Considerations

### Horizontal Scaling

**Multi-Instance Setup**:
```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  aegistrader-crypto:
    build: .
    environment:
      - DEFAULT_MARKETS=crypto
      - INSTANCE_ID=crypto
    volumes:
      - ./data/crypto:/app/data
      - ./logs/crypto:/app/logs

  aegistrader-stocks:
    build: .
    environment:
      - DEFAULT_MARKETS=stocks
      - INSTANCE_ID=stocks
    volumes:
      - ./data/stocks:/app/data
      - ./logs/stocks:/app/logs

  aegistrader-commodities:
    build: .
    environment:
      - DEFAULT_MARKETS=commodities
      - INSTANCE_ID=commodities
    volumes:
      - ./data/commodities:/app/data
      - ./logs/commodities:/app/logs
```

### Load Balancing

**Nginx Configuration**:
```nginx
# /etc/nginx/sites-available/aegistrader
upstream aegistrader_backend {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name aegistrader.example.com;

    location / {
        proxy_pass http://aegistrader_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Database Scaling

**PostgreSQL Setup**:
```sql
-- Create database for trading data
CREATE DATABASE aegistrader_db;
CREATE USER aegistrader WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE aegistrader_db TO aegistrader;

-- Create tables for trade history
CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    side VARCHAR(10),
    quantity DECIMAL(18,8),
    price DECIMAL(18,8),
    pnl DECIMAL(18,8),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Performance Optimization

**Resource Allocation**:
```bash
# Increase file descriptor limits
echo "aegistrader soft nofile 65536" >> /etc/security/limits.conf
echo "aegistrader hard nofile 65536" >> /etc/security/limits.conf

# Optimize Python garbage collection
export PYTHONOPTIMIZE=1
export PYTHONUNBUFFERED=1
```

This deployment guide provides comprehensive instructions for setting up AegisTrader in various environments, from local development to production cloud deployments with proper security, monitoring, and scaling considerations.

## 🔗 Additional Resources

- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions
- [API Integration Guide](API_INTEGRATION.md) - Broker API setup
- [Strategy Development Guide](STRATEGY_GUIDE.md) - Custom strategy creation
- [Main README](../README.md) - Project overview and quick start

## 📞 Support

For deployment-specific issues:
1. Check system logs: `journalctl -u aegistrader -f`
2. Verify configuration: `python3 -c "from config import validate_config; print(validate_config())"`
3. Run health checks: `python3 health_check.py`
4. Review deployment logs in `logs/` directory

Remember to always test in paper trading mode before deploying with live trading enabled.
