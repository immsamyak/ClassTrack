# database configuration
import mysql.connector
from mysql.connector import Error

class DatabaseConfig:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.database = 'classtrack_db'
        self.username = 'admin'
        self.password = 'admin123'
    
    def get_connection(self):
        """Create and return database connection"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def create_tables(self):
        """Create all required tables for the system"""
        connection = self.get_connection()
        if connection:
            cursor = connection.cursor()
            
            # Users table for login system
            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                role ENUM('admin', 'teacher', 'student') NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Students table
            create_students_table = """
            CREATE TABLE IF NOT EXISTS students (
                student_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT,
                roll_number VARCHAR(20) UNIQUE NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                gender ENUM('Male', 'Female', 'Other') NOT NULL,
                date_of_birth DATE,
                email VARCHAR(100) UNIQUE,
                phone VARCHAR(15),
                address TEXT,
                guardian_name VARCHAR(100),
                guardian_phone VARCHAR(15),
                class_name VARCHAR(50) NOT NULL,
                enrollment_date DATE,
                blood_group VARCHAR(5),
                emergency_contact VARCHAR(15),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            """
            
            # Subjects table
            create_subjects_table = """
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id INT PRIMARY KEY AUTO_INCREMENT,
                subject_name VARCHAR(100) NOT NULL,
                subject_code VARCHAR(20) UNIQUE NOT NULL,
                class_name VARCHAR(50) NOT NULL,
                teacher_id INT,
                credit_hours INT DEFAULT 3,
                description TEXT,
                FOREIGN KEY (teacher_id) REFERENCES users(user_id)
            )
            """
            
            # Teachers table
            create_teachers_table = """
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT,
                employee_id VARCHAR(20) UNIQUE NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                gender ENUM('Male', 'Female', 'Other') NOT NULL,
                date_of_birth DATE,
                email VARCHAR(100) UNIQUE,
                phone VARCHAR(15),
                department VARCHAR(50),
                qualification VARCHAR(200),
                specialization VARCHAR(200),
                experience_years INT,
                salary DECIMAL(10,2),
                address TEXT,
                hire_date DATE,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            """
            
            # Attendance table
            create_attendance_table = """
            CREATE TABLE IF NOT EXISTS attendance (
                attendance_id INT PRIMARY KEY AUTO_INCREMENT,
                student_id INT,
                subject_id INT,
                attendance_date DATE NOT NULL,
                status ENUM('present', 'absent') NOT NULL,
                marked_by INT,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
                FOREIGN KEY (marked_by) REFERENCES users(user_id)
            )
            """
            
            # Marks table
            create_marks_table = """
            CREATE TABLE IF NOT EXISTS marks (
                mark_id INT PRIMARY KEY AUTO_INCREMENT,
                student_id INT,
                subject_id INT,
                exam_type VARCHAR(50) NOT NULL,
                marks_obtained DECIMAL(5,2) NOT NULL,
                total_marks DECIMAL(5,2) NOT NULL,
                grade VARCHAR(2),
                exam_date DATE,
                entered_by INT,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
                FOREIGN KEY (entered_by) REFERENCES users(user_id)
            )
            """
            
            try:
                # Execute all table creation queries
                cursor.execute(create_users_table)
                cursor.execute(create_students_table)
                cursor.execute(create_subjects_table)
                cursor.execute(create_teachers_table)
                cursor.execute(create_attendance_table)
                cursor.execute(create_marks_table)
                
                # Insert default admin user
                insert_admin = """
                INSERT IGNORE INTO users (username, password, role, full_name, email)
                VALUES ('admin', 'admin123', 'admin', 'Administrator', 'admin@classtrack.com')
                """
                cursor.execute(insert_admin)
                
                # Insert sample teacher
                insert_teacher = """
                INSERT IGNORE INTO users (username, password, role, full_name, email)
                VALUES ('teacher1', 'teacher123', 'teacher', 'John Smith', 'john@classtrack.com')
                """
                cursor.execute(insert_teacher)
                
                # Insert sample subjects
                insert_subjects = """
                INSERT IGNORE INTO subjects (subject_name, subject_code, class_name, teacher_id, credit_hours, description)
                VALUES 
                ('Programming in C', 'CS101', 'BCSIT 2nd Sem', 2, 4, 'Introduction to C programming language'),
                ('Mathematics', 'MATH101', 'BCSIT 2nd Sem', 2, 3, 'Basic mathematics for computer science'),
                ('English', 'ENG101', 'BCSIT 2nd Sem', 2, 2, 'English communication skills'),
                ('Data Structures', 'CS201', 'BCSIT 2nd Sem', 2, 4, 'Data structures and algorithms'),
                ('Digital Logic', 'CS102', 'BCSIT 2nd Sem', 2, 3, 'Digital logic and computer organization')
                """
                cursor.execute(insert_subjects)
                
                connection.commit()
                print("Database tables created successfully!")
                
            except Error as e:
                print(f"Error creating tables: {e}")
            finally:
                cursor.close()
                connection.close()
