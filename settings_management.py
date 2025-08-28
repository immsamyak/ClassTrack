# Simple Settings for Beginner Students - Only School Information
import tkinter as tk
from tkinter import ttk, messagebox
from database_config import DatabaseConfig


class DatabaseSettingsManager:
    
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.create_table()
    
    def create_table(self):
        conn = self.db_config.get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    setting_name VARCHAR(50) PRIMARY KEY,
                    setting_value TEXT
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
    
    def get_setting(self, name):
        conn = self.db_config.get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT setting_value FROM settings WHERE setting_name = %s", (name,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result[0] if result else None
        return None
    
    def save_setting(self, name, value):
        conn = self.db_config.get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO settings (setting_name, setting_value) 
                VALUES (%s, %s) 
                ON DUPLICATE KEY UPDATE setting_value = %s
            """, (name, value, value))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        return False
    
    def get_all_settings(self):
        conn = self.db_config.get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT setting_name, setting_value FROM settings")
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            
            settings = {}
            for name, value in results:
                settings[name] = value
            return settings
        return {}


class SettingsManagement:
    
    def __init__(self, parent, db_config, user_id):
        self.parent = parent
        self.settings_manager = DatabaseSettingsManager()
        self.create_interface()
        self.load_settings()
    
    def create_interface(self):
        # Title
        tk.Label(self.parent, text="🏫 School Information Settings", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        # Form frame
        form = tk.Frame(self.parent)
        form.pack(pady=20, padx=50)
        
        # School information fields
        self.school_vars = {}
        fields = [
            ("school_name", "School Name:"),
            ("school_address", "School Address:"),
            ("school_phone", "School Phone:"),
            ("school_email", "School Email:"),
            ("principal_name", "Principal Name:")
        ]
        
        for i, (key, label) in enumerate(fields):
            # Label
            tk.Label(form, text=label, font=("Arial", 12)).grid(
                row=i, column=0, sticky='w', padx=10, pady=10)
            
            # Entry box
            self.school_vars[key] = tk.StringVar()
            tk.Entry(form, textvariable=self.school_vars[key], 
                    font=("Arial", 12), width=30).grid(
                row=i, column=1, padx=10, pady=10)
        
        # Buttons
        button_frame = tk.Frame(self.parent)
        button_frame.pack(pady=30)
        
        tk.Button(button_frame, text="💾 Save Settings", 
                 command=self.save_settings, bg='#27ae60', fg='white',
                 font=("Arial", 12), width=15).pack(side='left', padx=10)
        
        tk.Button(button_frame, text="🔄 Clear All", 
                 command=self.reset_settings, bg='#95a5a6', fg='white',
                 font=("Arial", 12), width=15).pack(side='left', padx=10)
    
    def load_settings(self):
        for key in self.school_vars:
            value = self.settings_manager.get_setting(key)
            if value:
                self.school_vars[key].set(value)
    
    def save_settings(self):
        try:
            for key, var in self.school_vars.items():
                self.settings_manager.save_setting(key, var.get())
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")
    
    def reset_settings(self):
        if messagebox.askyesno("Reset", "Reset all settings to empty?"):
            conn = self.settings_manager.db_config.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM settings")
                conn.commit()
                cursor.close()
                conn.close()
            self.load_settings()
            messagebox.showinfo("Success", "Settings cleared!")


# Simple helper functions
def get_setting(name):
    manager = DatabaseSettingsManager()
    return manager.get_setting(name)

def save_setting(name, value):
    manager = DatabaseSettingsManager()
    return manager.save_setting(name, value)


# Test the settings module if run directly
if __name__ == "__main__":
    # Simple test
    root = tk.Tk()
    root.title("School Settings Test")
    root.geometry("600x400")
    
    from database_config import DatabaseConfig
    db = DatabaseConfig()
    
    SettingsManagement(root, db, 1)
    root.mainloop()
