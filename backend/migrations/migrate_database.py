#!/usr/bin/env python3
"""
Database migration script to add missing columns and fix schema issues
"""
import mysql.connector
from mysql.connector import Error

def get_database_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='seating_plan_db',
            user='root',
            password=''
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def migrate_database():
    """Migrate database schema to latest version"""
    connection = get_database_connection()
    if not connection:
        print("❌ Failed to connect to database")
        return False
    
    try:
        cursor = connection.cursor()
        
        print("🔄 Starting database migration...")
        
        # Check if 'role' column exists in users table
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'seating_plan_db' 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'role'
        """)
        
        role_column_exists = cursor.fetchone()
        
        if not role_column_exists:
            print("📝 Adding 'role' column to users table...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN role ENUM('admin', 'faculty', 'student') DEFAULT 'student' 
                AFTER full_name
            """)
            print("✅ Added 'role' column successfully")
        else:
            print("✅ 'role' column already exists")
        
        # Check if 'is_active' column exists
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'seating_plan_db' 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'is_active'
        """)
        
        is_active_column_exists = cursor.fetchone()
        
        if not is_active_column_exists:
            print("📝 Adding 'is_active' column to users table...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN is_active BOOLEAN DEFAULT TRUE 
                AFTER role
            """)
            print("✅ Added 'is_active' column successfully")
        else:
            print("✅ 'is_active' column already exists")
        
        # Check if 'updated_at' column exists
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'seating_plan_db' 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'updated_at'
        """)
        
        updated_at_column_exists = cursor.fetchone()
        
        if not updated_at_column_exists:
            print("📝 Adding 'updated_at' column to users table...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP 
                AFTER created_at
            """)
            print("✅ Added 'updated_at' column successfully")
        else:
            print("✅ 'updated_at' column already exists")
        
        # Update existing users to have default role if null
        cursor.execute("UPDATE users SET role = 'student' WHERE role IS NULL")
        
        # Check if admin user exists, if not create one
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        admin_exists = cursor.fetchone()
        
        if not admin_exists:
            print("📝 Creating default admin user...")
            import bcrypt
            admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name, role, is_active)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, ('admin', 'admin@example.com', admin_password, 'System Administrator', 'admin', True))
            print("✅ Created default admin user (admin/admin123)")
        else:
            print("✅ Admin user already exists")
        
        connection.commit()
        print("🎉 Database migration completed successfully!")
        return True
        
    except Error as e:
        print(f"❌ Migration error: {e}")
        connection.rollback()
        return False
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    print("🚀 Database Migration Tool")
    print("=" * 40)
    migrate_database()