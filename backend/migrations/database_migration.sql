-- =========================================
-- DATABASE MIGRATION SCRIPT
-- Purpose: Add missing columns to existing tables
-- Version: 1.0
-- Date: September 23, 2025
-- =========================================

USE seating_plan_db;

-- Check and add missing columns to users table
-- Add 'role' column if it doesn't exist
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = 'seating_plan_db' 
     AND TABLE_NAME = 'users' 
     AND COLUMN_NAME = 'role') = 0,
    'ALTER TABLE users ADD COLUMN role ENUM(''admin'', ''faculty'', ''student'') DEFAULT ''student'' AFTER full_name;',
    'SELECT ''role column already exists'' as Status;'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add 'is_active' column if it doesn't exist
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = 'seating_plan_db' 
     AND TABLE_NAME = 'users' 
     AND COLUMN_NAME = 'is_active') = 0,
    'ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE AFTER role;',
    'SELECT ''is_active column already exists'' as Status;'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add 'updated_at' column if it doesn't exist
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = 'seating_plan_db' 
     AND TABLE_NAME = 'users' 
     AND COLUMN_NAME = 'updated_at') = 0,
    'ALTER TABLE users ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER created_at;',
    'SELECT ''updated_at column already exists'' as Status;'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Update existing users to have default role if null
UPDATE users SET role = 'student' WHERE role IS NULL;

-- Add missing columns to pdf_history table if they don't exist
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = 'seating_plan_db' 
     AND TABLE_NAME = 'pdf_history' 
     AND COLUMN_NAME = 'building') = 0,
    'ALTER TABLE pdf_history ADD COLUMN building VARCHAR(100) AFTER include_detained;',
    'SELECT ''building column already exists in pdf_history'' as Status;'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = 'seating_plan_db' 
     AND TABLE_NAME = 'pdf_history' 
     AND COLUMN_NAME = 'plan_details') = 0,
    'ALTER TABLE pdf_history ADD COLUMN plan_details TEXT AFTER building;',
    'SELECT ''plan_details column already exists in pdf_history'' as Status;'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Create missing tables if they don't exist

-- Password reset tokens table
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- System settings table
CREATE TABLE IF NOT EXISTS system_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    updated_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

-- Activity logs table
CREATE TABLE IF NOT EXISTS activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Login attempts table
CREATE TABLE IF NOT EXISTS login_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    ip_address VARCHAR(45),
    success BOOLEAN NOT NULL,
    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Email notifications table
CREATE TABLE IF NOT EXISTS email_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    recipient_email VARCHAR(100) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Rooms config table (fix column names)
CREATE TABLE IF NOT EXISTS rooms_config (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(50) NOT NULL,
    building VARCHAR(100),
    room_rows INT NOT NULL,
    room_columns INT NOT NULL,
    allowed_branches TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    branch VARCHAR(50) NOT NULL,
    section VARCHAR(10),
    is_detained BOOLEAN DEFAULT FALSE,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enhanced PDF History table
CREATE TABLE IF NOT EXISTS pdf_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    student_count INT NOT NULL,
    room_count INT NOT NULL,
    students_per_desk INT NOT NULL,
    include_detained BOOLEAN NOT NULL,
    building VARCHAR(100),
    plan_details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Now insert default data safely

-- Insert default admin user (password: admin123)
-- Generate proper bcrypt hash for 'admin123'
INSERT IGNORE INTO users (username, email, password_hash, full_name, role, is_active) VALUES 
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LsRyZy6DYgI2rk9jK', 'System Administrator', 'admin', TRUE);

-- Insert default system settings
INSERT IGNORE INTO system_settings (setting_key, setting_value, description) VALUES 
('app_name', 'Exam Seating Plan Generator', 'Application name displayed in UI'),
('students_per_desk_default', '1', 'Default number of students per desk'),
('include_detained_default', 'false', 'Default setting for including detained students'),
('session_timeout', '3600', 'Session timeout in seconds (1 hour)'),
('password_min_length', '6', 'Minimum password length requirement'),
('max_login_attempts', '5', 'Maximum failed login attempts before lockout'),
('lockout_duration', '900', 'Account lockout duration in seconds (15 minutes)'),
('email_notifications_enabled', 'true', 'Enable email notifications'),
('pdf_retention_days', '90', 'Number of days to retain PDF files'),
('app_version', '2.0.0', 'Current application version'),
('default_building', 'Main Building', 'Default building for room assignments');

-- Insert sample room configurations
INSERT IGNORE INTO rooms_config (room_number, building, room_rows, room_columns, allowed_branches, is_active) VALUES 
('101', 'Main Building', 5, 6, 'CSE;ECE;ME', TRUE),
('102', 'Main Building', 4, 7, 'CSE;ECE', TRUE),
('103', 'Main Building', 6, 5, 'ME;EEE;CE', TRUE),
('201', 'Science Block', 5, 8, 'CSE;IT', TRUE),
('202', 'Science Block', 4, 6, 'ECE;EEE', TRUE);

-- Insert sample students for testing
INSERT IGNORE INTO students (roll_number, name, branch, section, is_detained, email) VALUES 
('2021CSE001', 'John Doe', 'CSE', 'A', FALSE, 'john.doe@student.edu'),
('2021CSE002', 'Jane Smith', 'CSE', 'A', FALSE, 'jane.smith@student.edu'),
('2021ECE001', 'Mike Johnson', 'ECE', 'B', FALSE, 'mike.johnson@student.edu'),
('2021ECE002', 'Sarah Wilson', 'ECE', 'B', FALSE, 'sarah.wilson@student.edu'),
('2021ME001', 'David Brown', 'ME', 'A', FALSE, 'david.brown@student.edu'),
('2021ME002', 'Emily Davis', 'ME', 'A', TRUE, 'emily.davis@student.edu');

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_activity_logs_user_id ON activity_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_pdf_history_user_id ON pdf_history(user_id);

-- Display success message
SELECT 'Database migration completed successfully!' as Status;
SELECT 'Tables updated with missing columns' as Result;
SELECT 'Default admin user: admin / admin123' as Credentials;