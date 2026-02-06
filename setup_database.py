import pymysql

# Connect to database
conn = pymysql.connect(
    host="localhost",
    port=3306,
    database="smartplanner",
    user="root",
    password=""
)

cur = conn.cursor()

# Create tasks table
cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title TEXT,
        deadline DATE,
        duration_minutes INT,
        priority INT,
        status TEXT DEFAULT 'pending'
    )
""")

# Create daily_plan table
cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_plan (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_id INT,
        plan_date DATE,
        task_order INT
    )
""")

# Clear existing test data (optional - comment out if you want to keep existing data)
cur.execute("DELETE FROM tasks")
cur.execute("DELETE FROM daily_plan")

# Insert test data
test_tasks = [
    ('Math homework', '2026-02-06', 60, 5),
    ('Science project', '2026-02-10', 180, 3),
    ('Read book', '2026-02-07', 30, 2)
]

for task in test_tasks:
    cur.execute("""
        INSERT INTO tasks (title, deadline, duration_minutes, priority)
        VALUES (%s, %s, %s, %s)
    """, task)

conn.commit()
print("✅ Database setup complete!")
print("✅ Tables created: tasks, daily_plan")
print("✅ Test data inserted: 3 tasks")

cur.close()
conn.close()
