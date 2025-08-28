# Database Service - Common database operations
class DatabaseService:
    def __init__(self, db_config):
        self.db = db_config
    
    def get_subject_names(self):
        """Get all subject names for dropdowns"""
        try:
            conn = self.db.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT subject_name FROM subjects ORDER BY subject_name")
                subjects = [row[0] for row in cursor.fetchall()]
                cursor.close()
                conn.close()
                return subjects
        except:
            pass
        return []
    
    def get_teacher_names(self):
        """Get all teacher names for dropdowns"""
        try:
            conn = self.db.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT full_name FROM teachers ORDER BY full_name")
                teachers = [row[0] for row in cursor.fetchall()]
                cursor.close()
                conn.close()
                return teachers
        except:
            pass
        return []
    
    def get_subjects_by_semester(self, semester):
        """Get subjects for a specific semester"""
        try:
            conn = self.db.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT subject_id, subject_name FROM subjects WHERE class_name = %s", (semester,))
                subjects = cursor.fetchall()
                cursor.close()
                conn.close()
                return subjects
        except:
            pass
        return []
