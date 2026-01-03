# 📊 D's Sector ETF RS Analyzer

**Real-time Relative Strength Analysis for Indian Market Sectors & ETFs**  
**Subscription-based SaaS Platform with Cashfree Payment Integration**

![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)
![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-proprietary-red)

---

## 🎯 Features

✅ **Real-time RS Ratings**  
- 21-day, 55-day, and 123-day Relative Strength analysis
- Daily momentum signals with buy/sell recommendations
- Automated alerts and notifications

✅ **Comprehensive Market Coverage**  
- 19 NIFTY sector indices (Auto, Banking, Energy, IT, etc.)
- 35+ Indian ETF tracking across categories
- Real-time price updates and technical indicators

✅ **Subscription Platform**  
- Monthly (₹499) and Annual (₹4,990) plans
- Cashfree payment gateway integration
- Automated email receipts and reports

✅ **Automated Analytics**  
- Daily market analysis emails
- Sector momentum rankings
- ETF relative strength comparisons
- Performance summaries

✅ **Admin Dashboard**  
- User management and analytics
- Payment tracking and analytics
- Manual report generation
- System monitoring

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit 1.28+ |
| **Backend** | Python 3.10+ |
| **Database** | PostgreSQL 12+ |
| **Payment** | Cashfree PG v2025-01-01 |
| **Email** | SendGrid |
| **Deployment** | Fly.io |
| **Version Control** | Git & GitHub |
| **API Version** | Cashfree 2025-01-01 |

---

## 📁 Project Structure

```
etf-rs-analyzer/
├── landing_page.py              # Entry point - registration & payment
├── main.py                      # Dashboard - authenticated access
├── cashfree_integration.py      # Payment gateway wrapper
├── user_management.py           # User & subscription management
├── admin_panel.py               # Admin features & analytics
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
│
├── data/                        # Data files
│   ├── ETFs-List_updated.csv
│   ├── sector_analysis_data.csv
│   └── etf_rs_output.csv
│
├── docs/                        # Documentation
│   ├── CASHFREE_INTEGRATION_GUIDE.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── API_REFERENCE.md
│
├── .env.example                 # Template for environment variables
├── .gitignore                   # Git ignore rules
├── .dockerignore                # Docker ignore rules
├── Procfile                     # Fly.io deployment config
├── fly.toml                     # Fly.io application config
│
├── README.md                    # This file
└── LICENSE                      # Proprietary license
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- PostgreSQL 12 or higher
- Git
- pip (Python package manager)

### Local Development

**1. Clone Repository**
```bash
git clone https://github.com/YOUR_USERNAME/etf-rs-analyzer.git
cd etf-rs-analyzer
```

**2. Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment**
```bash
# Copy template
cp .env.example .env

# Edit .env with your credentials
# CASHFREE_CLIENT_ID=your_sandbox_id
# DATABASE_URL=postgresql://user:pass@localhost/etf_analyzer
# etc.
```

**5. Create Database**
```bash
# Create PostgreSQL database
createdb etf_analyzer

# Initialize tables (from user_management.py)
python user_management.py
```

**6. Run Locally**
```bash
streamlit run landing_page.py
```

**Access at:** `http://localhost:8501`

### Test Credentials (Sandbox)

**Admin Account**
```
Username: admin
Password: admin123
```

**Subscriber Account**
```
Username: dmr1
Password: dmr123
```

**Test Card (Cashfree Sandbox)**
```
Card: 1111 1111 1111 1111
Expiry: 12/30
CVV: 123
OTP: 123456
```

---

## 📋 Configuration

### Environment Variables (.env)

Required variables:

```env
# Cashfree Sandbox (Testing)
CASHFREE_CLIENT_ID=TEST_XXXXXXXXXXXXXXXXXXXXXX
CASHFREE_CLIENT_SECRET=cfsk_ma_test_XXXXXXXXXXXXXXXXXXXXXX

# Cashfree Production (Live)
CASHFREE_PROD_CLIENT_ID=PROD_XXXXXXXXXXXXXXXXXXXXXX
CASHFREE_PROD_CLIENT_SECRET=cfsk_ma_live_XXXXXXXXXXXXXXXXXXXXXX

# Database
DATABASE_URL=postgresql://user:password@localhost/etf_analyzer

# Email
SENDGRID_API_KEY=XXXXXXXXXXXXXXXXXXXXXX
SENDER_EMAIL=noreply@example.com

# Environment
ENVIRONMENT=sandbox  # or 'production'
DEBUG=false

# Webhook
CASHFREE_WEBHOOK_SECRET=XXXXXXXXXXXXXXXXXXXXXX
```

**⚠️ NEVER commit .env file!** Use `.env.example` as template.

---

## 🔄 Payment Flow

```
1. User Registration
   └─ Email, Username, Password, Plan Selection

2. Create Cashfree Payment Session
   └─ API Call → Generate payment_session_id

3. Checkout Page
   └─ JS SDK loads Cashfree payment form

4. Payment Entry
   └─ Card/UPI/Net Banking payment

5. Webhook Notification
   └─ Cashfree confirms payment

6. Subscription Activation
   └─ Mark subscription as ACTIVE

7. Dashboard Access
   └─ User can login and view RS analysis
```

---

## 🌐 Deployment

### Fly.io Deployment

See [DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md) for complete instructions.

**Quick Deploy:**
```bash
# Install Fly CLI
brew install flyctl

# Login
flyctl auth login

# Deploy
flyctl launch --name etf-rs-analyzer --region blr
flyctl secrets set CASHFREE_CLIENT_ID=XXXXX
flyctl deploy
```

**Live App:** https://etf-rs-analyzer.fly.dev

---

## 📊 API Endpoints

### Public Endpoints
- `GET /` - Landing page
- `POST /register` - User registration
- `POST /login` - User login

### Authenticated Endpoints
- `GET /dashboard` - Main dashboard
- `GET /api/rs-ratings` - Fetch RS data
- `GET /api/sectors` - Sector analysis
- `GET /api/etfs` - ETF analysis

### Admin Endpoints
- `GET /admin` - Admin dashboard
- `GET /admin/users` - User management
- `GET /admin/payments` - Payment analytics

### Webhook Endpoints
- `POST /webhooks/cashfree` - Payment confirmation

---

## 🧪 Testing

### Sandbox Testing
```bash
# Test registration & payment
1. Go to http://localhost:8501
2. Click "New User Sign Up"
3. Fill form with test data
4. Select Monthly Plan (₹499)
5. Use test card: 1111 1111 1111 1111
6. Complete payment
```

### Production Testing
```bash
# After deployment to Fly.io
1. Go to https://etf-rs-analyzer.fly.dev
2. Repeat above steps
3. Verify order in Cashfree PRODUCTION dashboard
4. Check email receipt (SendGrid)
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [CASHFREE_INTEGRATION_GUIDE.md](./docs/CASHFREE_INTEGRATION_GUIDE.md) | Complete Cashfree setup & troubleshooting |
| [DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md) | GitHub, Fly.io, and production setup |
| [API_REFERENCE.md](./docs/API_REFERENCE.md) | Complete API documentation |
| [QUICK_START_CHECKLIST.md](./docs/QUICK_START_CHECKLIST.md) | Fast deployment reference |

---

## 🐛 Troubleshooting

### Common Issues

**Cashfree module not found**
```bash
pip install -r requirements.txt
streamlit run landing_page.py
```

**Database connection error**
```bash
# Verify DATABASE_URL in .env
# Check PostgreSQL is running
psql -U user -d etf_analyzer -c "SELECT 1"
```

**Payment not processing**
```bash
# Check Cashfree credentials
# Verify ENVIRONMENT variable
# Check logs: streamlit run landing_page.py 2>&1 | tee debug.log
```

See full troubleshooting guide: [DEPLOYMENT_GUIDE.md - Section 5](./docs/DEPLOYMENT_GUIDE.md)

---

## 🔐 Security

- ✅ All secrets stored in environment variables
- ✅ No hardcoded credentials in code
- ✅ HTTPS enforced in production
- ✅ SQL injection prevention (parameterized queries)
- ✅ CSRF protection enabled
- ✅ Password hashing (bcrypt)
- ✅ Webhook signature verification

---

## 📧 Support & Contact

- **Email:** support@example.com
- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/etf-rs-analyzer/issues)
- **Documentation:** See [docs/](./docs/) folder

---

## 📄 License

Proprietary - D's Analysis Team  
Unauthorized copying or distribution prohibited.

---

## 👥 Contributors

- **D's Analysis Team**
- **Development Partner:** Perplexity AI

---

## 📈 Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Advanced portfolio analytics
- [ ] Machine learning predictions
- [ ] API marketplace integration
- [ ] White-label solution
- [ ] Multi-currency support

---

## 🎯 Version History

| Version | Date | Status | Changes |
|---------|------|--------|---------|
| 2.0 | 29 Dec 2025 | Production Ready | Cashfree integration complete, Fly.io ready |
| 1.5 | 28 Dec 2025 | Stable | Payment flow tested, webhooks configured |
| 1.0 | 22 Dec 2025 | Initial | Core analytics engine |

---

## ⚡ Getting Started in 3 Steps

```bash
# 1. Clone & setup
git clone https://github.com/YOUR_USERNAME/etf-rs-analyzer.git
cd etf-rs-analyzer
cp .env.example .env

# 2. Install & run
pip install -r requirements.txt
streamlit run landing_page.py

# 3. Open browser
# http://localhost:8501
```

---

**Made with ❤️ by D's Analysis Team**  
**Last Updated:** 29 December 2025  
**Status:** ✅ Production Ready
