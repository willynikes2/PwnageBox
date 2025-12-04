# 🚀 PwnageBox VPS Deployment Guide

## Step 1: Choose a VPS Provider

**Recommended Providers:**
| Provider | Min Plan | Cost/mo | Notes |
|----------|----------|---------|-------|
| **DigitalOcean** | 2GB RAM Droplet | $12 | Easy, great docs |
| **Linode** | Linode 2GB | $12 | Reliable |
| **Vultr** | 2GB Cloud | $12 | Global locations |
| **Hetzner** | CX21 | €4.85 | Best value (EU) |
| **AWS Lightsail** | 2GB | $10 | If you want AWS |

**Minimum Requirements:**
- 2GB RAM (4GB recommended for smooth Splunk)
- 1 vCPU (2 recommended)
- 50GB SSD
- Ubuntu 22.04 or 24.04 LTS

---

## Step 2: Initial VPS Setup

### 2.1 SSH into your new VPS
```bash
ssh root@YOUR_VPS_IP
```

### 2.2 Create a non-root user (security best practice)
```bash
# Create user
adduser pwnage
usermod -aG sudo pwnage

# Setup SSH key for new user
mkdir -p /home/pwnage/.ssh
cp ~/.ssh/authorized_keys /home/pwnage/.ssh/
chown -R pwnage:pwnage /home/pwnage/.ssh

# Switch to new user
su - pwnage
```

### 2.3 Update system
```bash
sudo apt update && sudo apt upgrade -y
```

### 2.4 Install Docker
```bash
# Install Docker
curl -fsSL https://get.docker.com | sudo sh

# Add your user to docker group (no sudo needed for docker commands)
sudo usermod -aG docker $USER

# Install Docker Compose plugin
sudo apt install docker-compose-plugin -y

# Log out and back in for group changes to take effect
exit
ssh pwnage@YOUR_VPS_IP

# Verify installation
docker --version
docker compose version
```

---

## Step 3: Configure Firewall

```bash
# Install UFW if not present
sudo apt install ufw -y

# Allow SSH (IMPORTANT - don't lock yourself out!)
sudo ufw allow 22/tcp

# Allow HTTP (Web UI)
sudo ufw allow 80/tcp

# Allow HTTPS (if you add SSL later)
sudo ufw allow 443/tcp

# Allow Splunk Web UI
sudo ufw allow 8000/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

---

## Step 4: Deploy PwnageBox

### 4.1 Upload or clone the project

**Option A: Upload the zip file**
```bash
# From your LOCAL machine
scp pwnagebox-lab.zip pwnage@YOUR_VPS_IP:~/

# On the VPS
cd ~
unzip pwnagebox-lab.zip
cd pwnagebox-lab
```

**Option B: Clone from GitHub (if you pushed it)**
```bash
cd ~
git clone https://github.com/willynikes2/PwnageBox.git
cd PwnageBox
```

### 4.2 Configure environment
```bash
# Copy example env
cp .env.example .env

# Edit with your secure password
nano .env
```

**IMPORTANT: Change these values in `.env`:**
```bash
# Use a STRONG password - this protects your attack button!
RECRUITER_PASSWORD=YourSuperSecretPassword123!

# Change Splunk password too
SPLUNK_PASSWORD=AnotherStrongPassword456!
```

### 4.3 Start the lab
```bash
# Make start script executable
chmod +x start.sh

# Run it
./start.sh
```

Or manually:
```bash
docker compose up -d --build
```

### 4.4 Verify everything is running
```bash
# Check container status
docker compose ps

# Check logs if something is wrong
docker compose logs -f
```

---

## Step 5: Access Your Lab

Open in browser:
- **Web UI:** `http://YOUR_VPS_IP`
- **Splunk:** `http://YOUR_VPS_IP:8000`

---

## Step 6: (Optional) Add a Domain & SSL

### 6.1 Point domain to VPS
Add an A record in your DNS:
```
Type: A
Name: pwnagebox (or @ for root)
Value: YOUR_VPS_IP
TTL: 300
```

### 6.2 Install Nginx as reverse proxy with SSL
```bash
# Install Nginx and Certbot
sudo apt install nginx certbot python3-certbot-nginx -y

# Create Nginx config
sudo nano /etc/nginx/sites-available/pwnagebox
```

**Paste this config:**
```nginx
server {
    listen 80;
    server_name pwnagebox.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
    }
}

server {
    listen 80;
    server_name splunk.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/pwnagebox /etc/nginx/sites-enabled/

# Update docker-compose.yml to use port 8080 instead of 80 for web-ui
# (so nginx can use port 80)

# Test and reload nginx
sudo nginx -t
sudo systemctl reload nginx

# Get SSL certificate
sudo certbot --nginx -d pwnagebox.yourdomain.com -d splunk.yourdomain.com
```

---

## Step 7: Maintenance Commands

```bash
# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f web-ui
docker compose logs -f pwnbox

# Restart everything
docker compose restart

# Stop everything
docker compose down

# Update and rebuild
git pull  # if using git
docker compose down
docker compose up -d --build

# Check resource usage
docker stats
```

---

## 🔒 Security Checklist

- [ ] Changed `RECRUITER_PASSWORD` to something strong
- [ ] Changed `SPLUNK_PASSWORD` to something strong
- [ ] Firewall enabled with only necessary ports
- [ ] Using non-root user
- [ ] SSH key authentication (disable password auth)
- [ ] (Optional) SSL/HTTPS configured
- [ ] (Optional) Fail2ban installed

### Disable SSH password authentication
```bash
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart sshd
```

### Install Fail2ban
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 🆘 Troubleshooting

### Splunk won't start (out of memory)
```bash
# Check memory
free -h

# If low on RAM, add swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Containers keep restarting
```bash
# Check logs
docker compose logs --tail=100

# Check system resources
htop
df -h
```

### Can't connect to ports
```bash
# Check if services are listening
sudo netstat -tlnp

# Check firewall
sudo ufw status

# Check if Docker is running
sudo systemctl status docker
```

---

## 📊 Quick Reference

| Task | Command |
|------|---------|
| Start lab | `docker compose up -d` |
| Stop lab | `docker compose down` |
| View logs | `docker compose logs -f` |
| Restart | `docker compose restart` |
| Rebuild | `docker compose up -d --build` |
| Check status | `docker compose ps` |
| Resource usage | `docker stats` |

---

## 💰 Cost Estimate

| Item | Monthly Cost |
|------|--------------|
| VPS (2GB) | $10-15 |
| Domain (optional) | $1 (amortized) |
| **Total** | **~$12/month** |

---

Good luck with your deployment! 🚀
