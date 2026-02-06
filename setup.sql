-- MySQL/MariaDB table creation for Smart Planner
-- Run this in DBeaver

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    deadline DATE,
    duration_minutes INT,
    priority INT,
    status TEXT DEFAULT 'pending'
);

CREATE TABLE daily_plan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT,
    plan_date DATE,
    task_order INT
);

-- Insert test data
INSERT INTO tasks (title, deadline, duration_minutes, priority)
VALUES ('Math homework', '2026-02-06', 60, 5);

INSERT INTO tasks (title, deadline, duration_minutes, priority)
VALUES ('Science project', '2026-02-10', 180, 3);

INSERT INTO tasks (title, deadline, duration_minutes, priority)
VALUES ('Read book', '2026-02-07', 30, 2);
