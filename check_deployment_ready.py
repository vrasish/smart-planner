#!/usr/bin/env python3
"""
Deployment Readiness Checker
Verifies all files and configurations are ready for deployment
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ Missing: {description} - {filepath}")
        return False

def check_file_content(filepath, required_strings, description):
    """Check if file contains required strings"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    all_found = True
    for req_str in required_strings:
        if req_str in content:
            print(f"✅ {description}: Found '{req_str}' in {filepath}")
        else:
            print(f"⚠️  {description}: Missing '{req_str}' in {filepath}")
            all_found = False
    
    return all_found

print("🔍 Checking Deployment Readiness...\n")

# Check critical files
files_ok = True
files_ok &= check_file_exists("api.py", "Backend API")
files_ok &= check_file_exists("index.html", "Main frontend")
files_ok &= check_file_exists("login.html", "Login page")
files_ok &= check_file_exists("calendar.html", "Calendar page")
files_ok &= check_file_exists("config.js", "API configuration")
files_ok &= check_file_exists("style.css", "Stylesheet")
files_ok &= check_file_exists("requirements.txt", "Python dependencies")
files_ok &= check_file_exists("vercel.json", "Vercel config")
files_ok &= check_file_exists("package.json", "Package config")
files_ok &= check_file_exists("railway.json", "Railway config")
files_ok &= check_file_exists("Procfile", "Render/Heroku config")
files_ok &= check_file_exists("DEPLOYMENT.md", "Deployment guide")
files_ok &= check_file_exists("QUICK_DEPLOY.md", "Quick deploy guide")

print("\n📋 Checking Configuration...\n")

# Check config.js
config_ok = check_file_content(
    "config.js",
    ["API_BASE", "localhost", "railway.app"],
    "config.js setup"
)

# Check API uses environment variables
api_ok = check_file_content(
    "api.py",
    ["os.getenv", "DB_HOST", "get_conn"],
    "API environment variables"
)

# Check frontend uses config.js
index_ok = check_file_content(
    "index.html",
    ["config.js"],
    "Frontend config.js reference"
)

login_ok = check_file_content(
    "login.html",
    ["config.js"],
    "Login page config.js reference"
)

calendar_ok = check_file_content(
    "calendar.html",
    ["config.js"],
    "Calendar page config.js reference"
)

print("\n📦 Checking Dependencies...\n")

# Check requirements.txt
if os.path.exists("requirements.txt"):
    with open("requirements.txt", 'r') as f:
        deps = f.read()
        required_deps = ["fastapi", "uvicorn", "pymysql"]
        for dep in required_deps:
            if dep in deps.lower():
                print(f"✅ Dependency found: {dep}")
            else:
                print(f"⚠️  Missing dependency: {dep}")

print("\n" + "="*50)
if files_ok and config_ok and api_ok and index_ok and login_ok and calendar_ok:
    print("✅ ALL CHECKS PASSED - Ready for deployment!")
    print("\n📝 Next Steps:")
    print("1. Update config.js with your backend URL after deployment")
    print("2. Deploy frontend to Vercel: vercel --prod")
    print("3. Deploy backend to Railway/Render")
    print("4. Set environment variables in Railway/Render")
    print("5. Run database setup scripts")
    sys.exit(0)
else:
    print("⚠️  SOME CHECKS FAILED - Review above")
    print("\nPlease fix the issues before deploying")
    sys.exit(1)
