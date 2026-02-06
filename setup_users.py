import pymysql
import hashlib

# Connect to database
conn = pymysql.connect(
    host="localhost",
    port=3306,
    database="smartplanner",
    user="root",
    password=""
)

cur = conn.cursor()

# Create users table
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        role VARCHAR(20) DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Add user_id to tasks table if it doesn't exist
try:
    cur.execute("ALTER TABLE tasks ADD COLUMN user_id INT")
    cur.execute("ALTER TABLE tasks ADD FOREIGN KEY (user_id) REFERENCES users(id)")
except:
    pass  # Column might already exist

# Add user_id to daily_plan table if it doesn't exist
try:
    cur.execute("ALTER TABLE daily_plan ADD COLUMN user_id INT")
    cur.execute("ALTER TABLE daily_plan ADD FOREIGN KEY (user_id) REFERENCES users(id)")
except:
    pass  # Column might already exist

# Add scheduled_time to daily_plan for time-based ordering
try:
    cur.execute("ALTER TABLE daily_plan ADD COLUMN scheduled_time TIME")
except:
    pass  # Column might already exist

# Hash password function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Clear existing users (optional - comment out if you want to keep existing users)
cur.execute("DELETE FROM users")

# Insert admin user
admin_password_hash = hash_password("admin123.")
cur.execute("""
    INSERT INTO users (username, password_hash, role)
    VALUES (%s, %s, %s)
""", ("admin", admin_password_hash, "admin"))

# Insert regular users
users = ["Vaishnavi", "Student2", "Student3", "Student4"]
student_password_hash = hash_password("student")

for username in users:
    try:
        cur.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (%s, %s, %s)
        """, (username, student_password_hash, "user"))
    except:
        pass  # User might already exist

conn.commit()
print("✅ Users table created!")
print("✅ Admin user created: username='admin', password='admin123.'")
print("✅ Student users created:")
for username in users:
    print(f"   - {username} (password: 'student')")
print("✅ Tables updated with user_id columns")

cur.close()
conn.close()
