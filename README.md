# 🧠 Smart Planner

A full-featured task planning application with intelligent scheduling, calendar view, notifications, and user management.

## ✨ Features

- ✅ **User Authentication** - Secure login with role-based access
- 📅 **Smart Scheduling** - AI-powered task planning based on deadlines and priorities
- 📆 **Calendar View** - Visual monthly calendar with all scheduled tasks
- 🔔 **Notifications** - Browser and in-app notifications
- 🏷️ **Categories** - Organize tasks by category (School, Work, Personal, etc.)
- ✅ **Task Completion** - Track completed tasks with timestamps
- 📊 **Multi-day Planning** - Plan tasks across multiple days
- 🎨 **Modern UI** - Beautiful, responsive design

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.13+
- MySQL/MariaDB
- XAMPP (for local database)

### Installation

1. **Clone/Download** the project

2. **Setup Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Setup Database**:
   ```bash
   python setup_users.py
   python setup_extended_features.py
   ```

4. **Start Backend**:
   ```bash
   uvicorn api:app --reload
   ```

5. **Open Frontend**:
   - Navigate to `http://localhost/smartplanner/login.html`
   - Or use any local server

### Default Users

- **Admin**: `admin` / `admin123.`
- **Students**: `Vaishnavi`, `Student2`, `Student3`, `Student4` / `student`

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy**:
- Frontend: Deploy to Vercel
- Backend: Deploy to Railway or Render
- Database: Use Railway MySQL or PlanetScale

See [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for step-by-step guide.

## 📁 Project Structure

```
smartplanner/
├── api.py                 # FastAPI backend
├── index.html             # Main planner interface
├── login.html             # Login page
├── calendar.html          # Calendar view
├── config.js              # API configuration
├── style.css              # Styling
├── setup_users.py         # User setup script
├── setup_extended_features.py  # Feature setup
├── requirements.txt       # Python dependencies
└── DEPLOYMENT.md         # Deployment guide
```

## 🔧 Configuration

### Local Development

Update `config.js`:
```javascript
const API_BASE = 'http://localhost:8000';
```

### Production

Update `config.js` with your backend URL:
```javascript
const API_BASE = 'https://your-backend.railway.app';
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, JavaScript, CSS3
- **Database**: MySQL/MariaDB
- **Authentication**: Session-based
- **Deployment**: Vercel (Frontend), Railway/Render (Backend)

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ for smart task planning**
