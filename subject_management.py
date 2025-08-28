# Subject Management - Simple and Working
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class SubjectManagement:
    def __init__(self, parent_frame, db_config, user_id):
        self.parent = parent_frame
        self.db = db_config
        
        # Title
        tk.Label(self.parent, text="Subject Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Form
        form = tk.Frame(self.parent)
        form.pack(pady=10)
        
        # Subject Name and Code
        tk.Label(form, text="Subject Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name = tk.Entry(form, width=25)
        self.name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Subject Code:").grid(row=0, column=2, padx=5, pady=5)
        self.code = tk.Entry(form, width=15)
        self.code.grid(row=0, column=3, padx=5, pady=5)
        
        # Credits and Semester
        tk.Label(form, text="Credits:").grid(row=1, column=0, padx=5, pady=5)
        self.credits = ttk.Combobox(form, values=["1", "2", "3", "4", "5"], width=22)
        self.credits.grid(row=1, column=1, padx=5, pady=5)
        self.credits.set("3")
        
        tk.Label(form, text="Semester:").grid(row=1, column=2, padx=5, pady=5)
        self.semester = ttk.Combobox(form, values=["BCSIT 1st Sem", "BCSIT 2nd Sem", "BCSIT 3rd Sem", "BCSIT 4th Sem"], width=12)
        self.semester.grid(row=1, column=3, padx=5, pady=5)
        self.semester.set("BCSIT 1st Sem")
        
        # Teacher and Department
        tk.Label(form, text="Teacher:").grid(row=2, column=0, padx=5, pady=5)
        self.teacher_combo = ttk.Combobox(form, width=22, state="readonly")
        self.teacher_combo.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Department:").grid(row=2, column=2, padx=5, pady=5)
        self.dept = ttk.Combobox(form, values=["IT", "Science", "Commerce", "Arts"], width=12)
        self.dept.grid(row=2, column=3, padx=5, pady=5)
        self.dept.set("IT")
        
        # Buttons
        btn_frame = tk.Frame(self.parent)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Subject", command=self.add_subject, bg='#27ae60', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Clear Form", command=self.clear_form, bg='#95a5a6', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_subject, bg='#e74c3c', fg='white', width=12).pack(side='left', padx=5)
        
        # Subject List
        tk.Label(self.parent, text="Subjects List", font=("Arial", 14, "bold")).pack(pady=(20, 5))
        
        # Table
        columns = ("ID", "Name", "Code", "Credits", "Semester", "Teacher")
        self.tree = ttk.Treeview(self.parent, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        self.load_teachers()
        self.load_subjects()
        
    def add_subject(self):
        name = self.name.get().strip()
        code = self.code.get().strip()
        credits = self.credits.get()
        semester = self.semester.get()
        teacher = self.teacher_combo.get()
        dept = self.dept.get()
        
        if not name or not code:
            messagebox.showerror("Error", "Subject name and code are required!")
            return
            
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Get teacher_id (user_id) if teacher is selected
                teacher_id = None
                if teacher:
                    cursor.execute("SELECT user_id FROM teachers WHERE full_name = %s", (teacher,))
                    result = cursor.fetchone()
                    if result:
                        teacher_id = result[0]
                
                # Insert subject with teacher assignment
                cursor.execute(
                    "INSERT INTO subjects (subject_name, subject_code, credit_hours, class_name, teacher_id) VALUES (%s, %s, %s, %s, %s)",
                    (name, code, int(credits), semester, teacher_id)
                )
                
                conn.commit()
                
                if teacher and teacher_id:
                    messagebox.showinfo("Success", f"Subject {name} added successfully and assigned to {teacher}!")
                else:
                    messagebox.showinfo("Success", f"Subject {name} added successfully!")
                    
                self.clear_form()
                self.load_subjects()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add subject: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def load_teachers(self):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT full_name FROM teachers ORDER BY full_name")
                teachers = [row[0] for row in cursor.fetchall()]
                self.teacher_combo['values'] = teachers
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load teachers: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def load_subjects(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Join with teachers table to get teacher name
                query = """
                SELECT s.subject_id, s.subject_name, s.subject_code, s.credit_hours, s.class_name,
                       COALESCE(t.full_name, 'Not Assigned') as teacher_name
                FROM subjects s
                LEFT JOIN teachers t ON s.teacher_id = t.user_id
                ORDER BY s.subject_name
                """
                cursor.execute(query)
                for row in cursor.fetchall():
                    self.tree.insert('', 'end', values=row)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load subjects: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def delete_subject(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a subject to delete!")
            return
            
        item = selected[0]
        values = self.tree.item(item, 'values')
        subject_id = values[0]
        subject_name = values[1]
        
        # Check if subject has attendance or marks records
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM attendance WHERE subject_id = %s", (subject_id,))
                attendance_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM marks WHERE subject_id = %s", (subject_id,))
                marks_count = cursor.fetchone()[0]
                
                if attendance_count > 0 or marks_count > 0:
                    # Show detailed warning
                    warning_msg = f"Cannot delete {subject_name} because:\n"
                    if attendance_count > 0:
                        warning_msg += f"• Subject has {attendance_count} attendance record(s)\n"
                    if marks_count > 0:
                        warning_msg += f"• Subject has {marks_count} mark(s) record(s)\n"
                    warning_msg += "\nDelete attendance and marks records first, or contact administrator."
                    
                    messagebox.showwarning("Cannot Delete", warning_msg)
                    return
                
                # If no dependencies, confirm deletion
                result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {subject_name}?")
                if result:
                    cursor.execute("DELETE FROM subjects WHERE subject_id = %s", (subject_id,))
                    conn.commit()
                    messagebox.showinfo("Success", f"Subject {subject_name} deleted successfully!")
                    self.load_subjects()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete subject: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def clear_form(self):
        self.name.delete(0, tk.END)
        self.code.delete(0, tk.END)
        self.credits.set("3")
        self.semester.set("BCSIT 1st Sem")
        self.teacher_combo.set("")
        self.dept.set("IT")

# Test
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    root.title("Subject Management")
    from database_config import DatabaseConfig
    db = DatabaseConfig()
    SubjectManagement(root, db, 1)
    root.mainloop()
