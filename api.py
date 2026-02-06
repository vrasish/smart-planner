from fastapi import FastAPI, HTTPException, Depends, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pymysql
from datetime import date, datetime, time, timedelta
from typing import List, Optional
import hashlib
import secrets
import os

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection using environment variables
def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "smartplanner"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        connect_timeout=10
    )

# Initialize database connection (lazy connection)
conn = None

def get_conn():
    global conn
    if conn is None:
        try:
            conn = get_db_connection()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")
    return conn

# In-memory session storage (use Redis in production)
sessions = {}

# Request/Response models
class LoginRequest(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    title: str
    deadline: str
    duration: int
    priority: int
    category: Optional[str] = "General"

class TaskResponse(BaseModel):
    id: int
    title: str
    deadline: str
    duration_minutes: int
    priority: int
    status: str
    category: Optional[str] = None
    completed_at: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    color: str

class NotificationResponse(BaseModel):
    id: int
    message: str
    type: str
    read_status: bool
    created_at: str

class CalendarEvent(BaseModel):
    date: str
    tasks: List[dict]

class PlanItem(BaseModel):
    title: str
    task_order: int
    duration_minutes: int
    priority: int
    deadline: str
    scheduled_time: Optional[str] = None
    task_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

# Authentication helpers
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash

def create_session(user_id: int, username: str, role: str) -> str:
    session_token = secrets.token_urlsafe(32)
    sessions[session_token] = {
        "user_id": user_id,
        "username": username,
        "role": role
    }
    return session_token

def get_current_user(session_token: Optional[str] = Cookie(None)) -> dict:
    if not session_token or session_token not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return sessions[session_token]

def create_notification(user_id: int, message: str, notif_type: str = "info"):
    """Helper function to create notifications"""
    db_conn = get_conn()
    cur = db_conn.cursor()
    cur.execute(
        "INSERT INTO notifications (user_id, message, type) VALUES (%s, %s, %s)",
        (user_id, message, notif_type)
    )
    db_conn.commit()

# Authentication endpoints
@app.post("/login")
def login(credentials: LoginRequest, response: JSONResponse):
    """Login endpoint"""
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = %s",
        (credentials.username,)
    )
    user = cur.fetchone()
    
    if not user or not verify_password(credentials.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    session_token = create_session(user[0], user[1], user[3])
    response.set_cookie(key="session_token", value=session_token, httponly=True, samesite="lax")
    
    return {
        "message": "Login successful",
        "user": {
            "id": user[0],
            "username": user[1],
            "role": user[3]
        },
        "session_token": session_token
    }

@app.post("/logout")
def logout(session_token: Optional[str] = Cookie(None)):
    """Logout endpoint"""
    if session_token and session_token in sessions:
        del sessions[session_token]
    return {"message": "Logged out successfully"}

@app.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user info"""
    return UserResponse(
        id=current_user["user_id"],
        username=current_user["username"],
        role=current_user["role"]
    )

# Task endpoints (require authentication)
@app.post("/tasks")
def add_task(task: TaskCreate, current_user: dict = Depends(get_current_user)):
    """Add a new task to the database"""
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, deadline, duration_minutes, priority, user_id, category) VALUES (%s, %s, %s, %s, %s, %s)",
        (task.title, task.deadline, task.duration, task.priority, current_user["user_id"], task.category)
    )
    conn.commit()
    
    # Create notification for new task
    create_notification(
        current_user["user_id"],
        f"New task '{task.title}' added with deadline {task.deadline}",
        "info"
    )
    
    return {"message": "Task added", "id": cur.lastrowid}

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(current_user: dict = Depends(get_current_user)):
    """Get all tasks for current user"""
    cur = conn.cursor()
    
    # Admin can see all tasks, users see only their own
    if current_user["role"] == "admin":
        cur.execute("SELECT id, title, deadline, duration_minutes, priority, status, category, completed_at FROM tasks")
    else:
        cur.execute(
            "SELECT id, title, deadline, duration_minutes, priority, status, category, completed_at FROM tasks WHERE user_id = %s",
            (current_user["user_id"],)
        )
    
    tasks = cur.fetchall()
    return [
        TaskResponse(
            id=t[0],
            title=t[1],
            deadline=str(t[2]),
            duration_minutes=t[3],
            priority=t[4],
            status=t[5],
            category=t[6] if len(t) > 6 else None,
            completed_at=str(t[7]) if len(t) > 7 and t[7] else None
        )
        for t in tasks
    ]

@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    """Mark a task as completed"""
    cur = conn.cursor()
    
    # Check if task belongs to user
    cur.execute("SELECT id, title, user_id FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task[2] != current_user["user_id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update task status
    cur.execute(
        "UPDATE tasks SET status = 'completed', completed_at = NOW() WHERE id = %s",
        (task_id,)
    )
    conn.commit()
    
    # Create notification
    create_notification(
        current_user["user_id"],
        f"Task '{task[1]}' marked as completed! 🎉",
        "success"
    )
    
    return {"message": "Task completed", "task_id": task_id}

@app.patch("/tasks/{task_id}/uncomplete")
def uncomplete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    """Mark a task as pending again"""
    cur = conn.cursor()
    
    cur.execute("SELECT user_id FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task[0] != current_user["user_id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    cur.execute(
        "UPDATE tasks SET status = 'pending', completed_at = NULL WHERE id = %s",
        (task_id,)
    )
    conn.commit()
    
    return {"message": "Task set to pending", "task_id": task_id}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    """Delete a task"""
    cur = conn.cursor()
    
    cur.execute("SELECT user_id FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task[0] != current_user["user_id"] and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    
    return {"message": "Task deleted", "task_id": task_id}

@app.post("/generate-plan")
def generate_plan(days: int = 1, current_user: dict = Depends(get_current_user)):
    """Generate smart daily plan from pending tasks with timely scheduling"""
    cur = conn.cursor()
    
    today = date.today()
    results = []
    
    for day_offset in range(days):
        plan_date = today + timedelta(days=day_offset)
        
        # Clear existing plan for this date
        cur.execute(
            "DELETE FROM daily_plan WHERE plan_date = %s AND user_id = %s",
            (plan_date, current_user["user_id"])
        )
    
        # Fetch pending tasks for this user that haven't been planned yet
        cur.execute("""
            SELECT t.id, t.deadline, t.duration_minutes, t.priority, t.title
            FROM tasks t
            LEFT JOIN daily_plan dp ON t.id = dp.task_id AND dp.plan_date = %s
            WHERE t.status='pending' AND t.user_id = %s AND dp.id IS NULL
        """, (plan_date, current_user["user_id"]))
        tasks = list(cur.fetchall())
        
        if not tasks:
            results.append({
                "date": str(plan_date),
                "tasks_planned": 0,
                "message": "No pending tasks to plan"
            })
            continue
        
        # Calculate urgency score: days until deadline
        def calculate_urgency(deadline_str):
            deadline = datetime.strptime(str(deadline_str), "%Y-%m-%d").date()
            days_until = (deadline - plan_date).days
            return days_until  # Negative means overdue (high urgency)
        
        # Sort tasks: most urgent first, then highest priority, then shortest duration
        tasks_with_urgency = [(t, calculate_urgency(t[1])) for t in tasks]
        tasks_with_urgency.sort(key=lambda x: (x[1], -x[0][3], x[0][2]))
        
        # Schedule tasks in timely order
        available_minutes = 300  # 5 hours
        start_time = datetime.combine(plan_date, time(9, 0))
        current_time = start_time
        order = 1
        planned_tasks = []
        
        for task, urgency in tasks_with_urgency:
            duration = task[2]
            
            if duration <= available_minutes:
                scheduled_time = current_time.time()
                
                cur.execute(
                    "INSERT INTO daily_plan (task_id, plan_date, task_order, user_id, scheduled_time) VALUES (%s, %s, %s, %s, %s)",
                    (task[0], plan_date, order, current_user["user_id"], scheduled_time)
                )
                
                current_time += timedelta(minutes=duration)
                available_minutes -= duration
                planned_tasks.append({
                    "task_id": task[0],
                    "title": task[4],
                    "order": order,
                    "duration": duration,
                    "scheduled_time": scheduled_time.strftime("%H:%M")
                })
                order += 1
        
        results.append({
            "date": str(plan_date),
            "tasks_planned": len(planned_tasks),
            "remaining_minutes": available_minutes,
            "start_time": start_time.strftime("%H:%M"),
            "tasks": planned_tasks
        })
    
    conn.commit()
    
    # Create notification
    total_planned = sum(r["tasks_planned"] for r in results)
    create_notification(
        current_user["user_id"],
        f"Generated plan for {days} day(s) with {total_planned} tasks scheduled!",
        "success"
    )
    
    return {
        "message": f"Plan generated for {days} day(s)",
        "results": results,
        "total_tasks_planned": total_planned
    }

@app.get("/plan/today", response_model=List[PlanItem])
def get_today(current_user: dict = Depends(get_current_user)):
    """Get today's plan for current user"""
    cur = conn.cursor()
    cur.execute("""
        SELECT t.title, d.task_order, t.duration_minutes, t.priority, t.deadline, d.scheduled_time, t.id
        FROM daily_plan d
        JOIN tasks t ON t.id = d.task_id
        WHERE d.plan_date = CURDATE() AND d.user_id = %s
        ORDER BY d.task_order
    """, (current_user["user_id"],))
    plan = cur.fetchall()
    result = []
    for item in plan:
        scheduled_time_str = None
        if item[5]:
            if isinstance(item[5], time):
                scheduled_time_str = item[5].strftime("%H:%M")
            else:
                scheduled_time_str = str(item[5])
        result.append(PlanItem(
            title=item[0],
            task_order=item[1],
            duration_minutes=item[2],
            priority=item[3],
            deadline=str(item[4]),
            scheduled_time=scheduled_time_str,
            task_id=item[6] if len(item) > 6 else None
        ))
    return result

@app.get("/plan/{plan_date}")
def get_plan_by_date(plan_date: str, current_user: dict = Depends(get_current_user)):
    """Get plan for a specific date"""
    cur = conn.cursor()
    cur.execute("""
        SELECT t.title, d.task_order, t.duration_minutes, t.priority, t.deadline, d.scheduled_time, t.id
        FROM daily_plan d
        JOIN tasks t ON t.id = d.task_id
        WHERE d.plan_date = %s AND d.user_id = %s
        ORDER BY d.task_order
    """, (plan_date, current_user["user_id"]))
    plan = cur.fetchall()
    result = []
    for item in plan:
        scheduled_time_str = None
        if item[5]:
            if isinstance(item[5], time):
                scheduled_time_str = item[5].strftime("%H:%M")
            else:
                scheduled_time_str = str(item[5])
        result.append({
            "title": item[0],
            "task_order": item[1],
            "duration_minutes": item[2],
            "priority": item[3],
            "deadline": str(item[4]),
            "scheduled_time": scheduled_time_str,
            "task_id": item[6]
        })
    return result

# Categories endpoints
@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(current_user: dict = Depends(get_current_user)):
    """Get all categories"""
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, color FROM categories 
        WHERE user_id IS NULL OR user_id = %s
        ORDER BY name
    """, (current_user["user_id"],))
    categories = cur.fetchall()
    return [
        CategoryResponse(id=c[0], name=c[1], color=c[2])
        for c in categories
    ]

@app.post("/categories")
def create_category(name: str, color: str = "#667eea", current_user: dict = Depends(get_current_user)):
    """Create a new category"""
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO categories (name, color, user_id) VALUES (%s, %s, %s)",
            (name, color, current_user["user_id"])
        )
        conn.commit()
        return {"message": "Category created", "id": cur.lastrowid}
    except pymysql.IntegrityError:
        raise HTTPException(status_code=400, detail="Category already exists")

# Calendar endpoints
@app.get("/calendar")
def get_calendar(start_date: str, end_date: str, current_user: dict = Depends(get_current_user)):
    """Get calendar view with tasks for date range"""
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            d.plan_date,
            t.id,
            t.title,
            t.duration_minutes,
            t.priority,
            t.deadline,
            d.scheduled_time,
            t.category,
            t.status
        FROM daily_plan d
        JOIN tasks t ON t.id = d.task_id
        WHERE d.plan_date BETWEEN %s AND %s AND d.user_id = %s
        ORDER BY d.plan_date, d.task_order
    """, (start_date, end_date, current_user["user_id"]))
    
    events = cur.fetchall()
    calendar = {}
    
    for event in events:
        date_str = str(event[0])
        if date_str not in calendar:
            calendar[date_str] = []
        
        scheduled_time_str = None
        if event[6]:
            if isinstance(event[6], time):
                scheduled_time_str = event[6].strftime("%H:%M")
            else:
                scheduled_time_str = str(event[6])
        
        calendar[date_str].append({
            "task_id": event[1],
            "title": event[2],
            "duration_minutes": event[3],
            "priority": event[4],
            "deadline": str(event[5]),
            "scheduled_time": scheduled_time_str,
            "category": event[7],
            "status": event[8]
        })
    
    return calendar

# Notifications endpoints
@app.get("/notifications", response_model=List[NotificationResponse])
def get_notifications(unread_only: bool = False, current_user: dict = Depends(get_current_user)):
    """Get notifications for current user"""
    cur = conn.cursor()
    
    if unread_only:
        cur.execute("""
            SELECT id, message, type, read_status, created_at
            FROM notifications
            WHERE user_id = %s AND read_status = FALSE
            ORDER BY created_at DESC
            LIMIT 50
        """, (current_user["user_id"],))
    else:
        cur.execute("""
            SELECT id, message, type, read_status, created_at
            FROM notifications
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 50
        """, (current_user["user_id"],))
    
    notifications = cur.fetchall()
    return [
        NotificationResponse(
            id=n[0],
            message=n[1],
            type=n[2],
            read_status=bool(n[3]),
            created_at=str(n[4])
        )
        for n in notifications
    ]

@app.patch("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: int, current_user: dict = Depends(get_current_user)):
    """Mark a notification as read"""
    cur = conn.cursor()
    cur.execute("""
        UPDATE notifications 
        SET read_status = TRUE 
        WHERE id = %s AND user_id = %s
    """, (notification_id, current_user["user_id"]))
    conn.commit()
    return {"message": "Notification marked as read"}

@app.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int, current_user: dict = Depends(get_current_user)):
    """Delete a notification"""
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM notifications 
        WHERE id = %s AND user_id = %s
    """, (notification_id, current_user["user_id"]))
    conn.commit()
    return {"message": "Notification deleted"}

@app.get("/")
def root():
    """API root endpoint"""
    return {
        "message": "Smart Planner API",
        "endpoints": {
            "POST /login": "Login",
            "POST /logout": "Logout",
            "GET /me": "Get current user",
            "POST /tasks": "Add a new task",
            "GET /tasks": "Get all tasks",
            "POST /generate-plan": "Generate today's smart plan",
            "GET /plan/today": "Get today's plan"
        },
        "docs": "/docs"
    }
