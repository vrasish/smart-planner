import pymysql
from datetime import date

conn = pymysql.connect(
    host="localhost",
    port=3306,
    database="smartplanner",
    user="root",
    password=""
)

cur = conn.cursor()

cur.execute("SELECT id, title, deadline, duration_minutes, priority FROM tasks WHERE status='pending'")
tasks = list(cur.fetchall())

# Sort tasks (smart logic)
tasks.sort(key=lambda x: (x[2], -x[4], x[3]))

available_minutes = 300
today = date.today()

order = 1

for task in tasks:
    if task[3] <= available_minutes:
        cur.execute(
            "INSERT INTO daily_plan (task_id, plan_date, task_order) VALUES (%s,%s,%s)",
            (task[0], today, order)
        )
        available_minutes -= task[3]
        order += 1

conn.commit()
print("Today's plan generated")

cur.close()
conn.close()
