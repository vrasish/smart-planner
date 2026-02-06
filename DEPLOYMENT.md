# 🚀 Smart Planner - Deployment Guide

This guide will help you deploy the Smart Planner application so others can access it online.

## Architecture Overview

- **Frontend**: Vercel (Static HTML/JS/CSS)
- **Backend API**: Railway or Render (FastAPI)
- **Database**: Railway MySQL or PlanetScale (Cloud MySQL)

---

## Option 1: Quick Deploy (Recommended)

### Step 1: Deploy Frontend to Vercel

1. **Install Vercel CLI** (if not installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy Frontend**:
   ```bash
   cd /Applications/XAMPP/xamppfiles/htdocs/smartplanner
   vercel
   ```
   
   Follow the prompts:
   - Set up and deploy? **Yes**
   - Which scope? **Your account**
   - Link to existing project? **No**
   - Project name: **smart-planner**
   - Directory: **./** (current directory)
   - Override settings? **No**

4. **Update API URL in Frontend**:
   
   After deployment, Vercel will give you a URL like `https://smart-planner.vercel.app`
   
   Update `index.html` and `calendar.html`:
   ```javascript
   const API_BASE = 'https://your-backend-url.railway.app'; // Update this
   ```

5. **Redeploy**:
   ```bash
   vercel --prod
   ```

### Step 2: Deploy Backend to Railway

1. **Go to Railway**: https://railway.app
   - Sign up/login with GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

3. **Add MySQL Database**:
   - Click "New" → "Database" → "MySQL"
   - Railway will create a MySQL database
   - Note the connection details

4. **Configure Environment Variables**:
   - Go to your backend service → Variables
   - Add these variables:
     ```
     DB_HOST=<railway-mysql-host>
     DB_PORT=3306
     DB_NAME=railway
     DB_USER=root
     DB_PASSWORD=<railway-mysql-password>
     ALLOWED_ORIGINS=https://your-frontend.vercel.app
     PORT=8000
     ```
   - Railway provides these in the MySQL service → Variables tab

5. **Deploy**:
   - Railway will auto-detect Python and deploy
   - It will run: `uvicorn api:app --host 0.0.0.0 --port $PORT`
   - Get your backend URL from the service → Settings → Domains

6. **Run Database Setup**:
   - Go to Railway MySQL → Connect
   - Run the SQL from `setup.sql` or use the setup scripts
   - Or SSH into the service and run:
     ```bash
     python setup_users.py
     python setup_extended_features.py
     ```

### Step 3: Update Frontend API URL

1. **Get Backend URL** from Railway (e.g., `https://smart-planner-production.up.railway.app`)

2. **Update Frontend Files**:
   ```bash
   # In index.html, login.html, calendar.html
   const API_BASE = 'https://your-backend-url.railway.app';
   ```

3. **Redeploy to Vercel**:
   ```bash
   vercel --prod
   ```

---

## Option 2: Deploy Backend to Render

1. **Go to Render**: https://render.com
   - Sign up/login

2. **Create New Web Service**:
   - Connect your GitHub repo
   - Settings:
     - **Name**: smart-planner-api
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables**:
   - Use Render's PostgreSQL or external MySQL
   - Add same variables as Railway

4. **Get Backend URL** and update frontend

---

## Option 3: All-in-One on Railway

Deploy both frontend and backend on Railway:

1. **Create Two Services**:
   - Backend service (Python)
   - Frontend service (Static site)

2. **For Frontend Service**:
   - Build Command: `echo "No build needed"`
   - Start Command: `npx serve . -p $PORT`

3. **Configure**:
   - Set environment variables
   - Connect database
   - Update API URLs

---

## Database Setup (Cloud)

### Using Railway MySQL:

1. **Get Connection String** from Railway MySQL service
2. **Run Setup Scripts**:
   ```bash
   # Set environment variables first
   export DB_HOST=...
   export DB_USER=...
   export DB_PASSWORD=...
   export DB_NAME=...
   
   # Run setup
   python setup_users.py
   python setup_extended_features.py
   ```

### Using PlanetScale (Free MySQL):

1. **Sign up**: https://planetscale.com
2. **Create Database**: "smartplanner"
3. **Get Connection String**
4. **Update Environment Variables**
5. **Run Setup Scripts**

---

## Environment Variables Reference

### Backend (Railway/Render):
```env
DB_HOST=your-db-host
DB_PORT=3306
DB_NAME=smartplanner
DB_USER=root
DB_PASSWORD=your-password
ALLOWED_ORIGINS=https://your-frontend.vercel.app
PORT=8000
```

### Frontend (Vercel):
No environment variables needed (API URL is hardcoded in HTML)

---

## Testing Deployment

1. **Test Frontend**: Visit your Vercel URL
2. **Test Backend**: Visit `https://your-backend.railway.app/docs`
3. **Test Login**: Try logging in with test credentials
4. **Test API**: Use Swagger UI at `/docs` endpoint

---

## Troubleshooting

### CORS Errors:
- Make sure `ALLOWED_ORIGINS` includes your frontend URL
- Check that backend allows credentials

### Database Connection Errors:
- Verify environment variables are set correctly
- Check database is accessible from Railway/Render
- Ensure database is created and tables exist

### Frontend Can't Connect:
- Verify API_BASE URL is correct
- Check backend is running (visit /docs)
- Check CORS settings

---

## Quick Start Commands

```bash
# Deploy frontend
vercel --prod

# Check backend logs (Railway)
railway logs

# Check backend logs (Render)
# Use Render dashboard

# Update database
railway run python setup_users.py
```

---

## Production Checklist

- [ ] Database is cloud-hosted (not localhost)
- [ ] Environment variables are set
- [ ] CORS is configured correctly
- [ ] Frontend API URL is updated
- [ ] Database tables are created
- [ ] Users are created
- [ ] SSL/HTTPS is enabled (automatic on Vercel/Railway)
- [ ] Test login works
- [ ] Test task creation works
- [ ] Test plan generation works

---

## Cost Estimate

- **Vercel**: Free tier (unlimited for personal projects)
- **Railway**: $5/month (includes database)
- **Render**: Free tier available
- **PlanetScale**: Free tier available

**Total**: ~$0-5/month

---

## Need Help?

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
