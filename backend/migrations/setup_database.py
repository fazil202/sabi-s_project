import mysql.connector
from mysql.connector import Error

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Change to your MySQL username
            password=''   # Change to your MySQL password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS seating_plan_db")
            print("Database 'seating_plan_db' created successfully!")
            
            cursor.close()
            connection.close()
            
            return True
    except Error as e:
        print(f"Error creating database: {e}")
        return False

def setup_database():
    """Setup the complete database with tables"""
    # First create the database
    if not create_database():
        return False
    
    # Now create tables using our Database class
    try:
        from database import Database
        
        db = Database()
        if db.connect():
            if db.create_tables():
                print("Database setup completed successfully!")
                print("Default admin user created with username: admin, password: admin123")
                db.disconnect()
                return True
            else:
                print("Error creating tables")
                db.disconnect()
                return False
        else:
            print("Error connecting to database")
            return False
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

if __name__ == "__main__":
    print("Setting up database for Exam Seating Plan Generator...")
    print("Make sure MySQL is running and update the credentials in database.py")
    print("-" * 60)
    
    if setup_database():
        print("\n✅ Database setup completed successfully!")
        print("You can now run the application with: python app.py")
    else:
        print("\n❌ Database setup failed!")
        print("Please check your MySQL connection and credentials.")