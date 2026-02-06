-- Complete SQL script to create all tables in Railway MySQL
-- Run this in Railway MySQL after connecting

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    deadline DATE,
    duration_minutes INT,
    priority INT,
    status TEXT DEFAULT 'pending',
    user_id INT,
    category VARCHAR(50) DEFAULT 'General',
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create daily_plan table
CREATE TABLE IF NOT EXISTS daily_plan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT,
    plan_date DATE,
    task_order INT,
    user_id INT,
    scheduled_time TIME,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(7) DEFAULT '#667eea',
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(20) DEFAULT 'info',
    read_status BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert default categories
INSERT IGNORE INTO categories (name, color, user_id) VALUES
('General', '#667eea', NULL),
('School', '#4CAF50', NULL),
('Work', '#2196F3', NULL),
('Personal', '#FF9800', NULL),
('Health', '#E91E63', NULL),
('Shopping', '#9C27B0', NULL);

-- Insert admin user (password: admin123.)
-- Password hash for "admin123." using SHA-256
INSERT IGNORE INTO users (username, password_hash, role) VALUES
('admin', '697e5535dcf7950a01b234207409cdb296684d3d8092ebddd7a7f699f6c21212', 'admin');

-- Insert student users (password: student)  
-- Password hash for "student" using SHA-256
INSERT IGNORE INTO users (username, password_hash, role) VALUES
('Vaishnavi', '264c8c381bf16c982a4e59b0dd4c6f7808c51a05f64c35db42cc78a2a72875bb', 'user'),
('Student2', '264c8c381bf16c982a4e59b0dd4c6f7808c51a05f64c35db42cc78a2a72875bb', 'user'),
('Student3', '264c8c381bf16c982a4e59b0dd4c6f7808c51a05f64c35db42cc78a2a72875bb', 'user'),
('Student4', '264c8c381bf16c982a4e59b0dd4c6f7808c51a05f64c35db42cc78a2a72875bb', 'user');
