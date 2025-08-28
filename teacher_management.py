# Teacher Management - Simple and Working
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database_service import DatabaseService

class TeacherManagement:
    def __init__(self, parent_frame, db_config, user_id):
        self.parent = parent_frame
        self.db = db_config
        self.db_service = DatabaseService(db_config)
        
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
        tk.Label(form, text="Specialization:").grid(row=2, column=0, padx=5, pady=5)
        self.specialization = ttk.Combobox(form, width=22, state="readonly")
        self.specialization.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Department:").grid(row=2, column=2, padx=5, pady=5)
        self.department = ttk.Combobox(form, values=["Business", "IT"], width=17)
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
        tk.Button(btn_frame, text="Assign Subjects", command=self.assign_subjects, bg='#3498db', fg='white', width=12).pack(side='left', padx=5)
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
        columns = ("ID", "Name", "Emp ID", "Email", "Phone", "Assigned Subjects", "Department", "Salary")
        self.tree = ttk.Treeview(self.parent, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Assigned Subjects":
                self.tree.column(col, width=150)
            else:
                self.tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(20, 0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        self.load_specialization_dropdown()
        self.load_teachers()
        
    def load_specialization_dropdown(self):
        """Load subjects for specialization dropdown using shared service"""
        subjects = self.db_service.get_subject_names()
        if subjects:
            self.specialization['values'] = subjects
        else:
            # Fallback if database issue
            self.specialization['values'] = ["Mathematics", "English", "Science", "Computer Science"]
        
    def add_teacher(self):
        name = self.name.get().strip()
        emp_id = self.emp_id.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        specialization = self.specialization.get()
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
                
                # First, create user account
                username = emp_id.lower()  # Use employee ID as username
                password = "teacher123"  # Default password
                
                cursor.execute("""
                    INSERT INTO users (username, password, role, full_name, email) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (username, password, 'teacher', name, email))
                
                user_id = cursor.lastrowid
                
                # Then, create teacher record with user_id
                cursor.execute("""
                    INSERT INTO teachers (user_id, employee_id, full_name, gender, email, phone, specialization, department, salary, hire_date) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, emp_id, name, gender, email, phone, specialization, department, salary, datetime.now().date()))
                
                conn.commit()
                messagebox.showinfo("Success", f"Teacher {name} added successfully!\nLogin: {username} | Password: {password}")
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
                # Get teachers with their assigned subjects
                query = """
                SELECT t.teacher_id, t.full_name, t.employee_id, t.email, t.phone, 
                       GROUP_CONCAT(s.subject_name SEPARATOR ', ') as assigned_subjects,
                       t.department, t.salary
                FROM teachers t
                LEFT JOIN subjects s ON t.user_id = s.teacher_id
                GROUP BY t.teacher_id, t.full_name, t.employee_id, t.email, t.phone, t.department, t.salary
                ORDER BY t.full_name
                """
                cursor.execute(query)
                for row in cursor.fetchall():
                    # Replace None with "No subjects assigned"
                    row_list = list(row)
                    if row_list[5] is None:
                        row_list[5] = "No subjects assigned"
                    self.tree.insert('', 'end', values=row_list)
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
                query = """
                SELECT t.teacher_id, t.full_name, t.employee_id, t.email, t.phone, 
                       GROUP_CONCAT(s.subject_name SEPARATOR ', ') as assigned_subjects,
                       t.department, t.salary
                FROM teachers t
                LEFT JOIN subjects s ON t.user_id = s.teacher_id
                WHERE LOWER(t.full_name) LIKE %s OR LOWER(t.employee_id) LIKE %s 
                GROUP BY t.teacher_id, t.full_name, t.employee_id, t.email, t.phone, t.department, t.salary
                ORDER BY t.full_name
                """
                pattern = f"%{search_text}%"
                cursor.execute(query, (pattern, pattern))
                for row in cursor.fetchall():
                    # Replace None with "No subjects assigned"
                    row_list = list(row)
                    if row_list[5] is None:
                        row_list[5] = "No subjects assigned"
                    self.tree.insert('', 'end', values=row_list)
            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")
            finally:
                cursor.close()
                conn.close()
    
    def assign_subjects(self):
        """Open a dialog to assign subjects to selected teacher"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a teacher to assign subjects!")
            return
            
        item = selected[0]
        values = self.tree.item(item, 'values')
        teacher_id = values[0]
        teacher_name = values[1]
        
        # Create assignment window
        assign_window = tk.Toplevel(self.parent)
        assign_window.title(f"Assign Subjects to {teacher_name}")
        assign_window.geometry("600x400")
        assign_window.grab_set()
        
        tk.Label(assign_window, text=f"Assign Subjects to: {teacher_name}", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Get teacher's user_id
        conn = self.db.get_connection()
        if not conn:
            messagebox.showerror("Error", "Database connection failed!")
            assign_window.destroy()
            return
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM teachers WHERE teacher_id = %s", (teacher_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Teacher not found!")
                assign_window.destroy()
                return
            teacher_user_id = result[0]
            
            # Get all subjects
            cursor.execute("SELECT subject_id, subject_name, class_name, teacher_id FROM subjects ORDER BY class_name, subject_name")
            subjects = cursor.fetchall()
            
            # Create listbox with checkboxes
            frame = tk.Frame(assign_window)
            frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            # Headers
            header_frame = tk.Frame(frame)
            header_frame.pack(fill='x', pady=5)
            tk.Label(header_frame, text="Assign", font=("Arial", 10, "bold"), width=8).pack(side='left')
            tk.Label(header_frame, text="Subject", font=("Arial", 10, "bold"), width=25, anchor='w').pack(side='left')
            tk.Label(header_frame, text="Class", font=("Arial", 10, "bold"), width=15, anchor='w').pack(side='left')
            tk.Label(header_frame, text="Current Teacher", font=("Arial", 10, "bold"), width=20, anchor='w').pack(side='left')
            
            # Scrollable frame
            canvas = tk.Canvas(frame)
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Subject checkboxes
            subject_vars = {}
            for subject_id, subject_name, class_name, current_teacher_id in subjects:
                row_frame = tk.Frame(scrollable_frame)
                row_frame.pack(fill='x', pady=2)
                
                # Checkbox
                var = tk.BooleanVar()
                if current_teacher_id == teacher_user_id:
                    var.set(True)
                
                subject_vars[subject_id] = var
                tk.Checkbutton(row_frame, variable=var, width=8).pack(side='left')
                
                # Subject name
                tk.Label(row_frame, text=subject_name, width=25, anchor='w').pack(side='left')
                
                # Class
                tk.Label(row_frame, text=class_name, width=15, anchor='w').pack(side='left')
                
                # Current teacher
                current_teacher = "Not Assigned"
                if current_teacher_id:
                    cursor.execute("SELECT full_name FROM teachers WHERE user_id = %s", (current_teacher_id,))
                    result = cursor.fetchone()
                    if result:
                        current_teacher = result[0]
                
                tk.Label(row_frame, text=current_teacher, width=20, anchor='w').pack(side='left')
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Buttons
            btn_frame = tk.Frame(assign_window)
            btn_frame.pack(pady=10)
            
            def save_assignments():
                # Create a new connection for the save operation
                save_conn = self.db.get_connection()
                if not save_conn:
                    messagebox.showerror("Error", "Database connection failed!")
                    return
                
                try:
                    save_cursor = save_conn.cursor()
                    
                    for subject_id, var in subject_vars.items():
                        if var.get():
                            # Assign this teacher to the subject
                            save_cursor.execute("UPDATE subjects SET teacher_id = %s WHERE subject_id = %s", 
                                         (teacher_user_id, subject_id))
                        else:
                            # Check if this teacher was previously assigned and remove if so
                            save_cursor.execute("SELECT teacher_id FROM subjects WHERE subject_id = %s", (subject_id,))
                            current = save_cursor.fetchone()
                            if current and current[0] == teacher_user_id:
                                save_cursor.execute("UPDATE subjects SET teacher_id = NULL WHERE subject_id = %s", 
                                             (subject_id,))
                    
                    save_conn.commit()
                    messagebox.showinfo("Success", f"Subject assignments updated for {teacher_name}!")
                    assign_window.destroy()
                    self.load_teachers()  # Refresh the teacher list
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update assignments: {str(e)}")
                finally:
                    save_cursor.close()
                    save_conn.close()
            
            tk.Button(btn_frame, text="Save Assignments", command=save_assignments, 
                     bg='#27ae60', fg='white', width=15).pack(side='left', padx=5)
            tk.Button(btn_frame, text="Cancel", command=assign_window.destroy, 
                     bg='#95a5a6', fg='white', width=10).pack(side='left', padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load assignment dialog: {str(e)}")
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
        
        # Check if teacher is assigned to any subjects
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM subjects WHERE teacher_id = %s", (teacher_id,))
                subject_count = cursor.fetchone()[0]
                
                if subject_count > 0:
                    warning_msg = f"Cannot delete {teacher_name} because:\n"
                    warning_msg += f"• Teacher is assigned to {subject_count} subject(s)\n"
                    warning_msg += "\nRemove teacher from subjects first, or contact administrator."
                    
                    messagebox.showwarning("Cannot Delete", warning_msg)
                    return
                
                # If no dependencies, confirm deletion
                result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {teacher_name}?")
                if result:
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
        if self.specialization['values']:
            self.specialization.set(self.specialization['values'][0])
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
