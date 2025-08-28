import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class AttendanceManagement:
    def __init__(self, parent_frame, db_config, user_id):
        self.parent = parent_frame
        self.db = db_config
        self.user_id = user_id
        
        # Title
        tk.Label(self.parent, text="Attendance Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Mark Attendance Tab
        self.mark_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.mark_frame, text="📝 Mark Attendance")
        self.create_mark_attendance_tab()
        
        # View Attendance Tab
        self.view_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_frame, text="👁️ View Attendance")
        self.create_view_attendance_tab()
    
    def create_mark_attendance_tab(self):
        # Selection frame
        selection_frame = tk.Frame(self.mark_frame)
        selection_frame.pack(pady=10)
        
        # Date input
        tk.Label(selection_frame, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(selection_frame, width=12)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, str(date.today()))
        
        # Semester selection
        tk.Label(selection_frame, text="Semester:").grid(row=0, column=2, padx=10, pady=5)
        self.semester_combo = ttk.Combobox(selection_frame, values=[
            "BCSIT 1st Sem", "BCSIT 2nd Sem", "BCSIT 3rd Sem", "BCSIT 4th Sem"
        ], width=15, state="readonly")
        self.semester_combo.grid(row=0, column=3, padx=5, pady=5)
        self.semester_combo.bind('<<ComboboxSelected>>', self.load_subjects)
        
        # Subject selection
        tk.Label(selection_frame, text="Subject:").grid(row=1, column=0, padx=5, pady=5)
        self.subject_combo = ttk.Combobox(selection_frame, width=20, state="readonly")
        self.subject_combo.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        # Load Students button
        tk.Button(self.mark_frame, text="Load Students", command=self.load_students, bg='blue', fg='white').pack(pady=10)
        
        # Students list frame
        self.students_frame = tk.Frame(self.mark_frame)
        self.students_frame.pack(fill='both', expand=True, pady=10)
        
        # Save button
        tk.Button(self.mark_frame, text="Save Attendance", command=self.save_attendance, bg='green', fg='white').pack(pady=10)
    
    def create_view_attendance_tab(self):
        # Filter frame for viewing
        filter_frame = tk.Frame(self.view_frame)
        filter_frame.pack(pady=10)
        
        # View options
        tk.Label(filter_frame, text="View Semester:").grid(row=0, column=0, padx=5, pady=5)
        self.view_semester_combo = ttk.Combobox(filter_frame, values=[
            "BCSIT 1st Sem", "BCSIT 2nd Sem", "BCSIT 3rd Sem", "BCSIT 4th Sem"
        ], width=15, state="readonly")
        self.view_semester_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(filter_frame, text="From Date:").grid(row=0, column=2, padx=10, pady=5)
        self.from_date_entry = tk.Entry(filter_frame, width=12)
        self.from_date_entry.grid(row=0, column=3, padx=5, pady=5)
        self.from_date_entry.insert(0, str(date.today()))
        
        tk.Label(filter_frame, text="To Date:").grid(row=1, column=0, padx=5, pady=5)
        self.to_date_entry = tk.Entry(filter_frame, width=12)
        self.to_date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.to_date_entry.insert(0, str(date.today()))
        
        # View button
        tk.Button(filter_frame, text="View Attendance", command=self.view_attendance, 
                 bg='#3498db', fg='white').grid(row=1, column=2, columnspan=2, padx=10, pady=5)
        
        # Attendance display frame with scrollbar
        display_frame = tk.Frame(self.view_frame)
        display_frame.pack(fill='both', expand=True, pady=10, padx=20)
        
        # Create Treeview for attendance data
        columns = ("Date", "Student", "Roll", "Subject", "Status")
        self.attendance_tree = ttk.Treeview(display_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.attendance_tree.heading(col, text=col)
            self.attendance_tree.column(col, width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(display_frame, orient='vertical', command=self.attendance_tree.yview)
        h_scrollbar = ttk.Scrollbar(display_frame, orient='horizontal', command=self.attendance_tree.xview)
        self.attendance_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack everything
        self.attendance_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Summary frame
        summary_frame = tk.Frame(self.view_frame)
        summary_frame.pack(pady=10)
        self.summary_label = tk.Label(summary_frame, text="Select filters and click 'View Attendance' to see records", 
                                     font=("Arial", 10), fg='blue')
        self.summary_label.pack()
        
    def load_subjects(self, event=None):
        # Load subjects based on selected semester
        semester = self.semester_combo.get()
        if not semester:
            return
            
        conn = self.db.get_connection()
        if conn:
            cursor = conn.cursor()
            # Get subjects for the semester from database
            cursor.execute("SELECT subject_name FROM subjects WHERE class_name = %s", (semester,))
            subjects = [row[0] for row in cursor.fetchall()]
            self.subject_combo['values'] = subjects
            self.subject_combo.set("")
            cursor.close()
            conn.close()
    
    def load_students(self):
        semester = self.semester_combo.get()
        subject = self.subject_combo.get()
        
        if not semester or not subject:
            messagebox.showwarning("Warning", "Please select semester and subject first!")
            return
            
        # Clear existing widgets
        for widget in self.students_frame.winfo_children():
            widget.destroy()
            
        # Get students from database for selected semester
        conn = self.db.get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT student_id, full_name, roll_number FROM students WHERE class_name = %s ORDER BY roll_number", (semester,))
            students = cursor.fetchall()
            
            if not students:
                tk.Label(self.students_frame, text="No students found for this semester", 
                        font=("Arial", 12), fg='red').pack(pady=20)
                cursor.close()
                conn.close()
                return
                
            self.student_vars = {}
            
            # Header
            header = tk.Frame(self.students_frame)
            header.pack(fill='x', padx=20, pady=5)
            tk.Label(header, text="Roll - Student Name", font=("Arial", 11, "bold"), width=30, anchor='w').pack(side='left')
            tk.Label(header, text="Present", font=("Arial", 11, "bold"), width=8).pack(side='left')
            tk.Label(header, text="Absent", font=("Arial", 11, "bold"), width=8).pack(side='left')
            tk.Label(header, text="Late", font=("Arial", 11, "bold"), width=8).pack(side='left')
            
            # Create radio buttons for each student
            for student_id, name, roll in students:
                frame = tk.Frame(self.students_frame)
                frame.pack(fill='x', padx=20, pady=2)
                
                # Student info
                tk.Label(frame, text=f"{roll} - {name}", width=30, anchor='w').pack(side='left')
                
                # Attendance status variable
                var = tk.StringVar(value="Present")
                self.student_vars[student_id] = var
                
                # Radio buttons
                tk.Radiobutton(frame, text="", variable=var, value="Present").pack(side='left', padx=20)
                tk.Radiobutton(frame, text="", variable=var, value="Absent").pack(side='left', padx=20)
                tk.Radiobutton(frame, text="", variable=var, value="Late").pack(side='left', padx=20)
            
            cursor.close()
            conn.close()
    
    def save_attendance(self):
        attendance_date = self.date_entry.get()
        semester = self.semester_combo.get()
        subject = self.subject_combo.get()
        
        if not attendance_date or not semester or not subject:
            messagebox.showerror("Error", "Please fill in date, semester and subject!")
            return
            
        if not hasattr(self, 'student_vars') or not self.student_vars:
            messagebox.showerror("Error", "Please load students first!")
            return
            
        conn = self.db.get_connection()
        if conn:
            cursor = conn.cursor()
            
            # First, get the subject_id from subject name
            cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = %s AND class_name = %s", 
                          (subject, semester))
            subject_result = cursor.fetchone()
            if not subject_result:
                messagebox.showerror("Error", f"Subject '{subject}' not found for {semester}!")
                cursor.close()
                conn.close()
                return
            
            subject_id = subject_result[0]
            saved_count = 0
            
            for student_id, status_var in self.student_vars.items():
                status = status_var.get()
                
                # Check if attendance already exists for this student, date, and subject
                cursor.execute("SELECT * FROM attendance WHERE student_id = %s AND attendance_date = %s AND subject_id = %s", 
                             (student_id, attendance_date, subject_id))
                if cursor.fetchone():
                    # Update existing
                    cursor.execute("UPDATE attendance SET status = %s WHERE student_id = %s AND attendance_date = %s AND subject_id = %s",
                                 (status, student_id, attendance_date, subject_id))
                else:
                    # Insert new with subject_id
                    cursor.execute("INSERT INTO attendance (student_id, subject_id, attendance_date, status, marked_by) VALUES (%s, %s, %s, %s, %s)",
                                 (student_id, subject_id, attendance_date, status, self.user_id))
                saved_count += 1
            
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", f"Attendance saved for {saved_count} students!\nSemester: {semester}\nSubject: {subject}")
    
    def view_attendance(self):
        # Clear existing data
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)
        
        semester = self.view_semester_combo.get()
        from_date = self.from_date_entry.get()
        to_date = self.to_date_entry.get()
        
        if not semester:
            messagebox.showwarning("Warning", "Please select a semester!")
            return
        
        conn = self.db.get_connection()
        if conn:
            cursor = conn.cursor()
            
            # Query to get attendance data with student and subject info
            query = """
            SELECT a.attendance_date, s.full_name, s.roll_number, 
                   subj.subject_name, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            LEFT JOIN subjects subj ON a.subject_id = subj.subject_id
            WHERE s.class_name = %s
            AND a.attendance_date BETWEEN %s AND %s
            ORDER BY a.attendance_date DESC, s.roll_number
            """
            
            cursor.execute(query, (semester, from_date, to_date))
            records = cursor.fetchall()
            
            # Insert data into tree
            present_count = 0
            absent_count = 0
            late_count = 0
            
            for record in records:
                attendance_date, student_name, roll_number, subject_name, status = record
                subject_name = subject_name or "N/A"
                
                # Color coding based on status
                if status == "Present":
                    present_count += 1
                    tags = ("present",)
                elif status == "Absent":
                    absent_count += 1
                    tags = ("absent",)
                else:  # Late
                    late_count += 1
                    tags = ("late",)
                
                self.attendance_tree.insert('', 'end', 
                    values=(attendance_date, student_name, roll_number, subject_name, status),
                    tags=tags)
            
            # Configure row colors
            self.attendance_tree.tag_configure("present", background="#d4edda")
            self.attendance_tree.tag_configure("absent", background="#f8d7da")
            self.attendance_tree.tag_configure("late", background="#fff3cd")
            
            # Update summary
            total_records = len(records)
            if total_records > 0:
                self.summary_label.config(
                    text=f"Total Records: {total_records} | Present: {present_count} | Absent: {absent_count} | Late: {late_count}",
                    fg='green'
                )
            else:
                self.summary_label.config(text="No attendance records found for the selected criteria", fg='red')
            
            cursor.close()
            conn.close()

# Test the module
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simple Attendance")
    root.geometry("600x500")
    from database_config import DatabaseConfig
    db = DatabaseConfig()
    AttendanceManagement(root, db, 1)
    root.mainloop()
