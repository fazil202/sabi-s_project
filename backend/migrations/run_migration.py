#!/usr/bin/env python3
"""
Python script to run database migration
"""
import mysql.connector
from mysql.connector import Error

def run_migration():
    """Run the database migration script"""
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host='localhost',
            database='seating_plan_db',
            user='root',
            password=''  # Update with your MySQL password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("🔄 Starting database migration...")
            
            # Read migration SQL file
            with open('database_migration.sql', 'r', encoding='utf-8') as file:
                sql_script = file.read()
            
            # Split SQL statements
            statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
            
            for i, statement in enumerate(statements):
                if statement and not statement.startswith('--'):
                    try:
                        cursor.execute(statement)
                        connection.commit()
                        print(f"✅ Executed statement {i+1}/{len(statements)}")
                    except Error as e:
                        if "already exists" in str(e) or "Duplicate" in str(e):
                            print(f"⚠️  Statement {i+1}: Already exists - {e}")
                        else:
                            print(f"❌ Error in statement {i+1}: {e}")
                            print(f"Statement: {statement[:100]}...")
            
            print("🎉 Migration completed successfully!")
            
    except Error as e:
        print(f"❌ Database connection error: {e}")
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Database connection closed")

if __name__ == "__main__":
    run_migration()