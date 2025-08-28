# Student Management - Simple and Working
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class StudentManagement:
    def __init__(self, parent_frame, db_config, user_id):
        self.parent = parent_frame
        self.db = db_config
        
        # Title
        tk.Label(self.parent, text="Student Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Form
        form = tk.Frame(self.parent)
        form.pack(pady=10)
        
        # Name and Roll
        tk.Label(form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name = tk.Entry(form, width=25)
        self.name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Roll Number:").grid(row=0, column=2, padx=5, pady=5)
        self.roll = tk.Entry(form, width=20)
        self.roll.grid(row=0, column=3, padx=5, pady=5)
        
        # Email and Phone
        tk.Label(form, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email = tk.Entry(form, width=25)
        self.email.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Phone:").grid(row=1, column=2, padx=5, pady=5)
        self.phone = tk.Entry(form, width=20)
        self.phone.grid(row=1, column=3, padx=5, pady=5)
        
        # Class and Gender
        tk.Label(form, text="Class:").grid(row=2, column=0, padx=5, pady=5)
        self.class_name = ttk.Combobox(form, values=["BCSIT 1st Sem", "BCSIT 2nd Sem", "BCSIT 3rd Sem", "BCSIT 4th Sem"], width=22)
        self.class_name.grid(row=2, column=1, padx=5, pady=5)
        self.class_name.set("BCSIT 1st Sem")
        
        tk.Label(form, text="Gender:").grid(row=2, column=2, padx=5, pady=5)
        self.gender = ttk.Combobox(form, values=["Male", "Female"], width=17)
        self.gender.grid(row=2, column=3, padx=5, pady=5)
        self.gender.set("Male")
        
        # Buttons
        btn_frame = tk.Frame(self.parent)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Student", command=self.add_student, bg='#27ae60', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Clear Form", command=self.clear_form, bg='#95a5a6', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_student, bg='#e74c3c', fg='white', width=12).pack(side='left', padx=5)
        
        # Student List
        tk.Label(self.parent, text="Students List", font=("Arial", 14, "bold")).pack(pady=(20, 5))
        
        # Search
        search_frame = tk.Frame(self.parent)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_students)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        # Table
        columns = ("ID", "Name", "Roll", "Email", "Phone", "Class", "Gender")
        self.tree = ttk.Treeview(self.parent, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        self.load_students()
        
    def add_student(self):
        name = self.name.get().strip()
        roll = self.roll.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        class_name = self.class_name.get()
        gender = self.gender.get()
        
        if not name or not roll:
            messagebox.showerror("Error", "Name and Roll Number are required!")
            return
            
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # First, create user account
                username = roll.lower()  # Use roll number as username
                password = "student123"  # Default password
                
                cursor.execute("""
                    INSERT INTO users (username, password, role, full_name, email) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (username, password, 'student', name, email))
                
                user_id = cursor.lastrowid
                
                # Then, create student record with user_id
                cursor.execute("""
                    INSERT INTO students (user_id, roll_number, full_name, gender, email, phone, class_name, enrollment_date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, roll, name, gender, email, phone, class_name, datetime.now().date()))
                
                conn.commit()
                messagebox.showinfo("Success", f"Student {name} added successfully!\nLogin: {username} | Password: {password}")
                self.clear_form()
                self.load_students()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add student: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def load_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT student_id, full_name, roll_number, email, phone, class_name, gender FROM students ORDER BY full_name")
                for row in cursor.fetchall():
                    self.tree.insert('', 'end', values=row)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load students: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def search_students(self, *args):
        search_text = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """SELECT student_id, full_name, roll_number, email, phone, class_name, gender 
                          FROM students 
                          WHERE LOWER(full_name) LIKE %s OR LOWER(roll_number) LIKE %s 
                          ORDER BY full_name"""
                pattern = f"%{search_text}%"
                cursor.execute(query, (pattern, pattern))
                for row in cursor.fetchall():
                    self.tree.insert('', 'end', values=row)
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student to delete!")
            return
            
        item = selected[0]
        values = self.tree.item(item, 'values')
        student_id = values[0]
        student_name = values[1]
        
        # Check if student has attendance records
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id = %s", (student_id,))
                attendance_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM marks WHERE student_id = %s", (student_id,))
                marks_count = cursor.fetchone()[0]
                
                if attendance_count > 0 or marks_count > 0:
                    # Show detailed warning
                    warning_msg = f"Cannot delete {student_name} because:\n"
                    if attendance_count > 0:
                        warning_msg += f"• Student has {attendance_count} attendance record(s)\n"
                    if marks_count > 0:
                        warning_msg += f"• Student has {marks_count} mark(s) record(s)\n"
                    warning_msg += "\nDelete attendance and marks records first, or contact administrator."
                    
                    messagebox.showwarning("Cannot Delete", warning_msg)
                    return
                
                # If no dependencies, confirm deletion
                result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student_name}?")
                if result:
                    cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
                    conn.commit()
                    messagebox.showinfo("Success", f"Student {student_name} deleted successfully!")
                    self.load_students()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def clear_form(self):
        self.name.delete(0, tk.END)
        self.roll.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.class_name.set("BCSIT 1st Sem")
        self.gender.set("Male")

# Test
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    root.title("Student Management")
    from database_config import DatabaseConfig
    db = DatabaseConfig()
    StudentManagement(root, db, 1)
    root.mainloop()
