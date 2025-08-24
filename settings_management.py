"""
Database-based Settings Management Module for Class Track System
Simple and beginner-friendly code that stores all settings in MySQL database
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database_config import DatabaseConfig
from datetime import datetime


class DatabaseSettingsManager:
    """
    Simple class to manage settings in database
    All settings are stored in 'settings' table
    """
    
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.create_settings_table()
        self.load_default_settings()
    
    def create_settings_table(self):
        """Create settings table if it doesn't exist"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Create settings table
                create_table_query = """
                CREATE TABLE IF NOT EXISTS settings (
                    setting_id INT AUTO_INCREMENT PRIMARY KEY,
                    setting_name VARCHAR(100) UNIQUE NOT NULL,
                    setting_value TEXT,
                    setting_description VARCHAR(255),
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_table_query)
                connection.commit()
                print("✓ Settings table created/verified")
                
                cursor.close()
                connection.close()
                
            except Exception as e:
                print(f"Error creating settings table: {e}")
    
    def load_default_settings(self):
        """Load default settings if they don't exist"""
        default_settings = {
            'school_name': 'Class Track School',
            'academic_year': '2024-2025',
            'semester': 'Fall 2024',
            'school_address': '123 Education Street, Learning City',
            'school_phone': '+1-234-567-8900',
            'school_email': 'info@classtrack.edu',
            'principal_name': 'Dr. John Smith',
            'attendance_percentage_required': '75',
            'passing_marks_percentage': '40',
            'grade_a_percentage': '90',
            'grade_b_percentage': '80',
            'grade_c_percentage': '70',
            'grade_d_percentage': '40',
            'backup_enabled': 'true',
            'notification_enabled': 'true',
            'theme': 'default'
        }
        
        # Add default settings if they don't exist
        for setting_name, setting_value in default_settings.items():
            if not self.get_setting(setting_name):
                self.save_setting(setting_name, setting_value)
    
    def get_setting(self, setting_name):
        """Get a setting value from database"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                query = "SELECT setting_value FROM settings WHERE setting_name = %s"
                cursor.execute(query, (setting_name,))
                result = cursor.fetchone()
                
                cursor.close()
                connection.close()
                
                if result:
                    return result[0]
                else:
                    return None
                    
            except Exception as e:
                print(f"Error getting setting {setting_name}: {e}")
                return None
        return None
    
    def save_setting(self, setting_name, setting_value):
        """Save a setting to database"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Use INSERT ... ON DUPLICATE KEY UPDATE to handle both insert and update
                query = """
                INSERT INTO settings (setting_name, setting_value) 
                VALUES (%s, %s) 
                ON DUPLICATE KEY UPDATE setting_value = %s
                """
                cursor.execute(query, (setting_name, setting_value, setting_value))
                connection.commit()
                
                cursor.close()
                connection.close()
                return True
                
            except Exception as e:
                print(f"Error saving setting {setting_name}: {e}")
                return False
        return False
    
    def get_all_settings(self):
        """Get all settings from database"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                query = "SELECT setting_name, setting_value FROM settings ORDER BY setting_name"
                cursor.execute(query)
                results = cursor.fetchall()
                
                cursor.close()
                connection.close()
                
                # Convert to dictionary
                settings_dict = {}
                for setting_name, setting_value in results:
                    settings_dict[setting_name] = setting_value
                
                return settings_dict
                
            except Exception as e:
                print(f"Error getting all settings: {e}")
                return {}
        return {}


class SettingsManagement:
    """
    Simple GUI for managing settings
    Easy to understand for beginners
    """
    
    def __init__(self, parent, db_config, user_id):
        self.parent = parent
        self.db_config = db_config
        self.user_id = user_id
        
        # Initialize settings manager
        self.settings_manager = DatabaseSettingsManager()
        
        # Create GUI
        self.create_settings_interface()
        self.load_current_settings()
    
    def create_settings_interface(self):
        """Create simple settings interface"""
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="⚙️ System Settings",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # School Information Tab
        self.create_school_info_tab()
        
        # Academic Settings Tab
        self.create_academic_settings_tab()
        
        # System Settings Tab
        self.create_system_settings_tab()
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        # Save button
        save_button = ttk.Button(
            buttons_frame,
            text="💾 Save Settings",
            command=self.save_all_settings
        )
        save_button.pack(side='left', padx=(0, 10))
        
        # Reset button
        reset_button = ttk.Button(
            buttons_frame,
            text="🔄 Reset to Default",
            command=self.reset_to_default
        )
        reset_button.pack(side='left', padx=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(
            buttons_frame,
            text="Ready",
            foreground="green"
        )
        self.status_label.pack(side='right')
    
    def create_school_info_tab(self):
        """Create school information settings tab"""
        # School Info Frame
        school_frame = ttk.Frame(self.notebook)
        self.notebook.add(school_frame, text="🏫 School Info")
        
        # Create scrollable frame
        canvas = tk.Canvas(school_frame)
        scrollbar = ttk.Scrollbar(school_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # School settings
        school_settings = [
            ("school_name", "School Name:", "text"),
            ("school_address", "School Address:", "text"),
            ("school_phone", "School Phone:", "text"),
            ("school_email", "School Email:", "text"),
            ("principal_name", "Principal Name:", "text"),
        ]
        
        self.school_vars = {}
        
        for i, (key, label, widget_type) in enumerate(school_settings):
            # Label
            ttk.Label(
                scrollable_frame,
                text=label,
                font=("Arial", 10, "bold")
            ).grid(row=i, column=0, sticky='w', padx=10, pady=5)
            
            # Entry
            self.school_vars[key] = tk.StringVar()
            entry = ttk.Entry(
                scrollable_frame,
                textvariable=self.school_vars[key],
                font=("Arial", 10),
                width=40
            )
            entry.grid(row=i, column=1, sticky='ew', padx=10, pady=5)
        
        # Configure grid
        scrollable_frame.columnconfigure(1, weight=1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_academic_settings_tab(self):
        """Create academic settings tab"""
        # Academic Frame
        academic_frame = ttk.Frame(self.notebook)
        self.notebook.add(academic_frame, text="📚 Academic")
        
        # Create scrollable frame
        canvas = tk.Canvas(academic_frame)
        scrollbar = ttk.Scrollbar(academic_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Academic settings
        academic_settings = [
            ("academic_year", "Academic Year:", "text"),
            ("semester", "Current Semester:", "text"),
            ("attendance_percentage_required", "Required Attendance %:", "number"),
            ("passing_marks_percentage", "Passing Marks %:", "number"),
            ("grade_a_percentage", "Grade A % (90+ default):", "number"),
            ("grade_b_percentage", "Grade B % (80+ default):", "number"),
            ("grade_c_percentage", "Grade C % (70+ default):", "number"),
            ("grade_d_percentage", "Grade D % (40+ default):", "number"),
        ]
        
        self.academic_vars = {}
        
        for i, (key, label, widget_type) in enumerate(academic_settings):
            # Label
            ttk.Label(
                scrollable_frame,
                text=label,
                font=("Arial", 10, "bold")
            ).grid(row=i, column=0, sticky='w', padx=10, pady=5)
            
            # Entry
            self.academic_vars[key] = tk.StringVar()
            entry = ttk.Entry(
                scrollable_frame,
                textvariable=self.academic_vars[key],
                font=("Arial", 10),
                width=40
            )
            entry.grid(row=i, column=1, sticky='ew', padx=10, pady=5)
        
        # Configure grid
        scrollable_frame.columnconfigure(1, weight=1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_system_settings_tab(self):
        """Create system settings tab"""
        # System Frame
        system_frame = ttk.Frame(self.notebook)
        self.notebook.add(system_frame, text="💻 System")
        
        # Create scrollable frame
        canvas = tk.Canvas(system_frame)
        scrollbar = ttk.Scrollbar(system_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.system_vars = {}
        
        # Backup Settings
        ttk.Label(
            scrollable_frame,
            text="Backup Settings:",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=(10, 5))
        
        self.system_vars['backup_enabled'] = tk.BooleanVar()
        backup_check = ttk.Checkbutton(
            scrollable_frame,
            text="Enable automatic backups",
            variable=self.system_vars['backup_enabled']
        )
        backup_check.grid(row=1, column=0, columnspan=2, sticky='w', padx=20, pady=5)
        
        # Notification Settings
        ttk.Label(
            scrollable_frame,
            text="Notification Settings:",
            font=("Arial", 12, "bold")
        ).grid(row=2, column=0, columnspan=2, sticky='w', padx=10, pady=(20, 5))
        
        self.system_vars['notification_enabled'] = tk.BooleanVar()
        notification_check = ttk.Checkbutton(
            scrollable_frame,
            text="Enable notifications",
            variable=self.system_vars['notification_enabled']
        )
        notification_check.grid(row=3, column=0, columnspan=2, sticky='w', padx=20, pady=5)
        
        # Theme Settings
        ttk.Label(
            scrollable_frame,
            text="Theme:",
            font=("Arial", 10, "bold")
        ).grid(row=4, column=0, sticky='w', padx=10, pady=(20, 5))
        
        self.system_vars['theme'] = tk.StringVar()
        theme_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.system_vars['theme'],
            values=["default", "dark", "light"],
            state="readonly",
            width=37
        )
        theme_combo.grid(row=4, column=1, sticky='ew', padx=10, pady=5)
        
        # Configure grid
        scrollable_frame.columnconfigure(1, weight=1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def load_current_settings(self):
        """Load current settings from database"""
        try:
            all_settings = self.settings_manager.get_all_settings()
            
            # Load school settings
            for key in self.school_vars:
                if key in all_settings:
                    self.school_vars[key].set(all_settings[key])
            
            # Load academic settings
            for key in self.academic_vars:
                if key in all_settings:
                    self.academic_vars[key].set(all_settings[key])
            
            # Load system settings
            if 'backup_enabled' in all_settings:
                self.system_vars['backup_enabled'].set(all_settings['backup_enabled'] == 'true')
            
            if 'notification_enabled' in all_settings:
                self.system_vars['notification_enabled'].set(all_settings['notification_enabled'] == 'true')
            
            if 'theme' in all_settings:
                self.system_vars['theme'].set(all_settings['theme'])
            
            self.status_label.config(text="Settings loaded", foreground="green")
            
        except Exception as e:
            self.status_label.config(text=f"Error loading settings: {e}", foreground="red")
    
    def save_all_settings(self):
        """Save all settings to database"""
        try:
            # Save school settings
            for key, var in self.school_vars.items():
                self.settings_manager.save_setting(key, var.get())
            
            # Save academic settings
            for key, var in self.academic_vars.items():
                self.settings_manager.save_setting(key, var.get())
            
            # Save system settings
            self.settings_manager.save_setting(
                'backup_enabled', 
                'true' if self.system_vars['backup_enabled'].get() else 'false'
            )
            self.settings_manager.save_setting(
                'notification_enabled', 
                'true' if self.system_vars['notification_enabled'].get() else 'false'
            )
            self.settings_manager.save_setting('theme', self.system_vars['theme'].get())
            
            self.status_label.config(text="✓ Settings saved successfully!", foreground="green")
            messagebox.showinfo("Success", "Settings saved to database successfully!")
            
        except Exception as e:
            self.status_label.config(text=f"✗ Error saving: {e}", foreground="red")
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def reset_to_default(self):
        """Reset all settings to default values"""
        result = messagebox.askyesno(
            "Reset Settings",
            "Are you sure you want to reset all settings to default values?"
        )
        
        if result:
            try:
                # Clear current settings from database
                connection = self.settings_manager.db_config.get_connection()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM settings")
                    connection.commit()
                    cursor.close()
                    connection.close()
                
                # Reload default settings
                self.settings_manager.load_default_settings()
                
                # Reload GUI with default values
                self.load_current_settings()
                
                self.status_label.config(text="✓ Reset to default values", foreground="green")
                messagebox.showinfo("Success", "Settings reset to default values!")
                
            except Exception as e:
                self.status_label.config(text=f"✗ Error resetting: {e}", foreground="red")
                messagebox.showerror("Error", f"Failed to reset settings: {e}")


# Helper function to get setting value (for use in other modules)
def get_setting(setting_name):
    """
    Simple function to get a setting value from database
    Can be used by other modules
    """
    settings_manager = DatabaseSettingsManager()
    return settings_manager.get_setting(setting_name)


# Helper function to save setting value (for use in other modules)
def save_setting(setting_name, setting_value):
    """
    Simple function to save a setting value to database
    Can be used by other modules
    """
    settings_manager = DatabaseSettingsManager()
    return settings_manager.save_setting(setting_name, setting_value)


# Test function
def test_settings():
    """Test the settings module"""
    print("Testing Settings Module...")
    
    # Test settings manager
    settings_manager = DatabaseSettingsManager()
    
    # Test saving and getting settings
    test_result = settings_manager.save_setting("test_setting", "test_value")
    if test_result:
        retrieved_value = settings_manager.get_setting("test_setting")
        if retrieved_value == "test_value":
            print("✓ Settings save and retrieve works!")
        else:
            print("✗ Settings retrieve failed")
    else:
        print("✗ Settings save failed")
    
    # Test getting all settings
    all_settings = settings_manager.get_all_settings()
    print(f"✓ Found {len(all_settings)} settings in database")
    
    print("Settings module test completed!")


if __name__ == "__main__":
    test_settings()
