# main.py - Main application entry point for Class Track System
"""
Class Track - Student Management System
A comprehensive GUI-based application for managing students, attendance, and marks.

Created by: BCSIT 2nd Semester Students
Features:
- Student Management
- Attendance Tracking
- Marks/Grades Management
- Reports Generation
- Role-based Access (Admin, Teacher, Student)
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_modules = [
        'mysql.connector',
        'tkinter',
        'datetime'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = f"Missing required modules: {', '.join(missing_modules)}\n"
        error_msg += "Please install them using: pip install -r requirements.txt"
        print(error_msg)
        return False
    return True

def setup_database():
    """Setup database connection and create tables"""
    try:
        from database_config import DatabaseConfig
        
        print("Setting up database...")
        db = DatabaseConfig()
        
        # Test connection
        connection = db.get_connection()
        if connection:
            print("✓ Database connection successful!")
            connection.close()
            
            # Create tables
            db.create_tables()
            print("✓ Database tables created/verified!")
            return True
        else:
            print("✗ Database connection failed!")
            print("Please make sure MySQL server is running and accessible.")
            return False
            
    except Exception as e:
        print(f"✗ Database setup error: {str(e)}")
        return False

def show_startup_info():
    """Show startup information"""
    info = """
    
                        CLASS TRACK                         
                    Student Management System                     
   
     Features:                                                   
      • Student Registration & Management                         
      • Attendance Tracking                                       
      • Marks & Grades Management                                 
      • Role-based Access Control                                 
      • Reports Generation                                         
  
      Default Login Credentials:                                  
      Admin    → Username: admin     | Password: admin123         
      Teacher  → Username: teacher1  | Password: teacher123       
    
    """
    print(info)

def show_docker_setup_info():
    """Show Docker setup information"""
    docker_info = """
    
                      DOCKER SETUP REQUIRED                     
    
     To start the MySQL database, run:                          
                                                                  
      docker-compose up -d                                      
                                                                
     This will start:                                         
     • MySQL Server (Port 3306)                               
     • phpMyAdmin (Port 8080)                                   
                                                                  
      Access phpMyAdmin at: http://localhost:8080               
      Username: admin | Password: admin123                       ║
    
    """
    print(docker_info)

def main():
    """Main application entry point"""
    try:
        # Show startup info
        show_startup_info()
        
        # Check dependencies
        print("Checking dependencies...")
        if not check_dependencies():
            input("Press Enter to exit...")
            return
        
        print("✓ All dependencies found!")
        
        # Setup database
        if not setup_database():
            print("\n" + "="*60)
            show_docker_setup_info()
            print("Please start the Docker containers and try again.")
            input("Press Enter to exit...")
            return
        
        # Start the application
        print("Starting Class Track System...")
        print("="*60)
        
        from login import LoginWindow
        
        # Create and run login window
        app = LoginWindow()
        app.start()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except Exception as e:
        print(f"Application error: {str(e)}")
        messagebox.showerror("Error", f"Application failed to start: {str(e)}")
    finally:
        print("Class Track System closed.")

if __name__ == "__main__":
    main()
