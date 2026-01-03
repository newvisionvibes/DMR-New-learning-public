# 🚀 PHASE 1: GITHUB SETUP - STEP BY STEP EXECUTION

**Folder Location:** `C:\fly\DsAnalysis\fly_perplexity`  
**Time Required:** 30 minutes  
**Date:** 29 December 2025, 2:26 PM IST  

---

## ✅ STEP 0: Preparation (5 mins)

### **Task 0.1: Open Command Prompt**
```
Windows Key + R
Type: cmd
Press Enter

OR

Open PowerShell (Right-click Windows → PowerShell)
```

### **Task 0.2: Navigate to Project Folder**
```bash
cd C:\fly\DsAnalysis\fly_perplexity
```

### **Task 0.3: Verify Folder Contents**
```bash
dir
# You should see:
# landing_page.py
# main.py
# cashfree_integration.py
# user_management.py
# admin_panel.py
# requirements.txt
# (and other .py files)
```

---

## ✅ STEP 1: Create .gitignore File (3 mins)

### **Option A: Using Command Line**
```bash
# Create .gitignore (copy content from artifact file)
# From attachment: .gitignore file

# On Windows, create empty file first:
echo. > .gitignore

# Then open in Notepad and paste content from artifact
notepad .gitignore
```

### **Option B: Using VS Code**
```bash
code .gitignore
# Paste content and save
```

### **Verify**
```bash
type .gitignore
# Should show 100+ lines of ignore rules
```

---

## ✅ STEP 2: Create .env.example File (2 mins)

### **Option A: Using Command Line**
```bash
# Windows
echo. > .env.example

# Edit in Notepad
notepad .env.example

# Paste content from artifact file (copy all lines)
```

### **Option B: Using VS Code**
```bash
code .env.example
# Paste and save
```

### **Verify**
```bash
type .env.example
# Should show environment variable template
```

---

## ✅ STEP 3: Verify .env is in .gitignore (2 mins)

**CRITICAL: Prevent accidentally committing secrets**

### **Check .gitignore contains**
```bash
# Search for .env in .gitignore
findstr ".env" .gitignore
# Windows PowerShell:
# Select-String -Path .gitignore -Pattern "\.env"

# Should show:
# .env
# .env.local
# .env.*.local
# .env.production
# !.env.example
```

### **Check you have actual .env file**
```bash
dir | findstr ".env"
# Should see:
# .env (this contains REAL secrets)
# .env.example (this is template)
```

---

## ✅ STEP 4: Create README.md File (2 mins)

### **Option A: Command Line**
```bash
echo. > README.md
notepad README.md
# Paste full content from artifact file
```

### **Option B: VS Code**
```bash
code README.md
# Paste and save
```

### **Verify**
```bash
type README.md | head -20
# Should show heading and features
```

---

## ✅ STEP 5: Verify NO Secrets in Code (3 mins)

**CRITICAL: Double-check before pushing to GitHub**

### **Search for Sandbox Credentials**
```bash
# Search for Cashfree sandbox key
findstr /r "TEST10854952ae8a97c68bc7d5809d7f25945801" *.py
# Windows PowerShell:
# Select-String -Path "*.py" -Pattern "TEST10854952ae8a97c68bc7d5809d7f25945801"

# Should return: NOTHING
# If found anywhere → REMOVE IT!
```

### **Search for Cashfree Secret**
```bash
findstr /r "cfsk_ma_test_" *.py
# Should return: NOTHING
```

### **Search for other credentials**
```bash
findstr /r "password" *.py
findstr /r "SENDGRID" *.py
findstr /r "api_key" *.py

# Should return NOTHING or only variable definitions
# Like: os.getenv('SENDGRID_API_KEY')
```

### **Safe Pattern**
```python
# ✅ GOOD - Uses environment variable
client_id = os.getenv('CASHFREE_CLIENT_ID')

# ❌ BAD - Hardcoded secret
client_id = "TEST10854952ae8a97c68bc7d5809d7f25945801"
```

---

## ✅ STEP 6: Initialize Git Repository (3 mins)

### **Check Git is Installed**
```bash
git --version
# Should show: git version 2.x.x

# If NOT installed: Download from https://git-scm.com
```

### **Initialize Repository**
```bash
git init
# Output: Initialized empty Git repository in C:\fly\DsAnalysis\fly_perplexity\.git\
```

### **Configure Git (First Time Only)**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify
git config --list | findstr user
```

---

## ✅ STEP 7: Stage All Files (2 mins)

### **Add All Files to Staging**
```bash
git add .

# Verify what will be committed
git status
```

### **Expected Output**
```
On branch main

No commits yet

Changes to be committed:
  new file:   .env.example
  new file:   .gitignore
  new file:   README.md
  new file:   landing_page.py
  new file:   main.py
  new file:   cashfree_integration.py
  new file:   user_management.py
  new file:   admin_panel.py
  ... (other files)

Untracked files will not be committed unless you use -f
  .env        ← GOOD! Not included because it's in .gitignore
```

### **Verify .env is NOT Staged**
```bash
git status | findstr ".env"
# Should show ONLY ".env.example" 
# .env should NOT appear anywhere
```

---

## ✅ STEP 8: Create Initial Commit (2 mins)

### **Commit with Message**
```bash
git commit -m "Initial commit: Cashfree payment integration complete"

# Output should show:
# [main (root-commit) abc1234] Initial commit: Cashfree payment integration complete
#  15 files changed, 5432 insertions(+)
#  create mode 100644 .env.example
#  create mode 100644 .gitignore
#  create mode 100644 README.md
#  ... (other files)
```

### **View Commit**
```bash
git log --oneline
# Should show:
# abc1234 Initial commit: Cashfree payment integration complete
```

---

## ✅ STEP 9: Create GitHub Repository (3 mins)

### **Go to GitHub**
```
https://github.com/new
```

### **Fill Form**
```
Repository name: etf-rs-analyzer
Description: Real-time Sector ETF RS Analysis & Subscription Platform
Privacy: Private (or Public - your choice)
✓ Initialize with README → NO (uncheck - we already have one)
✓ Add .gitignore → NO (uncheck - we already have one)
Click: Create repository
```

### **Copy Remote URL**
```
After creation, you'll see:
Quick setup — if you've done this kind of thing before

…or push an existing repository from the command line
git remote add origin https://github.com/YOUR_USERNAME/etf-rs-analyzer.git
git branch -M main
git push -u origin main

Copy the URL: https://github.com/YOUR_USERNAME/etf-rs-analyzer.git
```

---

## ✅ STEP 10: Connect Local Repo to GitHub (3 mins)

### **Add Remote**
```bash
git remote add origin https://github.com/YOUR_USERNAME/etf-rs-analyzer.git

# Replace YOUR_USERNAME with your GitHub username
```

### **Set Main Branch**
```bash
git branch -M main
```

### **Verify Remote**
```bash
git remote -v
# Should show:
# origin  https://github.com/YOUR_USERNAME/etf-rs-analyzer.git (fetch)
# origin  https://github.com/YOUR_USERNAME/etf-rs-analyzer.git (push)
```

---

## ✅ STEP 11: Push to GitHub (5 mins)

### **First Push**
```bash
git push -u origin main

# This may ask for credentials (first time only)
# GitHub will prompt for Personal Access Token
```

### **Generate Personal Access Token (if needed)**

```
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: "Git CLI"
4. Select scopes: repo, workflow
5. Copy the token (shown only once!)
6. Paste when Git asks for password
```

### **Wait for Push**
```
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 8 threads
Compressing objects: 100% (12/12), done.
Writing objects: 100% (15/15), 150 KiB | 1.2 MiB/s
...
To https://github.com/YOUR_USERNAME/etf-rs-analyzer.git
 * [new branch]      main -> main
Branch 'main' set to track remote branch 'main' from 'origin'.
```

---

## ✅ STEP 12: Verify on GitHub (2 mins)

### **Go to Repository**
```
https://github.com/YOUR_USERNAME/etf-rs-analyzer
```

### **Check Files**
- [ ] All .py files visible (landing_page.py, main.py, etc.)
- [ ] .gitignore visible
- [ ] .env.example visible
- [ ] README.md visible and rendered
- [ ] .env NOT visible (good!)

### **Verify README Renders**
- [ ] Heading shows: "📊 D's Sector ETF RS Analyzer"
- [ ] Features section displays
- [ ] Tech Stack table shows
- [ ] Quick Start section visible

---

## ✅ FINAL VERIFICATION

### **Local Check**
```bash
# Verify commit
git log --oneline
# Should show: abc1234 Initial commit: Cashfree payment integration complete

# Verify remote
git remote -v
# Should show origin with your repo URL

# Check status
git status
# Should show: On branch main, working tree clean
```

### **GitHub Check**
```
1. Visit https://github.com/YOUR_USERNAME/etf-rs-analyzer
2. Check Code tab shows all files
3. Check README renders properly
4. Count commits (should be 1)
5. Verify .env is NOT in repo
6. Verify .env.example IS in repo
```

---

## 🎉 SUCCESS INDICATORS

✅ **Local Repository**
- [ ] `.git` folder exists in `C:\fly\DsAnalysis\fly_perplexity`
- [ ] `git log` shows initial commit
- [ ] `git status` shows clean working tree
- [ ] `.env` file exists locally but NOT staged

✅ **GitHub Repository**
- [ ] Repository visible at github.com/YOUR_USERNAME/etf-rs-analyzer
- [ ] All project files visible
- [ ] `.env.example` visible (but NOT `.env`)
- [ ] README.md renders with proper formatting
- [ ] 1 commit shows in commit history

✅ **Security**
- [ ] No secrets in any .py files
- [ ] `.env` excluded by `.gitignore`
- [ ] `.env.example` shows template only
- [ ] Personal access token saved safely

---

## 🚨 TROUBLESHOOTING

### Problem: "fatal: not a git repository"
```bash
# Fix: Initialize git first
git init
git add .
git commit -m "Initial commit"
```

### Problem: ".env file appears in push"
```bash
# Fix: Remove from tracking
git rm --cached .env
git commit -m "Remove .env from tracking"
git push

# Verify in .gitignore:
# .env
# !.env.example
```

### Problem: "remote origin already exists"
```bash
# Fix: Remove old origin
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/etf-rs-analyzer.git
```

### Problem: "permission denied"
```bash
# Fix: Generate Personal Access Token
# 1. https://github.com/settings/tokens
# 2. Create new token with 'repo' scope
# 3. Use token as password when prompted
```

---

## 📋 NEXT STEPS

✅ **PHASE 1 COMPLETE!**

**Now Ready for PHASE 2: Fly.io Deployment**

When you're ready, run these commands for Phase 2:
```bash
# Install Fly CLI
brew install flyctl    # macOS
# OR download from https://fly.io/docs/getting-started/installing-flyctl/

# Login
flyctl auth login

# Deploy
flyctl launch --name etf-rs-analyzer --region blr
```

---

## 📞 NEED HELP?

| Issue | Solution |
|-------|----------|
| Git not installed | Download from https://git-scm.com |
| GitHub token expired | Generate new at https://github.com/settings/tokens |
| Files not pushing | Check `.gitignore` is not blocking them |
| README not rendering | Verify markdown syntax at https://readme.so |
| .env accidentally committed | See "Troubleshooting" section above |

---

**Status:** ✅ PHASE 1 Complete  
**Next:** PHASE 2 - Fly.io Deployment  
**Time Saved:** Deployed with 0 secrets exposed  
**Updated:** 29 December 2025, 2:26 PM IST
