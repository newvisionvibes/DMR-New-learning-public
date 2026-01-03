# 🤖 COMPLETE TEST AUTOMATION GUIDE FOR YOUR CHECKLIST

## Executive Summary

**YES - 65-70% of your checklist CAN be automated!**

| Category | Can Automate | % Automated |
|----------|---|---|
| Environment Checks | ✅ YES | 90% |
| Authentication | ✅ YES | 85% |
| Data Consistency | ✅ YES | 95% |
| API Integration | ✅ YES | 90% |
| Performance Tests | ✅ YES | 100% |
| Database Checks | ✅ YES | 95% |
| Security Basics | ✅ YES | 70% |
| UI/UX Testing | ⚠️ PARTIAL | 60% |
| Browser Compatibility | ✅ YES | 80% |
| Accessibility | ⚠️ PARTIAL | 50% |
| **TOTAL AUTOMATION** | **✅ 65-70%** | **Saves 20+ hours** |

---

## 🎯 WHAT CAN & CANNOT BE AUTOMATED

### ✅ FULLY AUTOMATABLE (Will implement)

```
✅ Environment variable validation
✅ Database connectivity tests
✅ CSV file integrity checks
✅ ETF count validation (34 always)
✅ Sector count validation (19 always)
✅ API response validation
✅ Password hashing verification
✅ Login/logout flows
✅ Data refresh consistency (10x consecutive)
✅ Cooldown timer accuracy (60 seconds ± 1)
✅ Response time benchmarks
✅ Memory leak detection
✅ SQL injection prevention
✅ Rate limiting verification
✅ File encoding UTF-8 check
```

### ⚠️ PARTIALLY AUTOMATABLE (Hybrid approach)

```
⚠️ Error message clarity (automated for consistency, manual for UX)
⚠️ UI rendering (automated screenshots, manual visual review)
⚠️ Email template rendering (automated for structure, manual for layout)
⚠️ Mobile responsiveness (automated for breakpoints, manual for user experience)
⚠️ Color contrast (automated with WCAG analyzer)
⚠️ Keyboard navigation (automated for tab order, manual for user flow)
```

### ❌ CANNOT AUTOMATE (Manual only)

```
❌ Design aesthetics
❌ User experience feel
❌ Content copy clarity
❌ Visual consistency subjective judgments
❌ Accessibility subjective testing
❌ User satisfaction surveys
❌ Sign-off approvals
```

---

## 📁 AUTOMATION ARCHITECTURE

```
your-app/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                          # Pytest configuration
│   ├── unit/
│   │   ├── test_auth.py                     # Login/logout/validation
│   │   ├── test_data_consistency.py         # ETF/sector counts
│   │   ├── test_database.py                 # DB connectivity
│   │   ├── test_api.py                      # API integration
│   │   ├── test_security.py                 # SQL injection, XSS
│   │   └── test_validation.py               # Input validation
│   │
│   ├── integration/
│   │   ├── test_end_to_end.py              # Full workflows
│   │   ├── test_data_flow.py                # Data through system
│   │   └── test_email_dispatch.py           # Email generation
│   │
│   ├── ui/
│   │   ├── test_login_ui.py                 # Selenium tests
│   │   ├── test_admin_dashboard.py          # Admin UI
│   │   └── test_subscriber_view.py          # Subscriber UI
│   │
│   ├── performance/
│   │   ├── test_load.py                     # 50 concurrent users
│   │   ├── test_response_time.py            # <3 second pages
│   │   └── test_memory_leak.py              # 24-hour uptime
│   │
│   ├── fixtures/
│   │   ├── test_data.py                     # Test datasets
│   │   ├── users.py                         # Test users
│   │   └── database.py                      # Test DB setup
│   │
│   └── reports/
│       ├── coverage/
│       ├── html/
│       └── junit.xml
│
├── .github/
│   └── workflows/
│       ├── test.yml                         # Run tests on commit
│       ├── daily_full_test.yml              # Nightly full test
│       └── performance_test.yml             # Weekly perf test
│
└── scripts/
    ├── run_all_tests.sh                     # Master test script
    ├── run_unit_tests.sh                    # Unit tests only
    ├── run_ui_tests.sh                      # Selenium tests
    ├── run_performance_tests.sh             # Load testing
    └── generate_test_report.py              # HTML report
```

---

## 🔧 SETUP INSTRUCTIONS

### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install testing libraries
pip install pytest>=7.0
pip install pytest-cov>=4.0
pip install pytest-xdist>=3.0
pip install requests>=2.28
pip install selenium>=4.0
pip install locust>=2.0
pip install psycopg2-binary>=2.9
pip install python-dotenv>=0.20
pip install pytest-timeout>=2.1
pip install responses>=0.22
```

### Step 2: Create Fixtures

```bash
# Create test database
createdb etf_test_db
# Load test data
psql etf_test_db < tests/fixtures/test_data.sql
```

### Step 3: Configure Environment

```bash
# Create .env.test file
cat > .env.test << 'EOF'
ENVIRONMENT=test
DATABASE_URL=postgresql://user:pass@localhost:5432/etf_test_db
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_CLIENT_TOOLBARPOSITION=hidden
API_URL=http://localhost:5000
PYTHONDONTWRITEBYTECODE=1
EOF
```

---

## 🧪 TEST TEMPLATES (COPY-PASTE READY)

### Template 1: Data Consistency Tests

```python
# tests/unit/test_data_consistency.py

import pytest
import pandas as pd
from datetime import datetime
from pathlib import Path

class TestDataConsistency:
    """Test data integrity and consistency across refreshes"""
    
    @pytest.fixture
    def etf_data(self):
        """Load ETF data"""
        csv_path = Path("etf_rs_output.csv")
        return pd.read_csv(csv_path)
    
    def test_etf_count_is_34(self, etf_data):
        """CRITICAL: ETF count must ALWAYS be 34"""
        assert len(etf_data) == 34, f"Expected 34 ETFs, got {len(etf_data)}"
    
    def test_sector_count_is_19(self):
        """CRITICAL: Sector count must ALWAYS be 19"""
        csv_path = Path("sector_analysis_data.csv")
        sector_data = pd.read_csv(csv_path)
        assert len(sector_data) == 19, f"Expected 19 sectors, got {len(sector_data)}"
    
    def test_no_nan_values_in_etf(self, etf_data):
        """No NaN values allowed in ETF data"""
        nan_columns = etf_data.columns[etf_data.isna().any()].tolist()
        assert len(nan_columns) == 0, f"Found NaN in columns: {nan_columns}"
    
    def test_csv_encoding_is_utf8(self):
        """All CSV files must be UTF-8 encoded"""
        csv_files = ["etf_rs_output.csv", "sector_analysis_data.csv"]
        for csv_file in csv_files:
            with open(csv_file, 'rb') as f:
                raw = f.read()
                try:
                    raw.decode('utf-8')
                except UnicodeDecodeError:
                    pytest.fail(f"{csv_file} is not UTF-8 encoded")
    
    def test_csv_headers_valid(self, etf_data):
        """CSV must have expected headers"""
        expected_headers = ['Symbol', 'Sector', 'LTP', 'Change%', 'RS', 'Category', 'TLDR']
        for header in expected_headers:
            assert header in etf_data.columns, f"Missing header: {header}"
    
    @pytest.mark.parametrize("iteration", range(1, 11))
    def test_refresh_10_times_consistency(self, iteration, etf_data):
        """
        CRITICAL TEST: Refresh data 10 times
        Each refresh must return identical count (34)
        """
        # Simulate refresh (in real test, call actual refresh API)
        from your_app.etf_rs_calculator import refresh_etf_data
        
        refreshed_data = refresh_etf_data()
        assert len(refreshed_data) == 34, \
            f"Iteration {iteration}: Expected 34 ETFs, got {len(refreshed_data)}"
```

### Template 2: Authentication Tests

```python
# tests/unit/test_auth.py

import pytest
from datetime import datetime
from your_app.auth import validate_password, hash_password, verify_password

class TestAuthentication:
    """Test authentication and security"""
    
    def test_login_success(self, test_client):
        """Successful login returns 200 and token"""
        response = test_client.post('/login', json={
            'username': 'admin',
            'password': 'testpass123'
        })
        assert response.status_code == 200
        assert 'token' in response.json
    
    def test_login_wrong_password(self, test_client):
        """Wrong password returns 401"""
        response = test_client.post('/login', json={
            'username': 'admin',
            'password': 'wrongpass'
        })
        assert response.status_code == 401
    
    def test_password_hashing(self):
        """Passwords must be hashed, not plain text"""
        plain_password = "MySecurePass123"
        hashed = hash_password(plain_password)
        
        # Hash should not contain plain password
        assert plain_password not in hashed
        assert verify_password(plain_password, hashed)
        assert not verify_password("WrongPass", hashed)
    
    def test_password_strength(self):
        """Password must be strong (min 8 chars, uppercase, number, special)"""
        weak_passwords = ["pass", "password", "12345678", "abcdefgh"]
        for weak_pass in weak_passwords:
            is_strong = validate_password(weak_pass)
            assert not is_strong, f"Weak password accepted: {weak_pass}"
    
    @pytest.mark.timeout(2)
    def test_rate_limiting_login_attempts(self, test_client):
        """Max 5 login attempts per minute"""
        for attempt in range(6):
            response = test_client.post('/login', json={
                'username': 'admin',
                'password': 'wrong'
            })
            if attempt < 5:
                assert response.status_code == 401
            else:
                assert response.status_code == 429, "Rate limit not applied"
```

### Template 3: Database Tests

```python
# tests/unit/test_database.py

import pytest
import psycopg2
from your_app.db import get_db_connection

class TestDatabase:
    """Test database connectivity and integrity"""
    
    def test_database_connection(self):
        """Database must be accessible"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            assert cursor.fetchone()[0] == 1
            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            pytest.fail(f"Database connection failed: {e}")
    
    def test_required_tables_exist(self):
        """All required tables must exist"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        required_tables = ['users', 'subscriptions', 'etf_analysis', 'sector_analysis']
        for table in required_tables:
            cursor.execute(f"SELECT 1 FROM {table} LIMIT 1")
            assert cursor.fetchone() is not None, f"Table {table} not found"
        
        cursor.close()
        conn.close()
    
    def test_user_record_count(self):
        """At least 1 admin, 3 subscribers"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
        admin_count = cursor.fetchone()[0]
        assert admin_count >= 1, "Must have at least 1 admin"
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='subscriber'")
        sub_count = cursor.fetchone()[0]
        assert sub_count >= 3, "Must have at least 3 subscribers"
        
        cursor.close()
        conn.close()
```

### Template 4: API Integration Tests

```python
# tests/unit/test_api.py

import pytest
import responses
import requests
from your_app.api_connector import fetch_etf_data

class TestAPIIntegration:
    """Test API connectivity and data validation"""
    
    @responses.activate
    def test_api_success_response(self):
        """API returns valid ETF data"""
        responses.add(
            responses.GET,
            'https://api.example.com/etf/data',
            json={'etfs': [{'symbol': 'NIFTYBEES', 'price': 65.5}]},
            status=200
        )
        
        data = fetch_etf_data()
        assert len(data) > 0
        assert 'symbol' in data[0]
    
    @responses.activate
    def test_api_timeout_handling(self):
        """API timeout should be handled gracefully"""
        responses.add(
            responses.GET,
            'https://api.example.com/etf/data',
            body=requests.Timeout()
        )
        
        from your_app.api_connector import fetch_etf_data_with_retry
        data = fetch_etf_data_with_retry(timeout=5, retries=3)
        
        # Should return cached data or empty, not crash
        assert data is not None
    
    @responses.activate
    def test_api_rate_limit_handling(self):
        """API 429 (too many requests) should retry"""
        # First 2 calls fail with 429
        responses.add(responses.GET, 'https://api.example.com/etf/data', status=429)
        responses.add(responses.GET, 'https://api.example.com/etf/data', status=429)
        # 3rd call succeeds
        responses.add(
            responses.GET,
            'https://api.example.com/etf/data',
            json={'etfs': [{'symbol': 'NIFTYBEES'}]},
            status=200
        )
        
        from your_app.api_connector import fetch_etf_data_with_retry
        data = fetch_etf_data_with_retry(retries=3)
        assert data is not None
```

### Template 5: Performance Tests

```python
# tests/performance/test_performance.py

import pytest
import time
from locust import HttpUser, task, between

class TestPerformance:
    """Test performance under load"""
    
    def test_page_load_time_under_3_seconds(self, test_client):
        """All pages must load in <3 seconds"""
        start = time.time()
        response = test_client.get('/')
        duration = time.time() - start
        
        assert duration < 3.0, f"Page load took {duration:.2f}s (max 3s)"
        assert response.status_code == 200
    
    def test_concurrent_users_50(self):
        """System must handle 50 concurrent subscribers"""
        import threading
        import requests
        
        errors = []
        
        def simulate_user():
            try:
                response = requests.get('http://localhost:8501/', timeout=10)
                assert response.status_code == 200
            except Exception as e:
                errors.append(str(e))
        
        threads = []
        for i in range(50):
            t = threading.Thread(target=simulate_user)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        assert len(errors) == 0, f"Concurrent users failed: {errors}"
    
    def test_memory_no_leak(self, test_client):
        """No memory leaks over repeated operations"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_mem = process.memory_info().rss / 1024 / 1024  # MB
        
        # Perform 100 operations
        for _ in range(100):
            test_client.get('/api/etf/data')
        
        final_mem = process.memory_info().rss / 1024 / 1024
        increase = final_mem - initial_mem
        
        # Memory should not increase by >50MB
        assert increase < 50, f"Memory leak detected: {increase:.2f}MB increase"
```

### Template 6: Security Tests

```python
# tests/unit/test_security.py

import pytest
from your_app.security import sanitize_input, validate_input

class TestSecurity:
    """Test security vulnerabilities"""
    
    def test_sql_injection_prevention(self):
        """SQL injection attempts should be blocked"""
        malicious = "admin'; DROP TABLE users; --"
        sanitized = sanitize_input(malicious)
        
        # Dangerous characters should be escaped
        assert "DROP" not in sanitized or "DROP" not in sanitized.upper()
    
    def test_xss_prevention(self):
        """XSS payload should be escaped"""
        xss_payload = "<script>alert('hacked')</script>"
        sanitized = sanitize_input(xss_payload)
        
        # Script tags should be escaped
        assert "<script>" not in sanitized
    
    def test_input_validation_required_fields(self):
        """Required fields cannot be empty"""
        invalid_inputs = [
            {'username': '', 'password': 'test'},
            {'username': 'admin', 'password': ''},
            {'username': None, 'password': 'test'},
        ]
        
        for invalid in invalid_inputs:
            is_valid = validate_input(invalid)
            assert not is_valid, f"Invalid input accepted: {invalid}"
    
    def test_no_sensitive_data_in_logs(self):
        """Passwords/tokens should not be in logs"""
        import logging
        from io import StringIO
        
        log_capture = StringIO()
        handler = logging.StreamHandler(log_capture)
        logger = logging.getLogger('your_app')
        logger.addHandler(handler)
        
        logger.info("User password123 logged in")
        
        log_contents = log_capture.getvalue()
        assert "password123" not in log_contents
```

---

## ▶️ HOW TO RUN TESTS

### Run All Tests
```bash
pytest tests/ -v --cov=your_app --cov-report=html
```

### Run Specific Category
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Performance tests only
pytest tests/performance/ -v

# UI tests only
pytest tests/ui/ -v
```

### Run With Timeout
```bash
pytest tests/ --timeout=60 -v
```

### Run In Parallel
```bash
pytest tests/ -n auto -v
```

### Generate HTML Report
```bash
pytest tests/ --html=report.html --self-contained-html
```

---

## 🔄 CI/CD AUTOMATION (GitHub Actions)

### `.github/workflows/test.yml`

```yaml
name: Run Tests on Commit

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_DB: etf_test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-xdist
    
    - name: Create test environment
      env:
        DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/etf_test_db
      run: |
        psql -h localhost -U test_user -d etf_test_db -f tests/fixtures/test_data.sql
    
    - name: Run Unit Tests
      env:
        DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/etf_test_db
      run: |
        pytest tests/unit/ -v --cov=your_app --cov-report=xml
    
    - name: Run Integration Tests
      env:
        DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/etf_test_db
      run: |
        pytest tests/integration/ -v
    
    - name: Upload Coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
    
    - name: Comment PR with Coverage
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const coverage = fs.readFileSync('coverage.xml', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: '✅ Tests passed! Coverage report attached.'
          })
```

### `.github/workflows/performance_test.yml`

```yaml
name: Weekly Performance Test

on:
  schedule:
    # Run every Monday at 2 AM
    - cron: '0 2 * * 1'

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install locust pytest
    
    - name: Run Load Test
      run: |
        pytest tests/performance/ -v --timeout=3600
    
    - name: Generate Report
      if: always()
      run: |
        python scripts/generate_test_report.py
    
    - name: Upload Report
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: performance-report
        path: tests/reports/
```

---

## 📊 TEST EXECUTION MATRIX

```
AUTOMATED TEST EXECUTION PLAN
═══════════════════════════════════════════════════════════════

Phase 1: On Every Commit (5 minutes)
  ✅ Unit Tests
     - Authentication (login/logout)
     - Data validation
     - Input sanitization
     - CSV integrity
     - ETF count (34)
     - Sector count (19)

Phase 2: On Every PR (10 minutes)
  ✅ Unit Tests (as above)
  ✅ Integration Tests
     - End-to-end login flow
     - Admin → analyze → email
     - Data refresh flow
     - Database integrity

Phase 3: Daily (20 minutes)
  ✅ Full Unit + Integration
  ✅ UI Tests (Selenium)
     - Login UI
     - Admin dashboard
     - Subscriber view
     - Mobile responsive
  ✅ Security Scan
     - SQL injection tests
     - XSS prevention
     - CSRF prevention

Phase 4: Weekly (60 minutes)
  ✅ All above
  ✅ Performance Tests
     - 50 concurrent users
     - Page load <3s
     - Memory leak check
     - 1-hour sustained test

Phase 5: Monthly (120 minutes)
  ✅ All above
  ✅ Accessibility Tests
     - WCAG AA compliance
     - Keyboard navigation
     - Screen reader compat
  ✅ Browser Compatibility
     - Chrome latest
     - Firefox latest
     - Safari latest
     - Edge latest
```

---

## ⏱️ TIME SAVINGS CALCULATION

| Activity | Manual Time | Automated Time | Saved |
|----------|---|---|---|
| Unit tests | 2 hours | 2 minutes | 1:58 |
| Integration tests | 1.5 hours | 1 minute | 1:29 |
| Data consistency | 1 hour | 30 seconds | 0:59 |
| Performance test | 2 hours | 5 minutes | 1:55 |
| Security checks | 1.5 hours | 2 minutes | 1:28 |
| Browser compat | 1 hour | 5 minutes | 0:55 |
| **TOTAL** | **9 hours** | **15 minutes** | **8:45 saved** |

**PER WEEK: 8.75 hours saved (more than 1 working day!)**

---

## 🎯 IMPLEMENTATION ROADMAP

### Week 1: Foundation
- [ ] Set up pytest framework
- [ ] Create fixtures and test data
- [ ] Write unit tests (Templates 1-4)
- [ ] Get 80% code coverage

### Week 2: Integration & Automation
- [ ] Write integration tests
- [ ] Set up GitHub Actions
- [ ] Configure CI/CD pipeline
- [ ] Test on sample PR

### Week 3: Performance & UI
- [ ] Write performance tests
- [ ] Set up Selenium tests
- [ ] Load testing with Locust
- [ ] Weekly schedule setup

### Week 4: Refinement & Documentation
- [ ] Fix failing tests
- [ ] Add edge case tests
- [ ] Documentation
- [ ] Team training

---

## 🚀 QUICK START SCRIPT

Create `run_all_tests.sh`:

```bash
#!/bin/bash

echo "═══════════════════════════════════════════════"
echo "ETF App - Comprehensive Test Suite"
echo "═══════════════════════════════════════════════"

# Activate virtual environment
source test_env/bin/activate

# Install dependencies
pip install -r requirements.txt -q

# Run tests
echo "📋 Running Unit Tests..."
pytest tests/unit/ -v --tb=short

echo "📋 Running Integration Tests..."
pytest tests/integration/ -v --tb=short

echo "📋 Running Performance Tests..."
pytest tests/performance/ -v --timeout=300

echo "📋 Generating Coverage Report..."
pytest tests/ --cov=your_app --cov-report=html --cov-report=term-missing

echo "✅ All tests completed!"
echo "📊 Coverage report: htmlcov/index.html"
```

Make it executable:
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

---

## ✅ NEXT STEPS

1. **Today:**
   - [ ] Copy Template 1 (Data Consistency)
   - [ ] Run pytest
   - [ ] See tests pass/fail

2. **Tomorrow:**
   - [ ] Copy Templates 2-4
   - [ ] Create GitHub Actions workflow
   - [ ] Test on next commit

3. **This Week:**
   - [ ] Complete all templates
   - [ ] Set up CI/CD
   - [ ] Generate first report

4. **Next Week:**
   - [ ] Performance tests
   - [ ] Browser automation
   - [ ] Team training

---

## 📞 COMMON ISSUES & FIXES

### Issue: Tests fail with database connection error
**Fix:** Ensure Postgres is running and `DATABASE_URL` is set correctly
```bash
psql -U postgres -c "SELECT version();"
```

### Issue: Pytest not found
**Fix:** Install in active virtual environment
```bash
pip install pytest --upgrade
```

### Issue: Selenium tests fail
**Fix:** Download matching ChromeDriver
```bash
# macOS
brew install chromedriver

# Ubuntu
sudo apt-get install chromium-chromedriver
```

### Issue: CI/CD tests pass locally but fail on GitHub
**Fix:** Check environment variables in GitHub secrets
```bash
Settings → Secrets and Variables → Actions
```

---

**Status:** ✅ READY TO IMPLEMENT

**Files Provided:**
1. ✅ Full automation guide (this file)
2. ✅ 6 test templates (copy-paste ready)
3. ✅ CI/CD configurations
4. ✅ Run scripts

**Next Action:** Pick Template 1, copy code, run `pytest tests/`

---

**Version:** 1.0 Automation Framework
**Date:** 2025-12-30 17:35 IST
**Time to Implement:** 2-3 weeks
**Time Saved Per Week:** 8-9 hours
**Automation Coverage:** 65-70%
