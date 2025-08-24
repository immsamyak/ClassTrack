# Simple Dashboard for ClassTrack System
# Easy to understand main screen after login
# Shows different options based on user role (Student/Teacher/Admin)

import tkinter as tk
from tkinter import messagebox
from database_config import DatabaseConfig

class Dashboard:
    def __init__(self, user_id, full_name, role):
        # Store user information
        self.user_id = user_id
        self.full_name = full_name
        self.role = role
        self.db = DatabaseConfig()
        
        # Create main window
        self.window = tk.Tk()
        self.window.title(f"ClassTrack Dashboard - {role.title()}")
        self.window.geometry("1000x700")
        self.window.configure(bg='#f0f0f0')
        
        # Center the window
        self.center_window()
        
        # Create the dashboard
        self.create_dashboard()
    
    def center_window(self):
        """Put window in center of screen"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 700) // 2
        self.window.geometry(f"1000x700+{x}+{y}")
    
    def create_dashboard(self):
        """Create the main dashboard with header and navigation"""
        # TOP SECTION - Header with welcome and logout
        header = tk.Frame(self.window, bg='#3498db', height=70)
        header.pack(fill='x', side='top')
        header.pack_propagate(False)
        
        # Welcome message
        tk.Label(
            header,
            text=f"Welcome back, {self.full_name}!",
            font=("Arial", 16, "bold"),
            bg='#3498db',
            fg='white'
        ).pack(side='left', padx=20, pady=20)
        
        # Role badge
        tk.Label(
            header,
            text=f"({self.role.upper()})",
            font=("Arial", 12),
            bg='#2980b9',
            fg='white',
            padx=10,
            pady=5
        ).pack(side='left', pady=20)
        
        # Logout button
        tk.Button(
            header,
            text="Logout",
            font=("Arial", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            command=self.logout,
            padx=20
        ).pack(side='right', padx=20, pady=20)
        
        # MAIN SECTION - Split into sidebar and content
        main_area = tk.Frame(self.window, bg='#f0f0f0')
        main_area.pack(fill='both', expand=True, padx=10, pady=10)
        
        # LEFT SIDEBAR - Navigation buttons
        sidebar = tk.Frame(main_area, bg='#34495e', width=200)
        sidebar.pack(side='left', fill='y', padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # RIGHT CONTENT AREA - Main content
        self.content_area = tk.Frame(main_area, bg='white')
        self.content_area.pack(side='right', fill='both', expand=True)
        
        # Create navigation buttons based on user role
        self.create_navigation(sidebar)
        
        # Show home screen by default
        self.show_home()
    
    def create_navigation(self, sidebar):
        """Create navigation buttons based on user role"""
        # Navigation title
        tk.Label(
            sidebar,
            text="Navigation",
            font=("Arial", 14, "bold"),
            bg='#34495e',
            fg='white'
        ).pack(pady=20)
        
        # Home button (for everyone)
        self.create_nav_button(sidebar, "🏠 Home", self.show_home)
        
        # Different buttons for different roles
        if self.role == 'admin':
            # Admin can see everything
            self.create_nav_button(sidebar, "👥 Manage Students", self.show_students)
            self.create_nav_button(sidebar, "👨‍🏫 Manage Teachers", self.show_teachers)
            self.create_nav_button(sidebar, "📚 Manage Subjects", self.show_subjects)
            self.create_nav_button(sidebar, "📊 View Attendance", self.show_attendance)
            self.create_nav_button(sidebar, "📝 View Marks", self.show_marks)
            self.create_nav_button(sidebar, "📈 Reports", self.show_reports)
            self.create_nav_button(sidebar, "⚙️ Settings", self.show_settings)
            
        elif self.role == 'teacher':
            # Teachers can manage attendance and marks
            self.create_nav_button(sidebar, "👥 View Students", self.show_students)
            self.create_nav_button(sidebar, "📊 Mark Attendance", self.show_attendance)
            self.create_nav_button(sidebar, "📝 Enter Marks", self.show_marks)
            self.create_nav_button(sidebar, "📚 My Subjects", self.show_subjects)
            self.create_nav_button(sidebar, "📈 Class Reports", self.show_reports)
            
        elif self.role == 'student':
            # Students can only view their own data
            self.create_nav_button(sidebar, "📊 My Attendance", self.show_my_attendance)
            self.create_nav_button(sidebar, "📝 My Marks", self.show_my_marks)
            self.create_nav_button(sidebar, "📚 My Subjects", self.show_my_subjects)
        
        # AI Assistant for everyone
        self.create_nav_button(sidebar, "🤖 AI Assistant", self.show_ai_assistant)
    
    def create_nav_button(self, parent, text, command):
        """Create a simple navigation button"""
        button = tk.Button(
            parent,
            text=text,
            font=("Arial", 11),
            bg='#34495e',
            fg='white',
            relief='flat',
            width=18,
            height=2,
            command=command,
            cursor='hand2'
        )
        button.pack(pady=5, padx=10, fill='x')
        
        # Change color when mouse hovers over button
        def on_hover(event):
            button.config(bg='#5d6d7e')
        
        def on_leave(event):
            button.config(bg='#34495e')
        
        button.bind("<Enter>", on_hover)
        button.bind("<Leave>", on_leave)
    
    def clear_content(self):
        """Clear the main content area"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def show_home(self):
        """Show the home/dashboard overview"""
        self.clear_content()
        
        # Welcome title
        tk.Label(
            self.content_area,
            text=f"Dashboard Overview - {self.role.title()}",
            font=("Arial", 18, "bold"),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=30)
        
        # Show statistics based on role
        stats_frame = tk.Frame(self.content_area, bg='white')
        stats_frame.pack(pady=20)
        
        if self.role == 'admin':
            self.show_admin_stats(stats_frame)
        elif self.role == 'teacher':
            self.show_teacher_stats(stats_frame)
        elif self.role == 'student':
            self.show_student_stats(stats_frame)
    
    def show_admin_stats(self, parent):
        """Show statistics for admin"""
        # Get counts from database
        connection = self.db.get_connection()
        if connection:
            cursor = connection.cursor()
            
            # Count students
            cursor.execute("SELECT COUNT(*) FROM students")
            student_count = cursor.fetchone()[0]
            
            # Count teachers  
            cursor.execute("SELECT COUNT(*) FROM teachers")
            teacher_count = cursor.fetchone()[0]
            
            # Count subjects
            cursor.execute("SELECT COUNT(*) FROM subjects")
            subject_count = cursor.fetchone()[0]
            
            cursor.close()
            connection.close()
            
            # Create stat cards
            self.create_stat_card(parent, "Total Students", student_count, "#3498db", 0, 0)
            self.create_stat_card(parent, "Total Teachers", teacher_count, "#27ae60", 0, 1)
            self.create_stat_card(parent, "Total Subjects", subject_count, "#f39c12", 0, 2)
    
    def show_teacher_stats(self, parent):
        """Show statistics for teacher"""
        tk.Label(
            parent,
            text="Teacher Dashboard",
            font=("Arial", 14),
            bg='white'
        ).pack(pady=20)
        
        tk.Label(
            parent,
            text="• Mark student attendance\n• Enter student marks\n• View class reports",
            font=("Arial", 12),
            bg='white',
            justify='left'
        ).pack()
    
    def show_student_stats(self, parent):
        """Show statistics for student"""
        tk.Label(
            parent,
            text="Student Dashboard",
            font=("Arial", 14),
            bg='white'
        ).pack(pady=20)
        
        tk.Label(
            parent,
            text="• View your attendance\n• Check your marks\n• See your subjects",
            font=("Arial", 12),
            bg='white',
            justify='left'
        ).pack()
    
    def create_stat_card(self, parent, title, value, color, row, col):
        """Create a simple statistics card"""
        card = tk.Frame(parent, bg=color, width=180, height=100)
        card.grid(row=row, column=col, padx=20, pady=10)
        card.pack_propagate(False)
        
        # Number
        tk.Label(
            card,
            text=str(value),
            font=("Arial", 20, "bold"),
            bg=color,
            fg='white'
        ).pack(pady=(15, 0))
        
        # Title
        tk.Label(
            card,
            text=title,
            font=("Arial", 10),
            bg=color,
            fg='white'
        ).pack()
    
    # Navigation functions - these will open different modules
    def show_students(self):
        """Show student management"""
        self.clear_content()
        try:
            from student_management import StudentManagement
            StudentManagement(self.content_area, self.db, self.user_id)
        except Exception as e:
            self.show_error("Students module not available yet")
    
    def show_teachers(self):
        """Show teacher management"""
        self.clear_content()
        try:
            from teacher_management import TeacherManagement
            TeacherManagement(self.content_area, self.db, self.user_id)
        except Exception as e:
            self.show_error("Teachers module not available yet")
    
    def show_subjects(self):
        """Show subject management"""
        self.clear_content()
        try:
            from subject_management import SubjectManagement
            SubjectManagement(self.content_area, self.db, self.user_id)
        except Exception as e:
            self.show_error("Subjects module not available yet")
    
    def show_attendance(self):
        """Show attendance management"""
        self.clear_content()
        try:
            from attendance_management import AttendanceManagement
            AttendanceManagement(self.content_area, self.db, self.user_id)
        except Exception as e:
            self.show_error("Attendance module not available yet")
    
    def show_marks(self):
        """Show marks management"""
        self.clear_content()
        try:
            from marks_management import MarksManagement
            MarksManagement(self.content_area, self.db, self.user_id)
        except Exception as e:
            self.show_error("Marks module not available yet")
    
    def show_reports(self):
        """Show reports"""
        self.clear_content()
        self.show_message("Reports", "📈 Reports feature coming soon!")
    
    def show_settings(self):
        """Show settings"""
        self.clear_content()
        try:
            from settings_management import SettingsManagement
            SettingsManagement(self.content_area, self.db, self.user_id)
        except Exception as e:
            self.show_error("Settings module not available yet")
    
    def show_my_attendance(self):
        """Show student's own attendance"""
        self.clear_content()
        self.show_message("My Attendance", "📊 Your attendance records will be shown here")
    
    def show_my_marks(self):
        """Show student's own marks"""
        self.clear_content()
        self.show_message("My Marks", "📝 Your marks will be shown here")
    
    def show_my_subjects(self):
        """Show student's subjects"""
        self.clear_content()
        self.show_message("My Subjects", "📚 Your enrolled subjects will be shown here")
    
    def show_ai_assistant(self):
        """Show AI assistant"""
        self.clear_content()
        try:
            from ai_chatbot import ChatbotGUI
            ChatbotGUI(self.content_area, self.user_id, self.role, self.full_name)
        except Exception as e:
            self.show_error("AI Assistant not available yet")
    
    def show_message(self, title, message):
        """Show a simple message in content area"""
        tk.Label(
            self.content_area,
            text=title,
            font=("Arial", 18, "bold"),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=30)
        
        tk.Label(
            self.content_area,
            text=message,
            font=("Arial", 14),
            bg='white',
            fg='#7f8c8d'
        ).pack(pady=20)
    
    def show_error(self, message):
        """Show error message"""
        tk.Label(
            self.content_area,
            text="⚠️ Module Not Ready",
            font=("Arial", 18, "bold"),
            bg='white',
            fg='#e74c3c'
        ).pack(pady=30)
        
        tk.Label(
            self.content_area,
            text=message,
            font=("Arial", 14),
            bg='white',
            fg='#7f8c8d'
        ).pack(pady=20)
    
    def logout(self):
        """Logout and return to login screen"""
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.window.destroy()
            # Open login window again
            from login import LoginWindow
            login = LoginWindow()
            login.start()
    
    def run(self):
        """Start the dashboard"""
        self.window.mainloop()

# Test the dashboard
if __name__ == "__main__":
    # Test with different roles
    dashboard = Dashboard(1, "Test User", "admin")
    dashboard.run()
