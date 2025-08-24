# dashboard.py - Main dashboard for Class Track system
import tkinter as tk
from tkinter import ttk, messagebox
from database_config import DatabaseConfig

class Dashboard:
    def __init__(self, user_id, full_name, role):
        self.user_id = user_id
        self.full_name = full_name
        self.role = role
        self.db_config = DatabaseConfig()
        
        self.window = tk.Tk()
        self.window.title(f"Class Track - Dashboard ({role.title()})")
        self.window.geometry("1000x700")
        self.window.configure(bg='#ecf0f1')
        
        # Center window
        self.center_window()
        
        self.create_dashboard()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"1000x700+{x}+{y}")
    
    def create_dashboard(self):
        """Create the main dashboard interface"""
        # Header frame
        header_frame = tk.Frame(self.window, bg='#2c3e50', height=60)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)
        
        # Header content
        tk.Label(
            header_frame,
            text=f"Class Track System - Welcome, {self.full_name}",
            font=("Arial", 16, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(side='left', padx=20, pady=15)
        
        tk.Button(
            header_frame,
            text="Logout",
            font=("Arial", 10),
            bg='#e74c3c',
            fg='white',
            command=self.logout
        ).pack(side='right', padx=20, pady=15)
        
        # Main content frame
        main_frame = tk.Frame(self.window, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sidebar frame
        sidebar_frame = tk.Frame(main_frame, bg='#34495e', width=200)
        sidebar_frame.pack(side='left', fill='y', padx=(0, 10))
        sidebar_frame.pack_propagate(False)
        
        # Content frame
        self.content_frame = tk.Frame(main_frame, bg='white')
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        self.create_sidebar(sidebar_frame)
        self.show_dashboard_home()
    
    def create_sidebar(self, parent):
        """Create sidebar navigation"""
        # Sidebar title
        tk.Label(
            parent,
            text="Navigation",
            font=("Arial", 14, "bold"),
            bg='#34495e',
            fg='white'
        ).pack(pady=20)
        
        # Navigation buttons based on role
        if self.role in ['admin', 'teacher']:
            self.create_nav_button(parent, "Dashboard", self.show_dashboard_home)
            self.create_nav_button(parent, "Students", self.show_students)
            if self.role == 'admin':
                self.create_nav_button(parent, "Teachers", self.show_teachers)
            self.create_nav_button(parent, "Attendance", self.show_attendance)
            self.create_nav_button(parent, "Marks", self.show_marks)
            self.create_nav_button(parent, "Reports", self.show_reports)
            if self.role == 'admin':
                self.create_nav_button(parent, "Subjects", self.show_subjects)
                self.create_nav_button(parent, "Settings", self.show_settings)
            # AI Assistant for all roles
            self.create_nav_button(parent, "🤖 AI Assistant", self.show_ai_assistant)
        else:  # student
            self.create_nav_button(parent, "Dashboard", self.show_dashboard_home)
            self.create_nav_button(parent, "My Attendance", self.show_my_attendance)
            self.create_nav_button(parent, "My Marks", self.show_my_marks)
            # AI Assistant for students
            self.create_nav_button(parent, "🤖 AI Assistant", self.show_ai_assistant)
    
    def create_nav_button(self, parent, text, command):
        """Create a navigation button"""
        btn = tk.Button(
            parent,
            text=text,
            font=("Arial", 11),
            bg='#34495e',
            fg='white',
            bd=0,
            width=18,
            height=2,
            command=command
        )
        btn.pack(pady=5, padx=10, fill='x')
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg='#4a6741')
        
        def on_leave(e):
            btn.configure(bg='#34495e')
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard_home(self):
        """Show dashboard home page"""
        self.clear_content()
        
        # Title
        tk.Label(
            self.content_frame,
            text="Dashboard Overview",
            font=("Arial", 18, "bold"),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=20)
        
        # Stats frame
        stats_frame = tk.Frame(self.content_frame, bg='white')
        stats_frame.pack(pady=20)
        
        if self.role in ['admin', 'teacher']:
            # Get statistics from database
            connection = self.db_config.get_connection()
            if connection:
                cursor = connection.cursor()
                
                # Total students
                cursor.execute("SELECT COUNT(*) FROM students")
                total_students = cursor.fetchone()[0]
                
                # Total subjects
                cursor.execute("SELECT COUNT(*) FROM subjects")
                total_subjects = cursor.fetchone()[0]
                
                # Total teachers (if admin)
                if self.role == 'admin':
                    cursor.execute("SELECT COUNT(*) FROM teachers")
                    total_teachers = cursor.fetchone()[0]
                    
                    self.create_stat_card(stats_frame, "Total Students", total_students, "#3498db", 0, 0)
                    self.create_stat_card(stats_frame, "Total Subjects", total_subjects, "#2ecc71", 0, 1)
                    self.create_stat_card(stats_frame, "Total Teachers", total_teachers, "#e74c3c", 0, 2)
                else:
                    self.create_stat_card(stats_frame, "Total Students", total_students, "#3498db", 0, 0)
                    self.create_stat_card(stats_frame, "Total Subjects", total_subjects, "#2ecc71", 0, 1)
                
                cursor.close()
                connection.close()
        else:
            # Student dashboard
            tk.Label(
                self.content_frame,
                text="Welcome to your student dashboard!",
                font=("Arial", 14),
                bg='white'
            ).pack(pady=50)
    
    def create_stat_card(self, parent, title, value, color, row, col):
        """Create a statistics card"""
        card_frame = tk.Frame(parent, bg=color, width=200, height=100)
        card_frame.grid(row=row, column=col, padx=20, pady=10)
        card_frame.pack_propagate(False)
        
        tk.Label(
            card_frame,
            text=str(value),
            font=("Arial", 24, "bold"),
            bg=color,
            fg='white'
        ).pack(pady=(10, 0))
        
        tk.Label(
            card_frame,
            text=title,
            font=("Arial", 12),
            bg=color,
            fg='white'
        ).pack()
    
    def show_students(self):
        """Show students management page"""
        self.clear_content()
        
        from student_management import StudentManagement
        student_mgmt = StudentManagement(self.content_frame, self.db_config, self.user_id)
    
    def show_teachers(self):
        """Show teachers management page"""
        self.clear_content()
        
        from teacher_management import TeacherManagement
        teacher_mgmt = TeacherManagement(self.content_frame, self.db_config, self.user_id)
    
    def show_attendance(self):
        """Show attendance management page"""
        self.clear_content()
        
        from attendance_management import AttendanceManagement
        attendance_mgmt = AttendanceManagement(self.content_frame, self.db_config, self.user_id)
    
    def show_marks(self):
        """Show marks management page"""
        self.clear_content()
        
        from marks_management import MarksManagement
        marks_mgmt = MarksManagement(self.content_frame, self.db_config, self.user_id)
    
    def show_subjects(self):
        """Show subjects management page"""
        self.clear_content()
        
        from subject_management import SubjectManagement
        subject_mgmt = SubjectManagement(self.content_frame, self.db_config, self.user_id)
    
    def show_reports(self):
        """Show reports page"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="Reports Module",
            font=("Arial", 18, "bold"),
            bg='white'
        ).pack(pady=50)
        
        tk.Label(
            self.content_frame,
            text="Coming Soon...",
            font=("Arial", 14),
            bg='white'
        ).pack()
    
    def show_settings(self):
        """Show settings page"""
        self.clear_content()
        
        try:
            from settings_management import SettingsManagement
            settings_mgmt = SettingsManagement(self.content_frame, self.db_config, self.user_id)
        except ImportError as e:
            tk.Label(
                self.content_frame,
                text="Settings module not available.\nPlease ensure settings_management.py is in the project directory.",
                font=("Arial", 12),
                bg='white',
                fg='red'
            ).pack(pady=50)
        except Exception as e:
            tk.Label(
                self.content_frame,
                text=f"Error loading Settings: {str(e)}",
                font=("Arial", 12),
                bg='white',
                fg='red'
            ).pack(pady=50)
    
    def show_my_attendance(self):
        """Show student's own attendance"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="My Attendance",
            font=("Arial", 18, "bold"),
            bg='white'
        ).pack(pady=50)
        
        tk.Label(
            self.content_frame,
            text="Coming Soon...",
            font=("Arial", 14),
            bg='white'
        ).pack()
    
    def show_my_marks(self):
        """Show student's own marks"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="My Marks",
            font=("Arial", 18, "bold"),
            bg='white'
        ).pack(pady=50)
        
        tk.Label(
            self.content_frame,
            text="Coming Soon...",
            font=("Arial", 14),
            bg='white'
        ).pack()
    
    def show_ai_assistant(self):
        """Show AI Assistant chatbot"""
        self.clear_content()
        
        try:
            from ai_chatbot import ChatbotGUI
            chatbot_gui = ChatbotGUI(self.content_frame, self.user_id, self.role, self.full_name)
        except ImportError as e:
            tk.Label(
                self.content_frame,
                text="AI Chatbot module not available.\nPlease ensure ai_chatbot.py is in the project directory.",
                font=("Arial", 12),
                bg='white',
                fg='red'
            ).pack(pady=50)
        except Exception as e:
            tk.Label(
                self.content_frame,
                text=f"Error loading AI Assistant: {str(e)}",
                font=("Arial", 12),
                bg='white',
                fg='red'
            ).pack(pady=50)
    
    def logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.window.destroy()
            from login import LoginWindow
            login = LoginWindow()
            login.run()
    
    def run(self):
        """Start the dashboard"""
        self.window.mainloop()
