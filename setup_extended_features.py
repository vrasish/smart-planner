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

# Add category column to tasks
try:
    cur.execute("ALTER TABLE tasks ADD COLUMN category VARCHAR(50) DEFAULT 'General'")
    print("✅ Added category column to tasks")
except Exception as e:
    print(f"Category column may already exist: {e}")

# Add completed_at timestamp to tasks
try:
    cur.execute("ALTER TABLE tasks ADD COLUMN completed_at TIMESTAMP NULL")
    print("✅ Added completed_at column to tasks")
except Exception as e:
    print(f"Completed_at column may already exist: {e}")

# Create categories table
cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL,
        color VARCHAR(7) DEFAULT '#667eea',
        user_id INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
""")
print("✅ Created categories table")

# Create notifications table
cur.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        message TEXT NOT NULL,
        type VARCHAR(20) DEFAULT 'info',
        read_status BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
""")
print("✅ Created notifications table")

# Insert default categories
default_categories = [
    ('General', '#667eea'),
    ('School', '#4CAF50'),
    ('Work', '#2196F3'),
    ('Personal', '#FF9800'),
    ('Health', '#E91E63'),
    ('Shopping', '#9C27B0')
]

for cat_name, color in default_categories:
    try:
        cur.execute("""
            INSERT INTO categories (name, color, user_id)
            VALUES (%s, %s, NULL)
        """, (cat_name, color))
    except:
        pass  # Category might already exist

conn.commit()
print("✅ Extended features setup complete!")
print("✅ Default categories created")

cur.close()
conn.close()
