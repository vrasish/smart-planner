# 🚀 Quick Deployment Guide

## Deploy in 3 Steps

### Step 1: Deploy Frontend to Vercel (5 minutes)

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd /Applications/XAMPP/xamppfiles/htdocs/smartplanner
vercel

# Follow prompts, then:
vercel --prod
```

**You'll get a URL like**: `https://smart-planner.vercel.app`

---

### Step 2: Deploy Backend to Railway (10 minutes)

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **New Project** → **Deploy from GitHub** (or use Railway CLI)
4. **Add MySQL Database**:
   - Click "New" → "Database" → "MySQL"
5. **Set Environment Variables**:
   - Go to your service → Variables
   - Add:
     ```
     DB_HOST=<from MySQL service>
     DB_PORT=3306
     DB_NAME=railway
     DB_USER=root
     DB_PASSWORD=<from MySQL service>
     ALLOWED_ORIGINS=https://your-vercel-url.vercel.app
     ```
6. **Get Backend URL**: Service → Settings → Generate Domain

**You'll get a URL like**: `https://smart-planner-production.up.railway.app`

---

### Step 3: Connect Frontend to Backend (2 minutes)

1. **Update `config.js`**:
   ```javascript
   const API_BASE = 'https://your-railway-backend-url.railway.app';
   ```

2. **Redeploy to Vercel**:
   ```bash
   vercel --prod
   ```

3. **Setup Database** (in Railway):
   - Connect to MySQL service
   - Run SQL from `setup.sql` OR
   - SSH and run: `python setup_users.py`

---

## That's It! 🎉

Your app is now live and accessible to everyone!

**Frontend**: `https://your-app.vercel.app`  
**Backend API**: `https://your-backend.railway.app`  
**API Docs**: `https://your-backend.railway.app/docs`

---

## Alternative: Deploy Backend to Render

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (same as Railway)
6. Get URL and update `config.js`

---

## Free Tier Limits

- **Vercel**: Unlimited (personal projects)
- **Railway**: $5/month (includes database)
- **Render**: Free tier available

**Total Cost**: $0-5/month

---

## Troubleshooting

**CORS Error?**
- Make sure `ALLOWED_ORIGINS` includes your Vercel URL
- Check backend is running (visit `/docs`)

**Database Error?**
- Verify environment variables
- Run setup scripts: `python setup_users.py`

**Frontend Can't Connect?**
- Check `config.js` has correct backend URL
- Test backend: visit `https://your-backend.railway.app/docs`
