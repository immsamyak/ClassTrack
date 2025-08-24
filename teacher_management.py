# Teacher Management - Simple and Working
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TeacherManagement:
    def __init__(self, parent_frame, db_config, user_id):
        self.parent = parent_frame
        self.db = db_config
        
        # Title
        tk.Label(self.parent, text="Teacher Management", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Form
        form = tk.Frame(self.parent)
        form.pack(pady=10)
        
        # Name and Employee ID
        tk.Label(form, text="Full Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name = tk.Entry(form, width=25)
        self.name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Employee ID:").grid(row=0, column=2, padx=5, pady=5)
        self.emp_id = tk.Entry(form, width=20)
        self.emp_id.grid(row=0, column=3, padx=5, pady=5)
        
        # Email and Phone
        tk.Label(form, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email = tk.Entry(form, width=25)
        self.email.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Phone:").grid(row=1, column=2, padx=5, pady=5)
        self.phone = tk.Entry(form, width=20)
        self.phone.grid(row=1, column=3, padx=5, pady=5)
        
        # Subject and Department
        tk.Label(form, text="Subject:").grid(row=2, column=0, padx=5, pady=5)
        self.subject = ttk.Combobox(form, values=["Mathematics", "English", "Science", "Computer Science", "Physics", "Chemistry"], width=22)
        self.subject.grid(row=2, column=1, padx=5, pady=5)
        self.subject.set("Mathematics")
        
        tk.Label(form, text="Department:").grid(row=2, column=2, padx=5, pady=5)
        self.department = ttk.Combobox(form, values=["IT", "Science", "Commerce", "Arts"], width=17)
        self.department.grid(row=2, column=3, padx=5, pady=5)
        self.department.set("IT")
        
        # Salary and Gender
        tk.Label(form, text="Salary:").grid(row=3, column=0, padx=5, pady=5)
        self.salary = tk.Entry(form, width=25)
        self.salary.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Gender:").grid(row=3, column=2, padx=5, pady=5)
        self.gender = ttk.Combobox(form, values=["Male", "Female"], width=17)
        self.gender.grid(row=3, column=3, padx=5, pady=5)
        self.gender.set("Male")
        
        # Buttons
        btn_frame = tk.Frame(self.parent)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Teacher", command=self.add_teacher, bg='#27ae60', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Clear Form", command=self.clear_form, bg='#95a5a6', fg='white', width=12).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_teacher, bg='#e74c3c', fg='white', width=12).pack(side='left', padx=5)
        
        # Teacher List
        tk.Label(self.parent, text="Teachers List", font=("Arial", 14, "bold")).pack(pady=(20, 5))
        
        # Search
        search_frame = tk.Frame(self.parent)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_teachers)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        # Table
        columns = ("ID", "Name", "Emp ID", "Email", "Phone", "Subject", "Department", "Salary")
        self.tree = ttk.Treeview(self.parent, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        self.load_teachers()
        
    def add_teacher(self):
        name = self.name.get().strip()
        emp_id = self.emp_id.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        subject = self.subject.get()
        department = self.department.get()
        salary = self.salary.get().strip()
        gender = self.gender.get()
        
        if not name or not emp_id:
            messagebox.showerror("Error", "Name and Employee ID are required!")
            return
            
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO teachers (employee_id, full_name, gender, email, phone, subject, department, salary, hire_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (emp_id, name, gender, email, phone, subject, department, salary, datetime.now().date())
                )
                conn.commit()
                messagebox.showinfo("Success", f"Teacher {name} added successfully!")
                self.clear_form()
                self.load_teachers()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add teacher: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def load_teachers(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT teacher_id, full_name, employee_id, email, phone, subject, department, salary FROM teachers ORDER BY full_name")
                for row in cursor.fetchall():
                    self.tree.insert('', 'end', values=row)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load teachers: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def search_teachers(self, *args):
        search_text = self.search_var.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """SELECT teacher_id, full_name, employee_id, email, phone, subject, department, salary 
                          FROM teachers 
                          WHERE LOWER(full_name) LIKE %s OR LOWER(employee_id) LIKE %s 
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
    
    def delete_teacher(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a teacher to delete!")
            return
            
        item = selected[0]
        values = self.tree.item(item, 'values')
        teacher_id = values[0]
        teacher_name = values[1]
        
        result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {teacher_name}?")
        if result:
            conn = self.db.get_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM teachers WHERE teacher_id = %s", (teacher_id,))
                    conn.commit()
                    messagebox.showinfo("Success", f"Teacher {teacher_name} deleted successfully!")
                    self.load_teachers()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete teacher: {str(e)}")
                finally:
                    cursor.close()
                    conn.close()
    
    def clear_form(self):
        self.name.delete(0, tk.END)
        self.emp_id.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.salary.delete(0, tk.END)
        self.subject.set("Mathematics")
        self.department.set("IT")
        self.gender.set("Male")

# Test
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    root.title("Teacher Management")
    from database_config import DatabaseConfig
    db = DatabaseConfig()
    TeacherManagement(root, db, 1)
    root.mainloop()
