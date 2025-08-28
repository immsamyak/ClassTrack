
import tkinter as tk
from tkinter import ttk, messagebox
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
        
        # Get student statistics from database
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Get student info using user_id
                cursor.execute("SELECT student_id, class_name FROM students WHERE user_id = %s", (self.user_id,))
                student_info = cursor.fetchone()
                
                if student_info:
                    student_id, class_name = student_info
                    
                    # Get attendance stats
                    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id = %s AND status = 'Present'", (student_id,))
                    present_count = cursor.fetchone()[0] or 0
                    
                    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id = %s", (student_id,))
                    total_attendance = cursor.fetchone()[0] or 0
                    
                    # Get marks stats
                    cursor.execute("SELECT COUNT(DISTINCT subject_id) FROM marks WHERE student_id = %s", (student_id,))
                    subjects_with_marks = cursor.fetchone()[0] or 0
                    
                    # Get subjects count for this class
                    cursor.execute("SELECT COUNT(*) FROM subjects WHERE class_name = %s", (class_name,))
                    total_subjects = cursor.fetchone()[0] or 0
                    
                    # Calculate attendance percentage
                    attendance_percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0
                    
                    # Create stat cards
                    stats_frame = tk.Frame(parent, bg='white')
                    stats_frame.pack(pady=20)
                    
                    self.create_stat_card(stats_frame, "Attendance", f"{attendance_percentage:.1f}%", "#3498db", 0, 0)
                    self.create_stat_card(stats_frame, "Total Classes", total_attendance, "#27ae60", 0, 1)
                    self.create_stat_card(stats_frame, "My Subjects", total_subjects, "#f39c12", 0, 2)
                    self.create_stat_card(stats_frame, "Subjects with Marks", subjects_with_marks, "#e74c3c", 0, 3)
                    
                else:
                    tk.Label(
                        parent,
                        text="Student information not found",
                        font=("Arial", 12),
                        bg='white',
                        fg='#e74c3c'
                    ).pack(pady=20)
                    
            except Exception as e:
                tk.Label(
                    parent,
                    text="• View your attendance\n• Check your marks\n• See your subjects",
                    font=("Arial", 12),
                    bg='white',
                    justify='left'
                ).pack()
            finally:
                cursor.close()
                conn.close()
        else:
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
        
        # Title
        tk.Label(
            self.content_area,
            text="Reports & Analytics",
            font=("Arial", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # Reports based on role
        if self.role == 'admin':
            self.show_admin_reports()
        elif self.role == 'teacher':
            self.show_teacher_reports()
        else:
            self.show_student_reports()
    
    def show_admin_reports(self):
        """Show admin reports"""
        reports_frame = tk.Frame(self.content_area, bg='white')
        reports_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Quick stats
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Get basic statistics
                stats = {}
                cursor.execute("SELECT COUNT(*) FROM students")
                stats['total_students'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM teachers")
                stats['total_teachers'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM subjects")
                stats['total_subjects'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM attendance WHERE attendance_date = CURDATE()")
                stats['today_attendance'] = cursor.fetchone()[0]
                
                # Display stats in cards
                stats_frame = tk.Frame(reports_frame, bg='white')
                stats_frame.pack(fill='x', pady=20)
                
                self.create_stat_card(stats_frame, "Total Students", stats['total_students'], "#3498db", 0, 0)
                self.create_stat_card(stats_frame, "Total Teachers", stats['total_teachers'], "#27ae60", 0, 1)
                self.create_stat_card(stats_frame, "Total Subjects", stats['total_subjects'], "#f39c12", 0, 2)
                self.create_stat_card(stats_frame, "Today's Attendance", stats['today_attendance'], "#e74c3c", 0, 3)
                
                # Recent activity
                tk.Label(
                    reports_frame,
                    text="Recent Activity",
                    font=("Arial", 14, "bold"),
                    bg='white'
                ).pack(pady=(20, 10))
                
                # Get recent enrollments
                cursor.execute("""
                    SELECT full_name, enrollment_date 
                    FROM students 
                    ORDER BY enrollment_date DESC 
                    LIMIT 5
                """)
                recent_students = cursor.fetchall()
                
                if recent_students:
                    for student, date in recent_students:
                        tk.Label(
                            reports_frame,
                            text=f"• {student} enrolled on {date}",
                            font=("Arial", 10),
                            bg='white',
                            anchor='w'
                        ).pack(fill='x', padx=20)
                
            except Exception as e:
                self.show_error(f"Failed to load reports: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def show_teacher_reports(self):
        """Show teacher reports"""
        tk.Label(
            self.content_area,
            text="Class Performance Reports",
            font=("Arial", 14, "bold"),
            bg='white'
        ).pack(pady=20)
        
        tk.Label(
            self.content_area,
            text="• View class attendance summary\n• Check student performance\n• Generate grade reports",
            font=("Arial", 12),
            bg='white',
            justify='left'
        ).pack()
    
    def show_student_reports(self):
        """Show student reports"""
        tk.Label(
            self.content_area,
            text="My Academic Report",
            font=("Arial", 14, "bold"),
            bg='white'
        ).pack(pady=20)
        
        tk.Label(
            self.content_area,
            text="• Your attendance summary\n• Your grade report\n• Your academic progress",
            font=("Arial", 12),
            bg='white',
            justify='left'
        ).pack()
    
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
        
        # Title
        tk.Label(
            self.content_area,
            text="My Attendance Records",
            font=("Arial", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # Create attendance display
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # First get student_id from students table using user_id
                cursor.execute("SELECT student_id FROM students WHERE user_id = %s", (self.user_id,))
                student_data = cursor.fetchone()
                
                if not student_data:
                    tk.Label(
                        self.content_area,
                        text="Student information not found",
                        font=("Arial", 14),
                        bg='white',
                        fg='#e74c3c'
                    ).pack(pady=50)
                    return
                
                student_id = student_data[0]
                
                # Get student's attendance with subject names
                cursor.execute("""
                    SELECT a.attendance_date, a.status, s.subject_name 
                    FROM attendance a 
                    LEFT JOIN subjects s ON a.subject_id = s.subject_id
                    WHERE a.student_id = %s 
                    ORDER BY a.attendance_date DESC LIMIT 50
                """, (student_id,))
                attendance_records = cursor.fetchall()
                
                if attendance_records:
                    # Create scrollable frame
                    canvas = tk.Canvas(self.content_area, bg='white')
                    scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
                    scrollable_frame = tk.Frame(canvas, bg='white')
                    
                    scrollable_frame.bind(
                        "<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                    )
                    
                    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                    canvas.configure(yscrollcommand=scrollbar.set)
                    
                    # Create table
                    columns = ("Date", "Status", "Subject")
                    tree = ttk.Treeview(scrollable_frame, columns=columns, show='headings', height=15)
                    
                    for col in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=150)
                    
                    for record in attendance_records:
                        date, status, subject = record
                        # Format the data
                        formatted_subject = subject if subject else "N/A"
                        tree.insert('', 'end', values=(date, status, formatted_subject))
                    
                    tree.pack(pady=10, padx=20, fill='both', expand=True)
                    
                    # Calculate attendance percentage
                    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id = %s AND status = 'present'", (student_id,))
                    present_count = cursor.fetchone()[0]
                    
                    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id = %s", (student_id,))
                    total_count = cursor.fetchone()[0]
                    
                    if total_count > 0:
                        percentage = (present_count / total_count) * 100
                        tk.Label(
                            scrollable_frame,
                            text=f"Attendance Percentage: {percentage:.1f}% ({present_count}/{total_count})",
                            font=("Arial", 14, "bold"),
                            bg='white',
                            fg='#27ae60' if percentage >= 75 else '#e74c3c'
                        ).pack(pady=20)
                    
                    canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
                    scrollbar.pack(side="right", fill="y", pady=10)
                    
                else:
                    tk.Label(
                        self.content_area,
                        text="No attendance records found",
                        font=("Arial", 14),
                        bg='white',
                        fg='#7f8c8d'
                    ).pack(pady=50)
                    
            except Exception as e:
                self.show_error(f"Failed to load attendance: {str(e)}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.show_error("Database connection failed")
    
    def show_my_marks(self):
        """Show student's own marks"""
        self.clear_content()
        
        # Title
        tk.Label(
            self.content_area,
            text="My Marks & Grades",
            font=("Arial", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # Create marks display
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # First get student_id from students table using user_id
                cursor.execute("SELECT student_id FROM students WHERE user_id = %s", (self.user_id,))
                student_data = cursor.fetchone()
                
                if not student_data:
                    tk.Label(
                        self.content_area,
                        text="Student information not found",
                        font=("Arial", 14),
                        bg='white',
                        fg='#e74c3c'
                    ).pack(pady=50)
                    return
                
                student_id = student_data[0]
                
                # Get student's marks with subject names
                cursor.execute("""
                    SELECT s.subject_name, m.exam_type, m.marks_obtained, m.total_marks, m.grade, m.exam_date
                    FROM marks m 
                    JOIN subjects s ON m.subject_id = s.subject_id
                    WHERE m.student_id = %s 
                    ORDER BY m.exam_date DESC
                """, (student_id,))
                marks_records = cursor.fetchall()
                
                if marks_records:
                    # Create scrollable frame
                    canvas = tk.Canvas(self.content_area, bg='white')
                    scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
                    scrollable_frame = tk.Frame(canvas, bg='white')
                    
                    scrollable_frame.bind(
                        "<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                    )
                    
                    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                    canvas.configure(yscrollcommand=scrollbar.set)
                    
                    # Create table
                    columns = ("Subject", "Exam Type", "Marks", "Total", "Grade", "Percentage", "Date")
                    tree = ttk.Treeview(scrollable_frame, columns=columns, show='headings', height=15)
                    
                    for col in columns:
                        tree.heading(col, text=col)
                        tree.column(col, width=110)
                    
                    total_marks_obtained = 0
                    total_marks_possible = 0
                    
                    for record in marks_records:
                        subject, exam_type, marks_obtained, total_marks, grade, exam_date = record
                        if total_marks and total_marks > 0:
                            percentage = (marks_obtained / total_marks) * 100
                            total_marks_obtained += marks_obtained or 0
                            total_marks_possible += total_marks or 0
                        else:
                            percentage = 0
                        
                        # Format the data
                        formatted_grade = grade if grade else "N/A"
                        formatted_date = exam_date if exam_date else "N/A"
                        
                        tree.insert('', 'end', values=(
                            subject or "N/A", 
                            exam_type or "N/A", 
                            marks_obtained or 0, 
                            total_marks or 0, 
                            formatted_grade,
                            f"{percentage:.1f}%", 
                            formatted_date
                        ))
                    
                    tree.pack(pady=10, padx=20, fill='both', expand=True)
                    
                    # Calculate overall percentage
                    if total_marks_possible > 0:
                        overall_percentage = (total_marks_obtained / total_marks_possible) * 100
                        
                        # Determine grade
                        if overall_percentage >= 90:
                            overall_grade = "A+"
                        elif overall_percentage >= 80:
                            overall_grade = "A"
                        elif overall_percentage >= 70:
                            overall_grade = "B+"
                        elif overall_percentage >= 60:
                            overall_grade = "B"
                        elif overall_percentage >= 50:
                            overall_grade = "C+"
                        elif overall_percentage >= 40:
                            overall_grade = "C"
                        elif overall_percentage >= 32:
                            overall_grade = "D"
                        else:
                            overall_grade = "F"
                        
                        tk.Label(
                            scrollable_frame,
                            text=f"Overall Performance: {overall_percentage:.1f}% | Grade: {overall_grade} | Total: ({total_marks_obtained}/{total_marks_possible})",
                            font=("Arial", 14, "bold"),
                            bg='white',
                            fg='#27ae60' if overall_percentage >= 60 else '#e74c3c'
                        ).pack(pady=20)
                    
                    canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
                    scrollbar.pack(side="right", fill="y", pady=10)
                    
                else:
                    tk.Label(
                        self.content_area,
                        text="No marks records found",
                        font=("Arial", 14),
                        bg='white',
                        fg='#7f8c8d'
                    ).pack(pady=50)
                    
            except Exception as e:
                self.show_error(f"Failed to load marks: {str(e)}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.show_error("Database connection failed")
    
    def show_my_subjects(self):
        """Show student's subjects"""
        self.clear_content()
        
        # Title
        tk.Label(
            self.content_area,
            text="My Enrolled Subjects",
            font=("Arial", 18, "bold"),
            bg='white'
        ).pack(pady=20)
        
        # Get student's class first
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Get student's class using user_id
                cursor.execute("SELECT student_id, class_name FROM students WHERE user_id = %s", (self.user_id,))
                student_data = cursor.fetchone()
                
                if student_data:
                    student_id, student_class = student_data
                    
                    # Show current class
                    tk.Label(
                        self.content_area,
                        text=f"Current Class: {student_class}",
                        font=("Arial", 14, "bold"),
                        bg='white',
                        fg='#3498db'
                    ).pack(pady=10)
                    
                    # Get subjects for this class using the standardized semester names
                    cursor.execute("""
                        SELECT s.subject_name, s.subject_code, s.credit_hours, 
                               COALESCE(t.full_name, 'Not Assigned') as teacher_name,
                               s.description
                        FROM subjects s 
                        LEFT JOIN teachers t ON s.teacher_id = t.teacher_id
                        WHERE s.class_name = %s
                        ORDER BY s.subject_name
                    """, (student_class,))
                    subjects = cursor.fetchall()
                    
                    if subjects:
                        # Create scrollable frame
                        canvas = tk.Canvas(self.content_area, bg='white')
                        scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
                        scrollable_frame = tk.Frame(canvas, bg='white')
                        
                        scrollable_frame.bind(
                            "<Configure>",
                            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                        )
                        
                        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                        canvas.configure(yscrollcommand=scrollbar.set)
                        
                        # Create table
                        columns = ("Subject Name", "Subject Code", "Credits", "Teacher", "Description")
                        tree = ttk.Treeview(scrollable_frame, columns=columns, show='headings', height=12)
                        
                        column_widths = {
                            "Subject Name": 200,
                            "Subject Code": 120,
                            "Credits": 80,
                            "Teacher": 150,
                            "Description": 250
                        }
                        
                        for col in columns:
                            tree.heading(col, text=col)
                            tree.column(col, width=column_widths.get(col, 150))
                        
                        total_credits = 0
                        for subject in subjects:
                            subject_name, subject_code, credits, teacher_name, description = subject
                            
                            # Format the data
                            formatted_credits = credits if credits else 0
                            formatted_description = description if description else "N/A"
                            
                            tree.insert('', 'end', values=(
                                subject_name,
                                subject_code,
                                formatted_credits,
                                teacher_name,
                                formatted_description
                            ))
                            
                            if credits:
                                total_credits += int(credits)
                        
                        tree.pack(pady=10, padx=20, fill='both', expand=True)
                        
                        # Show statistics
                        stats_frame = tk.Frame(scrollable_frame, bg='white')
                        stats_frame.pack(pady=20, fill='x')
                        
                        tk.Label(
                            stats_frame,
                            text=f"Total Subjects: {len(subjects)} | Total Credits: {total_credits}",
                            font=("Arial", 14, "bold"),
                            bg='white',
                            fg='#3498db'
                        ).pack()
                        
                        # Get attendance and marks statistics for subjects
                        subject_stats_frame = tk.Frame(scrollable_frame, bg='white')
                        subject_stats_frame.pack(pady=20, fill='x')
                        
                        tk.Label(
                            subject_stats_frame,
                            text="Subject Performance Overview:",
                            font=("Arial", 12, "bold"),
                            bg='white',
                            fg='#2c3e50'
                        ).pack(pady=(0, 10))
                        
                        # Get performance data for each subject
                        for subject_name, subject_code, _, _, _ in subjects:
                            # Get subject_id first
                            cursor.execute("SELECT subject_id FROM subjects WHERE subject_code = %s", (subject_code,))
                            subject_data = cursor.fetchone()
                            
                            if subject_data:
                                subject_id = subject_data[0]
                                
                                # Get attendance for this subject
                                cursor.execute("""
                                    SELECT COUNT(*) as total, 
                                           SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present
                                    FROM attendance 
                                    WHERE student_id = %s AND subject_id = %s
                                """, (student_id, subject_id))
                                attendance_data = cursor.fetchone()
                                
                                # Get marks for this subject
                                cursor.execute("""
                                    SELECT AVG(marks_obtained), AVG(total_marks), COUNT(*)
                                    FROM marks 
                                    WHERE student_id = %s AND subject_id = %s
                                """, (student_id, subject_id))
                                marks_data = cursor.fetchone()
                                
                                # Format the statistics
                                if attendance_data and attendance_data[0] > 0:
                                    attendance_percent = (attendance_data[1] / attendance_data[0]) * 100
                                    attendance_text = f"{attendance_percent:.1f}%"
                                else:
                                    attendance_text = "No data"
                                
                                if marks_data and marks_data[0] and marks_data[1]:
                                    marks_percent = (marks_data[0] / marks_data[1]) * 100
                                    marks_text = f"{marks_percent:.1f}%"
                                else:
                                    marks_text = "No marks"
                                
                                # Display subject stats
                                subject_stat_frame = tk.Frame(subject_stats_frame, bg='#f8f9fa', relief='raised', bd=1)
                                subject_stat_frame.pack(fill='x', pady=2, padx=20)
                                
                                tk.Label(
                                    subject_stat_frame,
                                    text=f"{subject_name} ({subject_code})",
                                    font=("Arial", 10, "bold"),
                                    bg='#f8f9fa',
                                    anchor='w'
                                ).pack(side='left', padx=10, pady=5)
                                
                                tk.Label(
                                    subject_stat_frame,
                                    text=f"Attendance: {attendance_text} | Performance: {marks_text}",
                                    font=("Arial", 9),
                                    bg='#f8f9fa',
                                    anchor='e'
                                ).pack(side='right', padx=10, pady=5)
                        
                        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
                        scrollbar.pack(side="right", fill="y", pady=10)
                        
                    else:
                        tk.Label(
                            self.content_area,
                            text=f"No subjects found for {student_class}",
                            font=("Arial", 14),
                            bg='white',
                            fg='#7f8c8d'
                        ).pack(pady=50)
                else:
                    tk.Label(
                        self.content_area,
                        text="Student information not found",
                        font=("Arial", 14),
                        bg='white',
                        fg='#e74c3c'
                    ).pack(pady=50)
                    
            except Exception as e:
                self.show_error(f"Failed to load subjects: {str(e)}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.show_error("Database connection failed")
    
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
