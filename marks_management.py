# Marks Management - Simple and Working
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class MarksManagement:
    def __init__(self, parent_frame, db_config, user_id):
        self.parent = parent_frame
        self.db = db_config
        
        # Title
        tk.Label(self.parent, text="Marks Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Selection Frame
        selection_frame = tk.LabelFrame(self.parent, text="Select Class Details", font=("Arial", 12, "bold"))
        selection_frame.pack(fill='x', padx=20, pady=10)
        
        # Row 1: Semester and Subject
        row1 = tk.Frame(selection_frame)
        row1.pack(pady=10)
        
        tk.Label(row1, text="Semester:").grid(row=0, column=0, padx=5, pady=5)
        self.semester_combo = ttk.Combobox(row1, values=[
            "BCSIT 1st Sem", "BCSIT 2nd Sem", "BCSIT 3rd Sem", "BCSIT 4th Sem"
        ], width=18, state="readonly")
        self.semester_combo.grid(row=0, column=1, padx=5, pady=5)
        self.semester_combo.bind('<<ComboboxSelected>>', self.load_subjects)
        
        tk.Label(row1, text="Subject:").grid(row=0, column=2, padx=15, pady=5)
        self.subject_combo = ttk.Combobox(row1, width=20, state="readonly")
        self.subject_combo.grid(row=0, column=3, padx=5, pady=5)
        self.subject_combo.bind('<<ComboboxSelected>>', self.load_students)
        
        # Row 2: Exam Type and Load button
        row2 = tk.Frame(selection_frame)
        row2.pack(pady=5)
        
        tk.Label(row2, text="Exam Type:").grid(row=0, column=0, padx=5, pady=5)
        self.exam_type_combo = ttk.Combobox(row2, values=["Assignment", "Quiz", "Mid Term", "Final"], width=15, state="readonly")
        self.exam_type_combo.grid(row=0, column=1, padx=5, pady=5)
        self.exam_type_combo.set("Assignment")
        
        tk.Button(row2, text="Load Students", command=self.load_students, bg='#3498db', fg='white').grid(row=0, column=2, padx=20, pady=5)
        
        # Form Frame for marks entry
        form_frame = tk.LabelFrame(self.parent, text="Enter Marks", font=("Arial", 12, "bold"))
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Form controls
        form_controls = tk.Frame(form_frame)
        form_controls.pack(pady=10)
        
        tk.Label(form_controls, text="Student:").grid(row=0, column=0, padx=5, pady=5)
        self.student_combo = ttk.Combobox(form_controls, width=25, state="readonly")
        self.student_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_controls, text="Marks Obtained:").grid(row=0, column=2, padx=15, pady=5)
        self.marks_entry = tk.Entry(form_controls, width=10)
        self.marks_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(form_controls, text="Total Marks:").grid(row=1, column=0, padx=5, pady=5)
        self.total_marks_entry = tk.Entry(form_controls, width=10)
        self.total_marks_entry.grid(row=1, column=1, padx=5, pady=5)
        self.total_marks_entry.insert(0, "100")
        
        tk.Label(form_controls, text="Exam Date:").grid(row=1, column=2, padx=15, pady=5)
        self.date_entry = tk.Entry(form_controls, width=12)
        self.date_entry.grid(row=1, column=3, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Buttons
        btn_frame = tk.Frame(self.parent)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Marks", command=self.add_marks, bg='#27ae60', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Clear Form", command=self.clear_form, bg='#95a5a6', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_marks, bg='#e74c3c', fg='white', width=12).pack(side='left', padx=5)
        
        # Initialize data
        self.current_subject_id = None
        
    def load_subjects(self, event=None):
        """Load subjects for selected semester"""
        semester = self.semester_combo.get()
        if not semester:
            return
            
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Get subjects for the semester from database
                cursor.execute("SELECT subject_id, subject_name FROM subjects WHERE class_name = %s", (semester,))
                subjects = cursor.fetchall()
                
                # Update subject dropdown
                subject_names = [f"{row[1]}" for row in subjects]
                self.subject_combo['values'] = subject_names
                self.subject_combo.set("")
                
                # Store subject mapping for later use
                self.subject_mapping = {row[1]: row[0] for row in subjects}
                
                # Store subject mapping for later use
                self.subject_mapping = {row[1]: row[0] for row in subjects}
                
            except Exception as e:
                # If subjects table doesn't exist or has different structure, use default
                default_subjects = ["Mathematics", "English", "Science", "Computer", "Physics"]
                self.subject_combo['values'] = default_subjects
                self.subject_mapping = {subj: i+1 for i, subj in enumerate(default_subjects)}
            finally:
                cursor.close()
                conn.close()
    
    def load_students(self, event=None):
        """Load students for selected semester"""
        semester = self.semester_combo.get()
        subject = self.subject_combo.get()
        
        if not semester:
            messagebox.showwarning("Warning", "Please select semester first!")
            return
            
        # Store current subject ID
        if hasattr(self, 'subject_mapping') and subject:
            self.current_subject_id = self.subject_mapping.get(subject, 1)
        
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT full_name FROM students WHERE class_name = %s ORDER BY full_name", (semester,))
                students = [row[0] for row in cursor.fetchall()]
                self.student_combo['values'] = students
                self.student_combo.set("")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load students: {str(e)}")
            finally:
                cursor.close()
                conn.close()
        
        # Marks List
        tk.Label(self.parent, text="Marks Records", font=("Arial", 14, "bold")).pack(pady=(20, 5))
        
        # Search
        search_frame = tk.Frame(self.parent)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_marks)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        # Table
        columns = ("ID", "Student", "Subject", "Exam Type", "Marks", "Total", "Percentage", "Date")
        self.tree = ttk.Treeview(self.parent, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        self.load_marks()
        
    def add_marks(self):
        student = self.student_combo.get()
        subject = self.subject_combo.get()
        exam_type = self.exam_type_combo.get()
        marks = self.marks_entry.get().strip()
        total_marks = self.total_marks_entry.get().strip()
        date = self.date_entry.get()
        
        if not student or not marks or not subject or not exam_type:
            messagebox.showerror("Error", "Please fill all fields!")
            return
            
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Get student ID
                cursor.execute("SELECT student_id FROM students WHERE full_name = %s", (student,))
                student_data = cursor.fetchone()
                if not student_data:
                    messagebox.showerror("Error", "Student not found!")
                    return
                    
                student_id = student_data[0]
                
                # Get subject ID
                subject_id = getattr(self, 'current_subject_id', 1)
                
                # Insert marks
                cursor.execute(
                    "INSERT INTO marks (student_id, subject_id, exam_type, marks_obtained, total_marks, exam_date) VALUES (%s, %s, %s, %s, %s, %s)",
                    (student_id, subject_id, exam_type, marks, total_marks, date)
                )
                conn.commit()
                messagebox.showinfo("Success", f"Marks added for {student} in {subject}!")
                self.clear_form()
                self.load_marks()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add marks: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def load_marks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT m.mark_id, s.full_name, subj.subject_name, m.exam_type, m.marks_obtained, m.total_marks, m.exam_date 
                    FROM marks m 
                    JOIN students s ON m.student_id = s.student_id 
                    LEFT JOIN subjects subj ON m.subject_id = subj.subject_id
                    ORDER BY m.exam_date DESC LIMIT 100
                """)
                for row in cursor.fetchall():
                    mark_id, student, subject, exam_type, marks_obtained, total_marks, exam_date = row
                    if total_marks and total_marks > 0:
                        percentage = f"{(marks_obtained / total_marks) * 100:.1f}%"
                    else:
                        percentage = "N/A"
                    
                    # Handle None subject from LEFT JOIN
                    if subject is None:
                        subject = "Unknown"
                    
                    self.tree.insert('', 'end', values=(
                        mark_id, student, subject, exam_type, marks_obtained, total_marks, percentage, exam_date
                    ))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load marks: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def search_marks(self, *args):
        search_text = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    SELECT m.mark_id, s.full_name, subj.subject_name, m.exam_type, m.marks_obtained, m.total_marks, m.exam_date 
                    FROM marks m 
                    JOIN students s ON m.student_id = s.student_id 
                    LEFT JOIN subjects subj ON m.subject_id = subj.subject_id
                    WHERE LOWER(s.full_name) LIKE %s OR LOWER(subj.subject_name) LIKE %s
                    ORDER BY m.exam_date DESC
                """
                pattern = f"%{search_text}%"
                cursor.execute(query, (pattern, pattern))
                for row in cursor.fetchall():
                    mark_id, student, subject, exam_type, marks_obtained, total_marks, exam_date = row
                    if total_marks and total_marks > 0:
                        percentage = f"{(marks_obtained / total_marks) * 100:.1f}%"
                    else:
                        percentage = "N/A"
                    
                    self.tree.insert('', 'end', values=(
                        mark_id, student, subject, exam_type, marks_obtained, total_marks, percentage, exam_date
                    ))
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def delete_marks(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a mark record to delete!")
            return
            
        item = selected[0]
        values = self.tree.item(item, 'values')
        mark_id = values[0]
        student_name = values[1]
        subject = values[2]
        
        result = messagebox.askyesno("Confirm Delete", f"Delete marks for {student_name} in {subject}?")
        if result:
            conn = self.db.get_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM marks WHERE mark_id = %s", (mark_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Marks deleted successfully!")
                    self.load_marks()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete marks: {str(e)}")
                finally:
                    cursor.close()
                    conn.close()
    
    def clear_form(self):
        self.student_combo.set("")
        self.marks_entry.delete(0, tk.END)
        self.total_marks_entry.delete(0, tk.END)
        self.total_marks_entry.insert(0, "100")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

# Test
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    root.title("Marks Management")
    from database_config import DatabaseConfig
    db = DatabaseConfig()
    MarksManagement(root, db, 1)
    root.mainloop()
