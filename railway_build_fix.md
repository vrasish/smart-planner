# Fix Railway Build - Manual Configuration

If nixpacks.toml doesn't work, configure manually in Railway:

## Step 1: Go to Service Settings

1. Click on your "web" service in Railway
2. Click "Settings" tab
3. Scroll to "Build & Deploy" section

## Step 2: Configure Build

Set these values:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn api:app --host 0.0.0.0 --port $PORT
```

## Step 3: Save and Redeploy

1. Click "Save" or the changes auto-save
2. Go to "Deployments" tab
3. Click "Redeploy" on latest deployment

## Alternative: Check Build Logs

1. Go to "Deployments" tab
2. Click on latest deployment
3. Click "Build Logs" tab
4. Check if it shows:
   - "Installing dependencies"
   - "pip install -r requirements.txt"
   - "Successfully installed..."

If you don't see this, the build isn't running. Use manual configuration above.
