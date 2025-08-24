# subject_management.py - Subject management module for Class Track system
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class SubjectManagement:
    def __init__(self, parent_frame, db_config, user_id):
        self.parent_frame = parent_frame
        self.db_config = db_config
        self.user_id = user_id
        
        self.create_subject_interface()
        
    def create_subject_interface(self):
        """Create the subject management interface"""
        # Title
        title_label = tk.Label(
            self.parent_frame,
            text="Subject Management",
            font=("Arial", 18, "bold"),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.parent_frame, bg='white')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Add subject form frame
        form_frame = tk.LabelFrame(main_container, text="Add New Subject", font=("Arial", 12, "bold"), bg='white')
        form_frame.pack(fill='x', pady=10)
        
        self.create_subject_form(form_frame)
        
        # Subjects list frame
        list_frame = tk.LabelFrame(main_container, text="Subjects List", font=("Arial", 12, "bold"), bg='white')
        list_frame.pack(fill='both', expand=True, pady=10)
        
        self.create_subjects_list(list_frame)
        
    def create_subject_form(self, parent):
        """Create the add subject form"""
        # Form fields frame
        fields_frame = tk.Frame(parent, bg='white')
        fields_frame.pack(pady=10, padx=10)
        
        # Row 1
        row1 = tk.Frame(fields_frame, bg='white')
        row1.pack(fill='x', pady=5)
        
        tk.Label(row1, text="Subject Name:", bg='white', width=15, anchor='w').pack(side='left', padx=5)
        self.subject_name_entry = tk.Entry(row1, width=25)
        self.subject_name_entry.pack(side='left', padx=5)
        
        tk.Label(row1, text="Subject Code:", bg='white', width=15, anchor='w').pack(side='left', padx=5)
        self.subject_code_entry = tk.Entry(row1, width=15)
        self.subject_code_entry.pack(side='left', padx=5)
        
        # Row 2
        row2 = tk.Frame(fields_frame, bg='white')
        row2.pack(fill='x', pady=5)
        
        tk.Label(row2, text="Semester:", bg='white', width=15, anchor='w').pack(side='left', padx=5)
        self.semester_combo = ttk.Combobox(row2, values=[
            "BCSIT 1st Sem", "BCSIT 2nd Sem", "BCSIT 3rd Sem", "BCSIT 4th Sem",
            "BCSIT 5th Sem", "BCSIT 6th Sem", "BCSIT 7th Sem", "BCSIT 8th Sem"
        ], width=22, state="readonly")
        self.semester_combo.pack(side='left', padx=5)
        self.semester_combo.set("BCSIT 2nd Sem")
        
        tk.Label(row2, text="Assign Teacher:", bg='white', width=15, anchor='w').pack(side='left', padx=5)
        self.teacher_combo = ttk.Combobox(row2, width=22, state="readonly")
        self.teacher_combo.pack(side='left', padx=5)
        
        # Row 3
        row3 = tk.Frame(fields_frame, bg='white')
        row3.pack(fill='x', pady=5)
        
        tk.Label(row3, text="Credit Hours:", bg='white', width=15, anchor='w').pack(side='left', padx=5)
        self.credit_hours_entry = tk.Entry(row3, width=10)
        self.credit_hours_entry.pack(side='left', padx=5)
        self.credit_hours_entry.insert(0, "3")
        
        tk.Label(row3, text="Description:", bg='white', width=15, anchor='w').pack(side='left', padx=5)
        self.description_entry = tk.Entry(row3, width=40)
        self.description_entry.pack(side='left', padx=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(parent, bg='white')
        buttons_frame.pack(pady=10)
        
        tk.Button(
            buttons_frame,
            text="Add Subject",
            bg='#27ae60',
            fg='white',
            font=("Arial", 10, "bold"),
            command=self.add_subject
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame,
            text="Update Subject",
            bg='#f39c12',
            fg='white',
            font=("Arial", 10, "bold"),
            command=self.update_subject
        ).pack(side='left', padx=5)
        
        tk.Button(
            buttons_frame,
            text="Clear Form",
            bg='#95a5a6',
            fg='white',
            font=("Arial", 10, "bold"),
            command=self.clear_form
        ).pack(side='left', padx=5)
        
        # Load teachers for dropdown
        self.load_teachers()
        
    def create_subjects_list(self, parent):
        """Create the subjects list with treeview"""
        # Filter frame
        filter_frame = tk.Frame(parent, bg='white')
        filter_frame.pack(fill='x', pady=5, padx=10)
        
        tk.Label(filter_frame, text="Filter by Semester:", bg='white').pack(side='left', padx=5)
        self.filter_semester_combo = ttk.Combobox(filter_frame, values=[
            "All Semesters", "BCSIT 1st Sem", "BCSIT 2nd Sem", "BCSIT 3rd Sem", "BCSIT 4th Sem",
            "BCSIT 5th Sem", "BCSIT 6th Sem", "BCSIT 7th Sem", "BCSIT 8th Sem"
        ], width=20, state="readonly")
        self.filter_semester_combo.pack(side='left', padx=5)
        self.filter_semester_combo.set("All Semesters")
        self.filter_semester_combo.bind('<<ComboboxSelected>>', self.filter_subjects)
        
        tk.Label(filter_frame, text="Search:", bg='white').pack(side='left', padx=(20, 5))
        self.search_entry = tk.Entry(filter_frame, width=25)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_subjects)
        
        tk.Button(
            filter_frame,
            text="Refresh",
            bg='#3498db',
            fg='white',
            command=self.load_subjects
        ).pack(side='right', padx=5)
        
        # Treeview frame
        tree_frame = tk.Frame(parent, bg='white')
        tree_frame.pack(fill='both', expand=True, pady=5, padx=10)
        
        # Treeview
        columns = ("ID", "Subject Code", "Subject Name", "Semester", "Teacher", "Credit Hours", "Description")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        # Define headings and column widths
        column_widths = {
            "ID": 50,
            "Subject Code": 100,
            "Subject Name": 180,
            "Semester": 120,
            "Teacher": 150,
            "Credit Hours": 80,
            "Description": 200
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_subject_select)
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Load subjects
        self.load_subjects()
        
    def load_teachers(self):
        """Load teachers for the dropdown"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT user_id, full_name FROM users WHERE role IN ('admin', 'teacher') ORDER BY full_name"
                cursor.execute(query)
                teachers = cursor.fetchall()
                
                teacher_list = [f"{teacher[1]} (ID: {teacher[0]})" for teacher in teachers]
                self.teacher_combo['values'] = teacher_list
                if teacher_list:
                    self.teacher_combo.set(teacher_list[0])
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load teachers: {str(e)}")
            finally:
                cursor.close()
                connection.close()
    
    def add_subject(self):
        """Add a new subject to the database"""
        subject_name = self.subject_name_entry.get().strip()
        subject_code = self.subject_code_entry.get().strip().upper()
        semester = self.semester_combo.get()
        teacher_text = self.teacher_combo.get()
        credit_hours = self.credit_hours_entry.get().strip()
        description = self.description_entry.get().strip()
        
        # Validation
        if not subject_name or not subject_code or not semester:
            messagebox.showerror("Error", "Subject Name, Subject Code, and Semester are required!")
            return
        
        if not teacher_text:
            messagebox.showerror("Error", "Please assign a teacher!")
            return
        
        try:
            credit_hours = int(credit_hours) if credit_hours else 3
        except ValueError:
            messagebox.showerror("Error", "Credit hours must be a number!")
            return
        
        # Extract teacher ID
        try:
            teacher_id = int(teacher_text.split("ID: ")[1].split(")")[0])
        except:
            messagebox.showerror("Error", "Invalid teacher selection!")
            return
        
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Check if subject code already exists
                check_query = "SELECT COUNT(*) FROM subjects WHERE subject_code = %s"
                cursor.execute(check_query, (subject_code,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Error", "Subject code already exists!")
                    return
                
                # Insert new subject
                insert_query = """
                INSERT INTO subjects (subject_name, subject_code, class_name, teacher_id, credit_hours, description)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (subject_name, subject_code, semester, teacher_id, credit_hours, description))
                
                connection.commit()
                messagebox.showinfo("Success", "Subject added successfully!")
                self.clear_form()
                self.load_subjects()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add subject: {str(e)}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
    
    def update_subject(self):
        """Update selected subject"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a subject to update!")
            return
        
        subject_data = self.tree.item(selected_item[0], 'values')
        subject_id = subject_data[0]
        
        subject_name = self.subject_name_entry.get().strip()
        subject_code = self.subject_code_entry.get().strip().upper()
        semester = self.semester_combo.get()
        teacher_text = self.teacher_combo.get()
        credit_hours = self.credit_hours_entry.get().strip()
        description = self.description_entry.get().strip()
        
        # Validation
        if not subject_name or not subject_code or not semester:
            messagebox.showerror("Error", "Subject Name, Subject Code, and Semester are required!")
            return
        
        if not teacher_text:
            messagebox.showerror("Error", "Please assign a teacher!")
            return
        
        try:
            credit_hours = int(credit_hours) if credit_hours else 3
        except ValueError:
            messagebox.showerror("Error", "Credit hours must be a number!")
            return
        
        # Extract teacher ID
        try:
            teacher_id = int(teacher_text.split("ID: ")[1].split(")")[0])
        except:
            messagebox.showerror("Error", "Invalid teacher selection!")
            return
        
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Check if subject code already exists for other subjects
                check_query = "SELECT COUNT(*) FROM subjects WHERE subject_code = %s AND subject_id != %s"
                cursor.execute(check_query, (subject_code, subject_id))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Error", "Subject code already exists!")
                    return
                
                # Update subject
                update_query = """
                UPDATE subjects 
                SET subject_name = %s, subject_code = %s, class_name = %s, teacher_id = %s, 
                    credit_hours = %s, description = %s
                WHERE subject_id = %s
                """
                cursor.execute(update_query, (subject_name, subject_code, semester, teacher_id, credit_hours, description, subject_id))
                
                connection.commit()
                messagebox.showinfo("Success", "Subject updated successfully!")
                self.clear_form()
                self.load_subjects()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update subject: {str(e)}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
    
    def on_subject_select(self, event):
        """Handle subject selection for editing"""
        selected_item = self.tree.selection()
        if selected_item:
            subject_data = self.tree.item(selected_item[0], 'values')
            
            # Fill form with selected subject data
            self.clear_form()
            self.subject_name_entry.insert(0, subject_data[2])  # Subject Name
            self.subject_code_entry.insert(0, subject_data[1])  # Subject Code
            self.semester_combo.set(subject_data[3])  # Semester
            self.credit_hours_entry.delete(0, tk.END)
            self.credit_hours_entry.insert(0, subject_data[5])  # Credit Hours
            self.description_entry.insert(0, subject_data[6])  # Description
            
            # Set teacher
            teacher_name = subject_data[4]
            for teacher_option in self.teacher_combo['values']:
                if teacher_name in teacher_option:
                    self.teacher_combo.set(teacher_option)
                    break
    
    def clear_form(self):
        """Clear the form fields"""
        self.subject_name_entry.delete(0, tk.END)
        self.subject_code_entry.delete(0, tk.END)
        self.semester_combo.set("BCSIT 2nd Sem")
        self.credit_hours_entry.delete(0, tk.END)
        self.credit_hours_entry.insert(0, "3")
        self.description_entry.delete(0, tk.END)
        if self.teacher_combo['values']:
            self.teacher_combo.set(self.teacher_combo['values'][0])
    
    def load_subjects(self):
        """Load subjects from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                SELECT s.subject_id, s.subject_code, s.subject_name, s.class_name, 
                       u.full_name, s.credit_hours, s.description
                FROM subjects s
                LEFT JOIN users u ON s.teacher_id = u.user_id
                ORDER BY s.class_name, s.subject_name
                """
                cursor.execute(query)
                subjects = cursor.fetchall()
                
                for subject in subjects:
                    # Handle None values
                    subject_list = list(subject)
                    for i, item in enumerate(subject_list):
                        if item is None:
                            subject_list[i] = "N/A"
                    self.tree.insert('', 'end', values=subject_list)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load subjects: {str(e)}")
            finally:
                cursor.close()
                connection.close()
    
    def filter_subjects(self, event=None):
        """Filter subjects by semester"""
        selected_semester = self.filter_semester_combo.get()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                if selected_semester == "All Semesters":
                    query = """
                    SELECT s.subject_id, s.subject_code, s.subject_name, s.class_name, 
                           u.full_name, s.credit_hours, s.description
                    FROM subjects s
                    LEFT JOIN users u ON s.teacher_id = u.user_id
                    ORDER BY s.class_name, s.subject_name
                    """
                    cursor.execute(query)
                else:
                    query = """
                    SELECT s.subject_id, s.subject_code, s.subject_name, s.class_name, 
                           u.full_name, s.credit_hours, s.description
                    FROM subjects s
                    LEFT JOIN users u ON s.teacher_id = u.user_id
                    WHERE s.class_name = %s
                    ORDER BY s.subject_name
                    """
                    cursor.execute(query, (selected_semester,))
                
                subjects = cursor.fetchall()
                for subject in subjects:
                    # Handle None values
                    subject_list = list(subject)
                    for i, item in enumerate(subject_list):
                        if item is None:
                            subject_list[i] = "N/A"
                    self.tree.insert('', 'end', values=subject_list)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to filter subjects: {str(e)}")
            finally:
                cursor.close()
                connection.close()
    
    def search_subjects(self, event=None):
        """Search subjects by name or code"""
        search_term = self.search_entry.get().strip()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                if search_term:
                    query = """
                    SELECT s.subject_id, s.subject_code, s.subject_name, s.class_name, 
                           u.full_name, s.credit_hours, s.description
                    FROM subjects s
                    LEFT JOIN users u ON s.teacher_id = u.user_id
                    WHERE s.subject_name LIKE %s OR s.subject_code LIKE %s
                    ORDER BY s.class_name, s.subject_name
                    """
                    cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
                else:
                    query = """
                    SELECT s.subject_id, s.subject_code, s.subject_name, s.class_name, 
                           u.full_name, s.credit_hours, s.description
                    FROM subjects s
                    LEFT JOIN users u ON s.teacher_id = u.user_id
                    ORDER BY s.class_name, s.subject_name
                    """
                    cursor.execute(query)
                
                subjects = cursor.fetchall()
                for subject in subjects:
                    # Handle None values
                    subject_list = list(subject)
                    for i, item in enumerate(subject_list):
                        if item is None:
                            subject_list[i] = "N/A"
                    self.tree.insert('', 'end', values=subject_list)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to search subjects: {str(e)}")
            finally:
                cursor.close()
                connection.close()
    
    def show_context_menu(self, event):
        """Show context menu for subject operations"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item:
            context_menu = tk.Menu(self.parent_frame, tearoff=0)
            context_menu.add_command(label="Edit Subject", command=lambda: self.on_subject_select(None))
            context_menu.add_command(label="Delete Subject", command=lambda: self.delete_subject(item))
            context_menu.add_separator()
            context_menu.add_command(label="View Subject Details", command=lambda: self.view_subject_details(item))
            context_menu.tk_popup(event.x_root, event.y_root)
    
    def delete_subject(self, item):
        """Delete selected subject"""
        subject_data = self.tree.item(item, 'values')
        subject_id = subject_data[0]
        subject_name = subject_data[2]
        
        # Check if subject has attendance or marks records
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Check attendance records
                cursor.execute("SELECT COUNT(*) FROM attendance WHERE subject_id = %s", (subject_id,))
                attendance_count = cursor.fetchone()[0]
                
                # Check marks records
                cursor.execute("SELECT COUNT(*) FROM marks WHERE subject_id = %s", (subject_id,))
                marks_count = cursor.fetchone()[0]
                
                if attendance_count > 0 or marks_count > 0:
                    warning_msg = f"Subject '{subject_name}' has {attendance_count} attendance records and {marks_count} marks records.\n"
                    warning_msg += "Deleting this subject will remove all related records. Are you sure?"
                    if not messagebox.askyesno("Warning", warning_msg):
                        return
                    
                    # Delete related records first
                    cursor.execute("DELETE FROM attendance WHERE subject_id = %s", (subject_id,))
                    cursor.execute("DELETE FROM marks WHERE subject_id = %s", (subject_id,))
                
                if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{subject_name}'?"):
                    # Delete subject
                    cursor.execute("DELETE FROM subjects WHERE subject_id = %s", (subject_id,))
                    
                    connection.commit()
                    messagebox.showinfo("Success", "Subject deleted successfully!")
                    self.load_subjects()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete subject: {str(e)}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
    
    def view_subject_details(self, item):
        """View detailed information about the subject"""
        subject_data = self.tree.item(item, 'values')
        subject_id = subject_data[0]
        
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Get detailed subject info
                query = """
                SELECT s.subject_name, s.subject_code, s.class_name, s.credit_hours, 
                       s.description, u.full_name, u.email
                FROM subjects s
                LEFT JOIN users u ON s.teacher_id = u.user_id
                WHERE s.subject_id = %s
                """
                cursor.execute(query, (subject_id,))
                subject_info = cursor.fetchone()
                
                # Get statistics
                cursor.execute("SELECT COUNT(*) FROM attendance WHERE subject_id = %s", (subject_id,))
                attendance_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM marks WHERE subject_id = %s", (subject_id,))
                marks_count = cursor.fetchone()[0]
                
                # Create details window
                details_window = tk.Toplevel()
                details_window.title(f"Subject Details - {subject_info[0]}")
                details_window.geometry("400x300")
                details_window.configure(bg='white')
                
                # Center the window
                details_window.update_idletasks()
                x = (details_window.winfo_screenwidth() // 2) - (400 // 2)
                y = (details_window.winfo_screenheight() // 2) - (300 // 2)
                details_window.geometry(f"400x300+{x}+{y}")
                
                # Details content
                details_text = f"""
Subject Name: {subject_info[0]}
Subject Code: {subject_info[1]}
Semester: {subject_info[2]}
Credit Hours: {subject_info[3]}
Description: {subject_info[4] or 'N/A'}

Assigned Teacher: {subject_info[5] or 'Not Assigned'}
Teacher Email: {subject_info[6] or 'N/A'}

Statistics:
• Total Attendance Records: {attendance_count}
• Total Marks Records: {marks_count}
                """
                
                tk.Label(
                    details_window,
                    text=details_text,
                    font=("Arial", 10),
                    bg='white',
                    justify='left',
                    anchor='nw'
                ).pack(padx=20, pady=20, fill='both', expand=True)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load subject details: {str(e)}")
            finally:
                cursor.close()
                connection.close()
