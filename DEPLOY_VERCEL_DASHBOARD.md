# Deploy to Vercel via Dashboard

## Step 1: Push Code to GitHub

1. Go to https://github.com
2. Create a new repository (or use existing)
3. Push your code:

```bash
cd /Applications/XAMPP/xamppfiles/htdocs/smartplanner
git init
git add .
git commit -m "Smart Planner project"
git remote add origin https://github.com/YOUR_USERNAME/smart-planner.git
git push -u origin main
```

## Step 2: Import Project in Vercel

1. Go to https://vercel.com/vrasishs-projects
2. Click **"Add New..."** → **"Project"**
3. Click **"Import Git Repository"**
4. Select your GitHub repository (`smart-planner`)
5. Click **"Import"**

## Step 3: Configure Project

Vercel will auto-detect settings:
- **Framework Preset**: Other (or leave default)
- **Root Directory**: `./` (current directory)
- **Build Command**: Leave empty (static site)
- **Output Directory**: Leave empty

Click **"Deploy"**

## Step 4: Wait for Deployment

- Vercel will deploy your project
- Takes 1-2 minutes
- You'll get a URL like: `https://smart-planner-xxxxx.vercel.app`

## Step 5: Done!

Your frontend is now live! 🎉

**Next**: Deploy backend to Railway and update `config.js`
