// API Configuration - Update this for production
// For local development, this will use localhost
// For production, update this to your deployed backend URL

const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : 'https://web-production-02573.up.railway.app' // UPDATE THIS with your Railway/Render backend URL
