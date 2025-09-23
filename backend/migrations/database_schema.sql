-- =========================================
-- EXAM SEATING PLAN GENERATOR DATABASE SCHEMA
-- Version: 2.0.0
-- Date: September 23, 2025
-- =========================================

-- Create database
CREATE DATABASE IF NOT EXISTS seating_plan_db;
USE seating_plan_db;

-- =========================================
-- TABLE: users
-- Description: User management with role-based access
-- =========================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('admin', 'faculty', 'student') DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_active (is_active)
);

-- =========================================
-- TABLE: password_reset_tokens
-- Description: Secure password reset functionality
-- =========================================
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_token (token),
    INDEX idx_expires (expires_at),
    INDEX idx_used (used)
);

-- =========================================
-- TABLE: system_settings
-- Description: Configurable system settings
-- =========================================
CREATE TABLE IF NOT EXISTS system_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    updated_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (updated_by) REFERENCES users(id),
    INDEX idx_setting_key (setting_key)
);

-- =========================================
-- TABLE: rooms_config
-- Description: Room configuration and layout
-- =========================================
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
    
    FOREIGN KEY (created_by) REFERENCES users(id),
    INDEX idx_room_number (room_number),
    INDEX idx_building (building),
    INDEX idx_active_rooms (is_active)
);

-- =========================================
-- TABLE: students
-- Description: Student information and details
-- =========================================
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    branch VARCHAR(50) NOT NULL,
    section VARCHAR(10),
    is_detained BOOLEAN DEFAULT FALSE,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_roll_number (roll_number),
    INDEX idx_branch (branch),
    INDEX idx_section (section),
    INDEX idx_detained (is_detained)
);

-- =========================================
-- TABLE: pdf_history
-- Description: History of generated seating plans
-- =========================================
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
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_filename (filename),
    INDEX idx_created_at (created_at)
);

-- =========================================
-- TABLE: activity_logs
-- Description: System activity and audit logging
-- =========================================
CREATE TABLE IF NOT EXISTS activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at),
    INDEX idx_ip_address (ip_address)
);

-- =========================================
-- TABLE: login_attempts
-- Description: Login attempt monitoring for security
-- =========================================
CREATE TABLE IF NOT EXISTS login_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    ip_address VARCHAR(45),
    success BOOLEAN NOT NULL,
    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_ip_address (ip_address),
    INDEX idx_success (success),
    INDEX idx_attempt_time (attempt_time)
);

-- =========================================
-- TABLE: email_notifications
-- Description: Email notification queue and tracking
-- =========================================
CREATE TABLE IF NOT EXISTS email_notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    recipient_email VARCHAR(100) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    sent BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_recipient (recipient_email),
    INDEX idx_sent (sent),
    INDEX idx_created_at (created_at)
);

-- =========================================
-- DEFAULT DATA INSERTION
-- =========================================

-- Insert default admin user (password: admin123)
-- Note: This is a bcrypt hash of 'admin123'
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
('backup_frequency', 'daily', 'Database backup frequency'),
('maintenance_mode', 'false', 'System maintenance mode flag'),
('default_building', 'Main Building', 'Default building for room assignments'),
('app_version', '2.0.0', 'Current application version'),
('last_backup', '', 'Timestamp of last database backup'),
('system_email', 'noreply@seatingplan.edu', 'System email address for notifications');

-- Insert sample room configurations
INSERT IGNORE INTO rooms_config (room_number, building, room_rows, room_columns, allowed_branches, is_active) VALUES 
('101', 'Main Building', 5, 6, 'CSE;ECE;ME', TRUE),
('102', 'Main Building', 4, 7, 'CSE;ECE', TRUE),
('103', 'Main Building', 6, 5, 'ME;EEE;CE', TRUE),
('201', 'Science Block', 5, 8, 'CSE;IT', TRUE),
('202', 'Science Block', 4, 6, 'ECE;EEE', TRUE),
('301', 'Engineering Block', 6, 6, 'ME;CE;MECH', TRUE);

-- Insert sample students (for testing)
INSERT IGNORE INTO students (roll_number, name, branch, section, is_detained, email) VALUES 
('2021CSE001', 'John Doe', 'CSE', 'A', FALSE, 'john.doe@student.edu'),
('2021CSE002', 'Jane Smith', 'CSE', 'A', FALSE, 'jane.smith@student.edu'),
('2021ECE001', 'Mike Johnson', 'ECE', 'B', FALSE, 'mike.johnson@student.edu'),
('2021ECE002', 'Sarah Wilson', 'ECE', 'B', FALSE, 'sarah.wilson@student.edu'),
('2021ME001', 'David Brown', 'ME', 'A', FALSE, 'david.brown@student.edu'),
('2021ME002', 'Emily Davis', 'ME', 'A', TRUE, 'emily.davis@student.edu'),
('2021EEE001', 'Robert Miller', 'EEE', 'C', FALSE, 'robert.miller@student.edu'),
('2021IT001', 'Lisa Anderson', 'IT', 'A', FALSE, 'lisa.anderson@student.edu');

-- =========================================
-- VIEWS FOR REPORTING (OPTIONAL)
-- =========================================

-- View for active users summary
CREATE OR REPLACE VIEW active_users_summary AS
SELECT 
    role,
    COUNT(*) as user_count,
    COUNT(CASE WHEN is_active = TRUE THEN 1 END) as active_count
FROM users 
GROUP BY role;

-- View for recent activity
CREATE OR REPLACE VIEW recent_activity AS
SELECT 
    al.id,
    u.username,
    u.full_name,
    al.action,
    al.details,
    al.ip_address,
    al.created_at
FROM activity_logs al
LEFT JOIN users u ON al.user_id = u.id
ORDER BY al.created_at DESC
LIMIT 100;

-- View for PDF generation statistics
CREATE OR REPLACE VIEW pdf_statistics AS
SELECT 
    DATE(created_at) as generation_date,
    COUNT(*) as total_pdfs,
    SUM(student_count) as total_students,
    SUM(room_count) as total_rooms,
    AVG(students_per_desk) as avg_students_per_desk
FROM pdf_history
GROUP BY DATE(created_at)
ORDER BY generation_date DESC;

-- =========================================
-- STORED PROCEDURES (OPTIONAL)
-- =========================================

DELIMITER //

-- Procedure to clean old login attempts
CREATE PROCEDURE CleanOldLoginAttempts()
BEGIN
    DELETE FROM login_attempts 
    WHERE attempt_time < DATE_SUB(NOW(), INTERVAL 30 DAY);
END //

-- Procedure to clean old activity logs
CREATE PROCEDURE CleanOldActivityLogs()
BEGIN
    DELETE FROM activity_logs 
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
END //

-- Procedure to get user statistics
CREATE PROCEDURE GetUserStatistics()
BEGIN
    SELECT 
        COUNT(*) as total_users,
        COUNT(CASE WHEN role = 'admin' THEN 1 END) as admin_count,
        COUNT(CASE WHEN role = 'faculty' THEN 1 END) as faculty_count,
        COUNT(CASE WHEN role = 'student' THEN 1 END) as student_count,
        COUNT(CASE WHEN is_active = TRUE THEN 1 END) as active_users,
        COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as new_users_this_month
    FROM users;
END //

DELIMITER ;

-- =========================================
-- TRIGGERS FOR AUDIT TRAIL (OPTIONAL)
-- =========================================

DELIMITER //

-- Trigger to log user updates
CREATE TRIGGER user_update_audit 
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    INSERT INTO activity_logs (user_id, action, details, created_at)
    VALUES (NEW.id, 'USER_UPDATED', 
           CONCAT('User profile updated: ', 
                 CASE 
                   WHEN OLD.username != NEW.username THEN CONCAT('username changed from ', OLD.username, ' to ', NEW.username, '; ')
                   ELSE ''
                 END,
                 CASE 
                   WHEN OLD.email != NEW.email THEN CONCAT('email changed from ', OLD.email, ' to ', NEW.email, '; ')
                   ELSE ''
                 END,
                 CASE 
                   WHEN OLD.role != NEW.role THEN CONCAT('role changed from ', OLD.role, ' to ', NEW.role, '; ')
                   ELSE ''
                 END,
                 CASE 
                   WHEN OLD.is_active != NEW.is_active THEN CONCAT('active status changed to ', NEW.is_active, '; ')
                   ELSE ''
                 END
           ), NOW());
END //

DELIMITER ;

-- =========================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- =========================================

-- Composite indexes for frequently queried combinations
CREATE INDEX idx_users_role_active ON users(role, is_active);
CREATE INDEX idx_activity_user_action ON activity_logs(user_id, action);
CREATE INDEX idx_login_attempts_user_time ON login_attempts(username, attempt_time);
CREATE INDEX idx_pdf_history_user_date ON pdf_history(user_id, created_at);

-- =========================================
-- GRANTS AND PERMISSIONS (CUSTOMIZE AS NEEDED)
-- =========================================

-- Create application user (optional)
-- CREATE USER 'seating_app'@'localhost' IDENTIFIED BY 'secure_password_here';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON seating_plan_db.* TO 'seating_app'@'localhost';
-- FLUSH PRIVILEGES;

-- =========================================
-- END OF SCHEMA
-- =========================================

-- Display completion message
SELECT 'Database schema created successfully!' as Status;
SELECT 'Default admin user: admin / admin123' as DefaultCredentials;
SELECT 'Please change default passwords in production!' as SecurityNote;