# Simple Login Window for ClassTrack System
# This is a beginner-friendly login screen
# Easy to understand and modify

import tkinter as tk
from tkinter import messagebox
from database_config import DatabaseConfig

class LoginWindow:
    def __init__(self):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("ClassTrack Login")
        self.window.geometry("800x500")
        self.window.configure(bg='#f0f0f0')
        
        # Center window on screen
        self.center_window()
        
        # Connect to database
        self.db = DatabaseConfig()
        
        # Create the login screen
        self.create_login_screen()
    
    def center_window(self):
        """Put window in center of screen"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 500) // 2
        self.window.geometry(f"800x500+{x}+{y}")
    
    def create_login_screen(self):
        """Create the login interface - split into welcome and login sections"""
        
        # Main container
        main_frame = tk.Frame(self.window, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)
        
        # LEFT SIDE - Welcome Section
        welcome_side = tk.Frame(main_frame, bg='#4CAF50', width=400)
        welcome_side.pack(side='left', fill='both', expand=True)
        
        # Welcome content
        welcome_frame = tk.Frame(welcome_side, bg='#4CAF50')
        welcome_frame.pack(expand=True)
        
        # School logo and name
        tk.Label(
            welcome_frame,
            text="🏫 ClassTrack",
            font=("Arial", 24, "bold"),
            bg='#4CAF50',
            fg='white'
        ).pack(pady=20)
        
        # Welcome message
        tk.Label(
            welcome_frame,
            text="Welcome to\nStudent Management System",
            font=("Arial", 16),
            bg='#4CAF50',
            fg='white',
            justify='center'
        ).pack(pady=10)
        
        # Simple feature list
        features = [
            "• Manage Students",
            "• Track Attendance", 
            "• Record Marks",
            "• Generate Reports"
        ]
        
        for feature in features:
            tk.Label(
                welcome_frame,
                text=feature,
                font=("Arial", 12),
                bg='#4CAF50',
                fg='white',
                anchor='w'
            ).pack(pady=3)
        
        # RIGHT SIDE - Login Form
        login_side = tk.Frame(main_frame, bg='white', width=400)
        login_side.pack(side='right', fill='both', expand=True)
        
        # Login form
        login_frame = tk.Frame(login_side, bg='white')
        login_frame.pack(expand=True)
        
        # Login title
        tk.Label(
            login_frame,
            text="Login",
            font=("Arial", 20, "bold"),
            bg='white',
            fg='#333333'
        ).pack(pady=(40, 30))
        
        # Username input
        tk.Label(
            login_frame,
            text="Username:",
            font=("Arial", 12),
            bg='white',
            fg='#333333'
        ).pack(anchor='w', padx=50)
        
        self.username_entry = tk.Entry(
            login_frame,
            font=("Arial", 12),
            width=30,
            bg='#f9f9f9',
            relief='solid',
            bd=1
        )
        self.username_entry.pack(pady=(5, 15), padx=50)
        
        # Password input
        tk.Label(
            login_frame,
            text="Password:",
            font=("Arial", 12),
            bg='white',
            fg='#333333'
        ).pack(anchor='w', padx=50)
        
        self.password_entry = tk.Entry(
            login_frame,
            font=("Arial", 12),
            width=30,
            show="*",
            bg='#f9f9f9',
            relief='solid',
            bd=1
        )
        self.password_entry.pack(pady=(5, 15), padx=50)
        
        # Role selection
        tk.Label(
            login_frame,
            text="I am a:",
            font=("Arial", 12),
            bg='white',
            fg='#333333'
        ).pack(anchor='w', padx=50)
        
        # Simple radio buttons for role
        self.role_var = tk.StringVar(value="student")
        
        role_frame = tk.Frame(login_frame, bg='white')
        role_frame.pack(pady=(5, 20))
        
        tk.Radiobutton(
            role_frame,
            text="Student",
            variable=self.role_var,
            value="student",
            font=("Arial", 11),
            bg='white'
        ).pack(side='left', padx=10)
        
        tk.Radiobutton(
            role_frame,
            text="Teacher",
            variable=self.role_var,
            value="teacher",
            font=("Arial", 11),
            bg='white'
        ).pack(side='left', padx=10)
        
        tk.Radiobutton(
            role_frame,
            text="Admin",
            variable=self.role_var,
            value="admin",
            font=("Arial", 11),
            bg='white'
        ).pack(side='left', padx=10)
        
        # Login button
        login_button = tk.Button(
            login_frame,
            text="Login",
            font=("Arial", 14, "bold"),
            bg='#4CAF50',
            fg='white',
            width=20,
            height=2,
            cursor='hand2',
            command=self.do_login
        )
        login_button.pack(pady=20)
        
        # Demo info
        demo_frame = tk.Frame(login_frame, bg='white')
        demo_frame.pack(pady=10)
        
        tk.Label(
            demo_frame,
            text="Demo Login Info:",
            font=("Arial", 10, "bold"),
            bg='white',
            fg='#666666'
        ).pack()
        
        tk.Label(
            demo_frame,
            text="Admin: admin / admin123\nTeacher: teacher1 / teacher123\nStudent: student1 / student123",
            font=("Arial", 9),
            bg='white',
            fg='#888888',
            justify='center'
        ).pack()
        
        # Press Enter to login
        self.window.bind('<Return>', lambda event: self.do_login())
        
        # Focus on username field
        self.username_entry.focus()
    
    def do_login(self):
        """Check username and password, then open main system"""
        
        # Get what user typed
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()
        
        # Check if fields are empty
        if not username:
            messagebox.showerror("Error", "Please enter your username!")
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter your password!")
            return
        
        # Connect to database and check login
        connection = self.db.get_connection()
        if not connection:
            messagebox.showerror("Error", "Cannot connect to database!")
            return
        
        try:
            cursor = connection.cursor()
            
            # Search for user in database
            query = "SELECT user_id, full_name, role FROM users WHERE username = %s AND password = %s AND role = %s"
            cursor.execute(query, (username, password, role))
            user_data = cursor.fetchone()
            
            if user_data:
                # Login successful
                user_id, full_name, user_role = user_data
                
                messagebox.showinfo("Success", f"Welcome back, {full_name}!")
                
                # Close login window
                self.window.destroy()
                
                # Open main dashboard
                from dashboard import Dashboard
                dashboard = Dashboard(user_id, full_name, user_role)
                dashboard.run()
            else:
                # Login failed
                messagebox.showerror("Login Failed", "Wrong username, password, or role!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
        
        finally:
            cursor.close()
            connection.close()
    
    def start(self):
        """Start the login window"""
        self.window.mainloop()

# Main program starts here
if __name__ == "__main__":
    # Setup database
    database = DatabaseConfig()
    database.create_tables()
    
    # Start login window
    login = LoginWindow()
    login.start()
