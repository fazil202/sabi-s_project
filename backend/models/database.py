import mysql.connector
from mysql.connector import Error
import bcrypt
from datetime import datetime, timedelta
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

class Database:
    def get_all_student_emails(self):
        """Return a list of all student emails from the students table (non-empty only)."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT email FROM students WHERE email IS NOT NULL AND email != ''")
            results = cursor.fetchall()
            return [row[0] for row in results]
        except Exception as e:
            print(f"Error getting student emails: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    def import_students_from_csv(self, csv_path):
        """Import students from a CSV file into the students table."""
        import pandas as pd
        try:
            students = pd.read_csv(csv_path)
            cursor = self.connection.cursor()
            inserted = 0
            for _, row in students.iterrows():
                roll_number = str(row.get('Roll Number', row.get('roll_number', ''))).strip()
                name = str(row.get('Name', row.get('name', ''))).strip()
                branch = str(row.get('Branch', row.get('branch', ''))).strip()
                section = str(row.get('Section', row.get('section', ''))).strip() if 'Section' in row or 'section' in row else None
                is_detained = bool(row.get('detained', row.get('detained_status', False)))
                email = str(row.get('Email', row.get('email', ''))).strip() if 'Email' in row or 'email' in row else None
                if not roll_number or not name or not branch:
                    continue
                insert_query = """
                    INSERT INTO students (roll_number, name, branch, section, is_detained, email)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE name=VALUES(name), branch=VALUES(branch), section=VALUES(section), is_detained=VALUES(is_detained), email=VALUES(email)
                """
                cursor.execute(insert_query, (roll_number, name, branch, section, is_detained, email))
                inserted += 1
            self.connection.commit()
            cursor.close()
            return inserted
        except Exception as e:
            print(f"Error importing students from CSV: {e}")
            return 0
    def __init__(self):
        self.host = 'localhost'
        self.database = 'seating_plan_db'
        self.user = 'root'  # Change to your MySQL username
        self.password = ''  # Change to your MySQL password
        self.connection = None
        
        # Email configuration
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.email_username = 'seatgenerator.gprec@gmail.com'  # Configure this
        self.email_password = 'jhpj lkkv rjmp fzfc'  # Configure this
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def create_tables(self):
        """Create the necessary tables if they don't exist"""
        try:
            cursor = self.connection.cursor()
            
            # Users table with enhanced fields
            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                role ENUM('admin', 'faculty', 'student') DEFAULT 'student',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            
            # Password reset tokens table
            create_reset_tokens_table = """
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                token VARCHAR(255) UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                used BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            
            # System settings table
            create_settings_table = """
            CREATE TABLE IF NOT EXISTS system_settings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                setting_key VARCHAR(100) UNIQUE NOT NULL,
                setting_value TEXT,
                description TEXT,
                updated_by INT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (updated_by) REFERENCES users(id)
            )
            """
            
            # Rooms configuration table
            create_rooms_config_table = """
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
            )
            """
            
            # Students table
            create_students_table = """
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                roll_number VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                branch VARCHAR(50) NOT NULL,
                section VARCHAR(10),
                is_detained BOOLEAN DEFAULT FALSE,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # PDF History table (enhanced)
            create_pdf_history_table = """
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
            )
            """
            
            # Activity logs table
            create_activity_logs_table = """
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                action VARCHAR(100) NOT NULL,
                details TEXT,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
            """
            
            # Login attempts table
            create_login_attempts_table = """
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                ip_address VARCHAR(45),
                success BOOLEAN NOT NULL,
                attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Email notifications table
            create_notifications_table = """
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
            )
            """
            
            # Execute table creation
            cursor.execute(create_users_table)
            cursor.execute(create_reset_tokens_table)
            cursor.execute(create_settings_table)
            cursor.execute(create_rooms_config_table)
            cursor.execute(create_students_table)
            cursor.execute(create_pdf_history_table)
            cursor.execute(create_activity_logs_table)
            cursor.execute(create_login_attempts_table)
            cursor.execute(create_notifications_table)
            
            self.connection.commit()
            
            # Create default admin user and settings
            self.create_default_admin()
            self.create_default_settings()
            
            return True
        except Error as e:
            print(f"Error creating tables: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def create_default_admin(self):
        """Create a default admin user"""
        try:
            cursor = self.connection.cursor()
            
            # Check if admin user exists
            cursor.execute("SELECT id FROM users WHERE username = 'admin'")
            if cursor.fetchone():
                return  # Admin already exists
            
            # Create admin user
            password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
            
            insert_query = """
            INSERT INTO users (username, email, password_hash, full_name, role)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, ('admin', 'admin@example.com', password_hash, 'Administrator', 'admin'))
            self.connection.commit()
            
        except Error as e:
            print(f"Error creating default admin: {e}")
        finally:
            if cursor:
                cursor.close()
                
    def create_default_settings(self):
        """Create default system settings"""
        try:
            cursor = self.connection.cursor()
            
            default_settings = [
                ('students_per_desk', '1', 'Default number of students per desk'),
                ('include_detained', 'false', 'Include detained students in seating plans by default'),
                ('default_building', 'Main Building', 'Default building for seating arrangements'),
                ('session_timeout', '3600', 'Session timeout in seconds'),
                ('max_login_attempts', '5', 'Maximum login attempts before account lockout'),
                ('email_notifications', 'true', 'Enable email notifications'),
                ('password_min_length', '6', 'Minimum password length'),
                ('pdf_retention_days', '30', 'Number of days to retain PDF files')
            ]
            
            for key, value, description in default_settings:
                cursor.execute(
                    "INSERT IGNORE INTO system_settings (setting_key, setting_value, description) VALUES (%s, %s, %s)",
                    (key, value, description)
                )
            
            self.connection.commit()
            
        except Error as e:
            print(f"Error creating default settings: {e}")
        finally:
            if cursor:
                cursor.close()
    
    def authenticate_user(self, username, password):
        """Authenticate user login with enhanced security"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Log login attempt
            self.log_login_attempt(username, success=False)  # Will update to True if successful
            
            cursor.execute(
                "SELECT id, username, password_hash, full_name, role, is_active FROM users WHERE username = %s OR email = %s", 
                (username, username)
            )
            user = cursor.fetchone()
            
            if user and user['is_active'] and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                # Update login attempt to success
                self.log_login_attempt(username, success=True)
                
                # Log successful login activity
                self.log_activity(user['id'], 'LOGIN', f"User {username} logged in successfully")
                
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'full_name': user['full_name'],
                    'role': user['role']
                }
            
            # Log failed login activity
            self.log_activity(None, 'LOGIN_FAILED', f"Failed login attempt for username: {username}")
            return None
            
        except Error as e:
            print(f"Error authenticating user: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def create_user(self, username, email, password, full_name, role='student'):
        """Create a new user with enhanced validation"""
        try:
            cursor = self.connection.cursor()
            
            # Check if username or email already exists
            cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone():
                return False, "Username or email already exists"
            
            # Validate password strength
            if len(password) < int(self.get_setting('password_min_length', '6')):
                return False, f"Password must be at least {self.get_setting('password_min_length', '6')} characters long"
            
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Insert new user
            insert_query = """
            INSERT INTO users (username, email, password_hash, full_name, role)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (username, email, password_hash, full_name, role))
            self.connection.commit()
            
            # Log user creation activity
            user_id = cursor.lastrowid
            self.log_activity(user_id, 'USER_CREATED', f"New user {username} created with role {role}")
            
            return True, "User created successfully"
            
        except Error as e:
            print(f"Error creating user: {e}")
            return False, f"Error creating user: {e}"
        finally:
            if cursor:
                cursor.close()
    
    def save_pdf_history(self, user_id, filename, file_path, student_count, room_count, students_per_desk, include_detained, building=None):
        """Save PDF generation history"""
        try:
            cursor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO pdf_history (user_id, filename, file_path, student_count, room_count, students_per_desk, include_detained, building)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (user_id, filename, file_path, student_count, room_count, students_per_desk, include_detained, building))
            self.connection.commit()
            
            # Log PDF generation activity
            self.log_activity(user_id, 'PDF_GENERATED', f"PDF {filename} generated with {student_count} students in {room_count} rooms")
            
            return True
        except Error as e:
            print(f"Error saving PDF history: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def get_user_pdf_history(self, user_id):
        """Get PDF history for a user"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            SELECT id, filename, student_count, room_count, students_per_desk, include_detained, building, created_at
            FROM pdf_history
            WHERE user_id = %s
            ORDER BY created_at DESC
            """
            
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error getting PDF history: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def get_pdf_file_path(self, pdf_id, user_id):
        """Get PDF file path for download"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT file_path FROM pdf_history WHERE id = %s AND user_id = %s", (pdf_id, user_id))
            result = cursor.fetchone()
            
            return result[0] if result else None
        except Error as e:
            print(f"Error getting PDF file path: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    # Additional methods for enhanced functionality
    def log_activity(self, user_id, action, details, ip_address=None, user_agent=None):
        """Log user activity"""
        try:
            cursor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO activity_logs (user_id, action, details, ip_address, user_agent)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (user_id, action, details, ip_address, user_agent))
            self.connection.commit()
            
        except Error as e:
            print(f"Error logging activity: {e}")
        finally:
            if cursor:
                cursor.close()
    
    def log_login_attempt(self, username, success=False, ip_address=None):
        """Log login attempts"""
        try:
            cursor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO login_attempts (username, ip_address, success)
            VALUES (%s, %s, %s)
            """
            
            cursor.execute(insert_query, (username, ip_address, success))
            self.connection.commit()
            
        except Error as e:
            print(f"Error logging login attempt: {e}")
        finally:
            if cursor:
                cursor.close()
    
    def get_setting(self, key, default_value=None):
        """Get system setting value"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT setting_value FROM system_settings WHERE setting_key = %s", (key,))
            result = cursor.fetchone()
            
            return result[0] if result else default_value
        except Error as e:
            print(f"Error getting setting: {e}")
            return default_value
        finally:
            if cursor:
                cursor.close()
    
    def update_setting(self, key, value, user_id=None):
        """Update system setting"""
        try:
            cursor = self.connection.cursor()
            
            update_query = """
            UPDATE system_settings 
            SET setting_value = %s, updated_by = %s, updated_at = NOW()
            WHERE setting_key = %s
            """
            
            cursor.execute(update_query, (value, user_id, key))
            self.connection.commit()
            
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating setting: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        try:
            cursor = self.connection.cursor()
            
            # Verify old password
            cursor.execute("SELECT password_hash FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            
            if not result or not bcrypt.checkpw(old_password.encode('utf-8'), result[0].encode('utf-8')):
                return False, "Current password is incorrect"
            
            # Validate new password
            if len(new_password) < int(self.get_setting('password_min_length', '6')):
                return False, f"Password must be at least {self.get_setting('password_min_length', '6')} characters long"
            
            # Update password
            new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            
            cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (new_password_hash, user_id))
            self.connection.commit()
            
            # Log activity
            self.log_activity(user_id, 'PASSWORD_CHANGED', 'User changed password')
            
            return True, "Password changed successfully"
            
        except Error as e:
            print(f"Error changing password: {e}")
            return False, f"Error changing password: {e}"
        finally:
            if cursor:
                cursor.close()
    
    def create_password_reset_token(self, email):
        """Create password reset token"""
        try:
            cursor = self.connection.cursor()
            
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if not user:
                return False, "Email not found"
            
            user_id = user[0]
            
            # Generate token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=1)
            
            # Save token
            insert_query = """
            INSERT INTO password_reset_tokens (user_id, token, expires_at)
            VALUES (%s, %s, %s)
            """
            
            cursor.execute(insert_query, (user_id, token, expires_at))
            self.connection.commit()
            
            # Log activity
            self.log_activity(user_id, 'PASSWORD_RESET_REQUESTED', 'Password reset token generated')
            
            return True, token
            
        except Error as e:
            print(f"Error creating reset token: {e}")
            return False, f"Error creating reset token: {e}"
        finally:
            if cursor:
                cursor.close()
    
    def reset_password_with_token(self, token, new_password):
        """Reset password using token"""
        try:
            cursor = self.connection.cursor()
            
            # Verify token
            cursor.execute("""
                SELECT user_id FROM password_reset_tokens 
                WHERE token = %s AND expires_at > NOW() AND used = FALSE
            """, (token,))
            
            result = cursor.fetchone()
            if not result:
                return False, "Invalid or expired token"
            
            user_id = result[0]
            
            # Validate new password
            if len(new_password) < int(self.get_setting('password_min_length', '6')):
                return False, f"Password must be at least {self.get_setting('password_min_length', '6')} characters long"
            
            # Update password
            new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            
            cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (new_password_hash, user_id))
            
            # Mark token as used
            cursor.execute("UPDATE password_reset_tokens SET used = TRUE WHERE token = %s", (token,))
            
            self.connection.commit()
            
            # Log activity
            self.log_activity(user_id, 'PASSWORD_RESET', 'Password reset using token')
            
            return True, "Password reset successfully"
            
        except Error as e:
            print(f"Error resetting password: {e}")
            return False, f"Error resetting password: {e}"
        finally:
            if cursor:
                cursor.close()
    
    def send_email(self, to_email, subject, body, pdf_path=None):
        """Send email notification, optionally with PDF attachment. Returns (success, error_message)"""
        try:
            from email.mime.base import MIMEBase
            from email import encoders
            msg = MIMEMultipart()
            msg['From'] = self.email_username
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'html'))

            # Attach PDF if provided
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(pdf_path)}"')
                msg.attach(part)

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_username, self.email_password)

            text = msg.as_string()
            server.sendmail(self.email_username, to_email, text)
            server.quit()

            return True, None
        except Exception as e:
            print(f"Error sending email: {e}")
            return False, str(e)
    
    def get_users_by_role(self, role=None):
        """Get users filtered by role"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if role:
                cursor.execute("SELECT id, username, email, full_name, role, is_active, created_at FROM users WHERE role = %s", (role,))
            else:
                cursor.execute("SELECT id, username, email, full_name, role, is_active, created_at FROM users")
            
            return cursor.fetchall()
        except Error as e:
            print(f"Error getting users: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def update_user_role(self, user_id, new_role, updated_by):
        """Update user role"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
            self.connection.commit()
            
            # Log activity
            self.log_activity(updated_by, 'ROLE_UPDATED', f"User {user_id} role changed to {new_role}")
            
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating user role: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
    
    def get_activity_logs(self, user_id=None, limit=100):
        """Get activity logs"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if user_id:
                cursor.execute("""
                    SELECT al.*, u.username 
                    FROM activity_logs al 
                    LEFT JOIN users u ON al.user_id = u.id 
                    WHERE al.user_id = %s 
                    ORDER BY al.created_at DESC 
                    LIMIT %s
                """, (user_id, limit))
            else:
                cursor.execute("""
                    SELECT al.*, u.username 
                    FROM activity_logs al 
                    LEFT JOIN users u ON al.user_id = u.id 
                    ORDER BY al.created_at DESC 
                    LIMIT %s
                """, (limit,))
            
            return cursor.fetchall()
        except Error as e:
            print(f"Error getting activity logs: {e}")
            return []
        finally:
            if cursor:
                cursor.close()