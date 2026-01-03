# FLY.IO DEPLOYMENT CHECKLIST - Production Guide

## Pre-Deployment Verification

Before starting, verify you have:

```
✅ Fly.io account (free tier)
✅ Fly CLI installed
✅ Docker installed
✅ Git repository ready
✅ All app code committed
✅ Environment variables documented
✅ Payment credentials (Cashfree)
✅ Custom domain (optional but recommended)
```

---

## STEP 1: Install Fly CLI

### Windows (PowerShell):
```powershell
# Install Homebrew first if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Fly CLI
brew install flyctl

# Verify
flyctl version
```

### Mac:
```bash
brew install flyctl
flyctl version
```

### Linux:
```bash
curl -L https://fly.io/install.sh | sh
flyctl version
```

---

## STEP 2: Create Fly.io Account

1. Go to https://fly.io
2. Click "Sign Up"
3. Create account (choose free tier)
4. Verify your email

---

## STEP 3: Login to Fly CLI

```bash
flyctl auth login
# This opens your browser for authentication
# Follow the prompts
```

Verify login:
```bash
flyctl auth whoami
```

---

## STEP 4: Prepare Your Application

### Create fly.toml in project root:

```toml
app = "d-sector-etf-analyzer"  # Change to your app name
primary_region = "del"  # Delhi region for India

[build]
builder = "paketobuildpacks"

[env]
STREAMLIT_SERVER_HEADLESS = "true"
STREAMLIT_SERVER_PORT = "8080"
STREAMLIT_SERVER_ENABLECORS = "false"
STREAMLIT_LOGGER_LEVEL = "info"

[[services]]
protocol = "tcp"
internal_port = 8080
processes = ["app"]

  [[services.ports]]
  port = 80
  handlers = ["http"]

  [[services.ports]]
  port = 443
  handlers = ["tls", "http"]

[checks]
  [checks.alive]
    type = "http"
    interval = "10s"
    timeout = "5s"
    grace_period = "5s"
    method = "GET"
    path = "/"

[deploy]
  release_command = "true"
  strategy = "rolling"
```

### Update requirements.txt:

```txt
streamlit==1.28.1
pandas==2.0.3
requests==2.31.0
python-dateutil==2.8.2
cashfree-pg==2.0.0
python-dotenv==1.0.0
Pillow==10.0.0
altair==5.0.1
```

### Update Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/.streamlit
RUN mkdir -p /app/data

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

EXPOSE 8080

CMD ["python", "-O", "-m", "streamlit", "run", "main.py", \
     "--server.port=8080", "--server.address=0.0.0.0"]
```

### Create .dockerignore:

```
.git
.gitignore
.env
.env.local
__pycache__
*.pyc
.pytest_cache
.streamlit/cache
node_modules
.DS_Store
*.log
.venv
venv/
.idea
.vscode
*.egg-info
dist
build
```

---

## STEP 5: Setup Environment Variables

### Create .env.production file (don't commit to git):

```bash
# Cashfree (Production)
CASHFREE_CLIENT_ID=your_production_client_id
CASHFREE_CLIENT_SECRET=your_production_secret
CASHFREE_ENVIRONMENT=production

# Application
APP_DOMAIN=https://yourdomain.fly.dev
DEBUG=False
PYTHONUNBUFFERED=1
```

### Add to .gitignore:
```
.env
.env.local
.env.production
```

---

## STEP 6: Create Persistent Storage Volume

```bash
# Create volume for data persistence
flyctl volume create data --region del --size 1

# Verify volume created
flyctl volume list
```

### Update fly.toml to use volume:

```toml
[mounts]
source = "data"
destination = "/app/data"
```

### Update code to use /app/data:

```python
import os

DATA_DIR = "/app/data"
os.makedirs(DATA_DIR, exist_ok=True)

USERS_DB_FILE = os.path.join(DATA_DIR, "users_database.json")
SUBSCRIPTIONS_FILE = os.path.join(DATA_DIR, "subscriptions.json")
PAYMENT_LOG = os.path.join(DATA_DIR, "payment_logs.json")
```

---

## STEP 7: Initialize Fly App

```bash
# This creates your app on Fly.io
flyctl launch

# Follow prompts:
# - App name: d-sector-etf-analyzer
# - Region: del (Delhi)
# - Setup Postgres: No
# - Deploy: Yes (or do manually later)
```

---

## STEP 8: Set Secrets on Fly.io

```bash
# Set your production credentials
flyctl secrets set \
  CASHFREE_CLIENT_ID="your_production_id" \
  CASHFREE_CLIENT_SECRET="your_production_secret" \
  CASHFREE_ENVIRONMENT="production" \
  APP_DOMAIN="https://yourdomain.fly.dev"

# Verify secrets are set
flyctl secrets list
```

---

## STEP 9: Deploy Application

```bash
# Deploy to Fly.io
flyctl deploy

# Watch deployment logs
flyctl logs -f

# Wait for "Deployed successfully" message
```

### Deployment complete when:
- ✅ Docker image builds successfully
- ✅ App starts without errors
- ✅ Health check passes
- ✅ App is accessible

---

## STEP 10: Verify Deployment

```bash
# Check app status
flyctl status

# View logs
flyctl logs

# Open app in browser (automatic)
flyctl open

# Or visit: https://d-sector-etf-analyzer.fly.dev
```

### Test your app:

```
1. Open: https://d-sector-etf-analyzer.fly.dev
2. Login with: admin / Manu
3. Navigate to: Analyzer page
4. Test: Payment flow (sandbox)
5. Check: All features working
```

---

## STEP 11: Configure Custom Domain (Optional)

### Create SSL certificate:

```bash
# Add your domain
flyctl certs create yourdomain.com

# Add www subdomain
flyctl certs create www.yourdomain.com

# Check certificate status
flyctl certs list
```

### Update DNS at your registrar (GoDaddy, Namecheap, etc):

```
Type: CNAME
Host: yourdomain.com
Value: yourdomain.fly.dev
TTL: 3600

Type: CNAME
Host: www
Value: yourdomain.fly.dev
TTL: 3600
```

### Verify certificate:

```bash
# After DNS updates (can take up to 24 hours):
flyctl certs list

# Should show VERIFIED status
```

---

## STEP 12: Setup Monitoring

### View real-time metrics:

```bash
# CPU and memory usage
flyctl metrics

# Live logs
flyctl logs -f

# Monitor in browser (optional)
# Visit: https://fly.io → Dashboard → Your App
```

### Enable automatic restarts:

```bash
# Already enabled by default health checks
# But verify in fly.toml:
[checks]
  [checks.alive]
    type = "http"
    interval = "10s"
    timeout = "5s"
    grace_period = "5s"
    method = "GET"
    path = "/"
```

---

## STEP 13: Setup Automated Deployments (GitHub CI/CD)

### Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Fly.io

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Flyctl
        uses: superfly/flyctl-actions/setup-flyctl@master
      
      - name: Deploy to Fly.io
        run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### Add GitHub Secret:

```bash
# Get your Fly API token
flyctl auth token

# Add to GitHub:
# Go to: Repo → Settings → Secrets → New repository secret
# Name: FLY_API_TOKEN
# Value: (paste your token)
```

### Now every push to main auto-deploys!

```bash
git add .
git commit -m "Update feature"
git push origin main
# → Auto-deploys to Fly.io! 🚀
```

---

## Post-Deployment Checklist

```
Testing:
☐ App loads without errors
☐ Login works (admin / Manu)
☐ Registration works
☐ Payment flow works (sandbox)
☐ All sectors display
☐ All ETFs display
☐ Charts render correctly
☐ Mobile responsive

Infrastructure:
☐ App status shows "running"
☐ Health checks passing
☐ Logs show no errors
☐ Metrics showing normal CPU
☐ Data persisting (volume working)

Monitoring:
☐ Real-time metrics accessible
☐ Logs accessible
☐ Can view deployment history
☐ Can rollback if needed

Security:
☐ HTTPS working (lock icon)
☐ Secrets properly set
☐ No hardcoded credentials
☐ .env not in git
```

---

## Troubleshooting

### App won't start

```bash
# Check logs
flyctl logs -f

# Common issues:
1. Missing environment variable
   → Solution: flyctl secrets set KEY=value

2. Database file not found
   → Solution: Check /app/data mount

3. Port binding error
   → Solution: Ensure port 8080 is used

4. Restart app
   → flyctl restart
```

### High CPU usage

```bash
# Check what's consuming CPU
flyctl logs -f

# Quick fix:
1. Add caching to main.py
2. Use lazy loading (tabs)
3. Deploy: flyctl deploy
4. Monitor: flyctl metrics

# See QUICK_OPTIMIZATION_STEPS.md for details
```

### Data not persisting

```bash
# Verify volume is mounted
flyctl volume list

# Check fly.toml
cat fly.toml | grep -A 2 "mounts"

# Should show:
# [mounts]
# source = "data"
# destination = "/app/data"
```

### Custom domain not working

```bash
# Check DNS propagation
nslookup yourdomain.com

# Check certificate status
flyctl certs list

# Should show VERIFIED (can take 24 hours)
```

---

## Cost Estimation

**Fly.io Pricing (Free Tier):**

| Resource | Limit | Cost |
|----------|-------|------|
| Apps | 3 free | $0 |
| Shared CPU | 600 hours/month | Included |
| Memory | 3GB total | Included |
| Storage | 3GB | Included |
| Bandwidth | 30GB/month | Included |

**Your app will be FREE!** 🎉

---

## Useful Commands

```bash
# Status & monitoring
flyctl status                 # Check app status
flyctl logs -f                # View live logs
flyctl metrics                # CPU & memory
flyctl scale show             # Current scaling

# Deployment
flyctl deploy                 # Deploy latest
flyctl releases               # View history
flyctl releases rollback      # Revert to previous

# Secrets & config
flyctl secrets list           # View all secrets
flyctl secrets set KEY=VALUE  # Set a secret
flyctl config show            # View fly.toml

# Volumes
flyctl volume list            # View volumes
flyctl volume delete name     # Delete volume

# Domain
flyctl certs list             # View certificates
flyctl certs remove domain    # Remove certificate

# Scale
flyctl scale count 2          # Run 2 instances
flyctl scale memory 512       # Set memory per instance
```

---

## Next Steps

After successful deployment:

1. **Test in production** - Verify all features work
2. **Monitor performance** - Check CPU and memory
3. **Optimize if needed** - See QUICK_OPTIMIZATION_STEPS.md
4. **Add premium features** - See OPTIMIZATION_REVENUE_GUIDE.md
5. **Market your app** - Start acquiring users

---

## Success! 🎉

Your app is now:
- ✅ Live on Fly.io
- ✅ Auto-scaling enabled
- ✅ SSL/HTTPS working
- ✅ Persistent data storage
- ✅ Monitoring active
- ✅ Production ready

**Next:** Follow QUICK_OPTIMIZATION_STEPS.md to reduce CPU costs!

*Last Updated: December 27, 2025*
