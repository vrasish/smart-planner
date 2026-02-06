# 🚀 Step-by-Step Deployment Guide

Follow these steps in order to deploy your Smart Planner application.

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:
- [ ] A GitHub account
- [ ] Your code committed to a GitHub repository (or ready to commit)
- [ ] A Vercel account (free) - sign up at https://vercel.com
- [ ] A Railway account (free trial) - sign up at https://railway.app

---

## PART 1: Deploy Frontend to Vercel

### Step 1.1: Install Vercel CLI

Open Terminal and run:
```bash
npm install -g vercel
```

If you don't have Node.js/npm, install it first from https://nodejs.org

### Step 1.2: Login to Vercel

```bash
vercel login
```

This will open a browser window. Sign in with your GitHub account.

### Step 1.3: Navigate to Project Directory

```bash
cd /Applications/XAMPP/xamppfiles/htdocs/smartplanner
```

### Step 1.4: Initialize Vercel Project

```bash
vercel
```

You'll be asked several questions:
- **Set up and deploy?** → Type `Y` and press Enter
- **Which scope?** → Select your account (usually just press Enter)
- **Link to existing project?** → Type `N` and press Enter
- **What's your project's name?** → Type `smart-planner` (or any name)
- **In which directory is your code located?** → Press Enter (current directory)
- **Want to override the settings?** → Type `N` and press Enter

### Step 1.5: Deploy to Production

```bash
vercel --prod
```

**✅ You'll get a URL like:** `https://smart-planner-xxxxx.vercel.app`

**📝 SAVE THIS URL** - You'll need it later!

---

## PART 2: Deploy Backend to Railway

### Step 2.1: Create GitHub Repository (if not done)

1. Go to https://github.com
2. Click "New repository"
3. Name it: `smart-planner`
4. Make it **Public** (or Private if you have GitHub Pro)
5. Click "Create repository"

### Step 2.2: Push Code to GitHub

In Terminal, run:
```bash
cd /Applications/XAMPP/xamppfiles/htdocs/smartplanner

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Smart Planner"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/smart-planner.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2.3: Sign Up for Railway

1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with **GitHub** (recommended)
4. Authorize Railway to access your GitHub

### Step 2.4: Create New Project on Railway

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Find and select your `smart-planner` repository
4. Click **"Deploy Now"**

Railway will start deploying your project automatically.

### Step 2.5: Add MySQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"**
3. Select **"MySQL"**
4. Railway will create a MySQL database for you

### Step 2.6: Get Database Credentials

1. Click on the **MySQL service** you just created
2. Go to the **"Variables"** tab
3. You'll see these variables:
   - `MYSQLHOST`
   - `MYSQLPORT`
   - `MYSQLDATABASE`
   - `MYSQLUSER`
   - `MYSQLPASSWORD`

**📝 COPY THESE VALUES** - You'll need them in the next step!

### Step 2.7: Configure Backend Environment Variables

1. Click on your **backend service** (the one with your code, not MySQL)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add these variables one by one:

   ```
   DB_HOST = <value from MYSQLHOST>
   DB_PORT = 3306
   DB_NAME = <value from MYSQLDATABASE>
   DB_USER = <value from MYSQLUSER>
   DB_PASSWORD = <value from MYSQLPASSWORD>
   ALLOWED_ORIGINS = https://your-vercel-url.vercel.app
   PORT = 8000
   ```

   **Important:** Replace `https://your-vercel-url.vercel.app` with your actual Vercel URL from Step 1.5!

5. After adding all variables, Railway will automatically redeploy

### Step 2.8: Get Backend URL

1. In your backend service, go to **"Settings"**
2. Scroll down to **"Generate Domain"**
3. Click **"Generate Domain"**
4. You'll get a URL like: `https://smart-planner-production.up.railway.app`

**📝 SAVE THIS URL** - You need it for the frontend!

### Step 2.9: Wait for Deployment

- Railway will show "Deploying..." status
- Wait until it shows "Active" (usually 2-3 minutes)
- Check the **"Logs"** tab if there are any errors

---

## PART 3: Setup Database

### Step 3.1: Connect to Railway MySQL

You have two options:

**Option A: Using Railway CLI (Recommended)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Connect to MySQL
railway connect mysql
```

**Option B: Using Railway Dashboard**
1. Go to your MySQL service
2. Click **"Connect"** tab
3. Copy the connection string
4. Use a MySQL client (like DBeaver) to connect

### Step 3.2: Run Database Setup

**If using Railway CLI:**
```bash
# Set environment variables locally
export DB_HOST=<your-mysql-host>
export DB_PORT=3306
export DB_NAME=<your-db-name>
export DB_USER=<your-db-user>
export DB_PASSWORD=<your-db-password>

# Run setup scripts
python setup_users.py
python setup_extended_features.py
```

**If using MySQL client:**
1. Open the SQL file: `setup.sql`
2. Copy the SQL commands
3. Run them in your MySQL client
4. Then run the Python scripts via Railway CLI or locally with env vars set

---

## PART 4: Connect Frontend to Backend

### Step 4.1: Update config.js

1. Open `config.js` in your project
2. Update the API_BASE URL:

```javascript
const API_BASE = 'https://your-railway-backend-url.railway.app';
```

Replace `your-railway-backend-url.railway.app` with your actual Railway URL from Step 2.8.

### Step 4.2: Commit and Push Changes

```bash
git add config.js
git commit -m "Update API URL for production"
git push
```

### Step 4.3: Redeploy Frontend

```bash
vercel --prod
```

Or Vercel will auto-deploy if you connected it to GitHub.

---

## PART 5: Test Your Deployment

### Step 5.1: Test Backend API

1. Open your browser
2. Go to: `https://your-backend-url.railway.app/docs`
3. You should see the Swagger API documentation
4. If you see it, your backend is working! ✅

### Step 5.2: Test Frontend

1. Go to your Vercel URL: `https://your-app.vercel.app`
2. You should see the login page
3. Try logging in with:
   - Username: `admin`
   - Password: `admin123.`

### Step 5.3: Test Full Flow

1. **Login** - Should work
2. **Add a task** - Fill the form and submit
3. **Generate plan** - Click "Generate Smart Plan"
4. **View calendar** - Click "📅 Calendar"
5. **Check notifications** - Click "🔔 Notifications"

If all these work, **🎉 CONGRATULATIONS! Your app is live!**

---

## 🔧 Troubleshooting

### Backend Not Working?

1. **Check Railway Logs:**
   - Go to Railway → Your service → Logs
   - Look for error messages

2. **Check Environment Variables:**
   - Make sure all DB_* variables are set correctly
   - Verify ALLOWED_ORIGINS matches your Vercel URL

3. **Check Database Connection:**
   - Verify MySQL service is running
   - Check database credentials are correct

### Frontend Can't Connect to Backend?

1. **Check config.js:**
   - Make sure API_BASE has the correct Railway URL
   - Should be `https://` not `http://`

2. **Check CORS:**
   - Verify ALLOWED_ORIGINS in Railway includes your Vercel URL
   - Should be exactly: `https://your-app.vercel.app`

3. **Check Browser Console:**
   - Open browser DevTools (F12)
   - Go to Console tab
   - Look for error messages

### Database Errors?

1. **Verify Tables Exist:**
   - Connect to MySQL
   - Run: `SHOW TABLES;`
   - Should show: users, tasks, daily_plan, categories, notifications

2. **Run Setup Scripts Again:**
   ```bash
   python setup_users.py
   python setup_extended_features.py
   ```

---

## ✅ Deployment Checklist

Before considering deployment complete:

- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Railway
- [ ] MySQL database created
- [ ] Environment variables set in Railway
- [ ] Database tables created
- [ ] config.js updated with backend URL
- [ ] Frontend redeployed with new config
- [ ] Backend API accessible at /docs
- [ ] Frontend accessible and shows login
- [ ] Can login successfully
- [ ] Can add tasks
- [ ] Can generate plan
- [ ] Calendar view works
- [ ] Notifications work

---

## 📞 Need Help?

If you get stuck:

1. **Check the logs:**
   - Railway: Service → Logs
   - Vercel: Project → Deployments → Click deployment → View logs

2. **Common Issues:**
   - CORS errors → Check ALLOWED_ORIGINS
   - Database errors → Check environment variables
   - 404 errors → Check URLs are correct

3. **Railway Support:** https://docs.railway.app
4. **Vercel Support:** https://vercel.com/docs

---

## 🎉 Success!

Once everything is working, share your app URL with others!

**Frontend:** `https://your-app.vercel.app`  
**Backend API:** `https://your-backend.railway.app`  
**API Docs:** `https://your-backend.railway.app/docs`

---

**Good luck with your deployment! 🚀**
