# ClassTrack - Student Management System

A complete student management system built with Python, Tkinter, and Live Docker MySQL. Perfect for schools and colleges to manage students, attendance, marks, and generate reports.

## Preview Screenshots

### Login
![Admin Dashboard](Screenshot/Screenshot%202025-08-28%20102710.png)

### Admin Dashboard
![Student Management](Screenshot/Screenshot%202025-08-28%20102717.png)

### Student Management
![Teacher Management](Screenshot/Screenshot%202025-08-28%20102731.png)

### Teacher Management
![Subject Management](Screenshot/Screenshot%202025-08-28%20102738.png)

### Subject Management
![Attendance Management](Screenshot/Screenshot%202025-08-28%20102743.png)

### Attendance Management
![Marks Management](Screenshot/Screenshot%202025-08-28%20102756.png)

### Marks Management
![Reports & Analytics](Screenshot/Screenshot%202025-08-28%20102810.png)

### Reports
![AI Assistant](Screenshot/Screenshot%202025-08-28%20102815.png)

### Settinggs
![Student Dashboard](Screenshot/Screenshot%202025-08-28%20102823.png)

### AI
![Student Features](Screenshot/Screenshot%202025-08-28%20102836.png)

## ✨ Features

- **👥 Student Management** - Add, edit, search students
- **📅 Attendance Tracking** - Daily attendance with subject-wise records  
- **📝 Marks & Grades** - Enter marks with automatic grade calculation
- **📊 Reports & Analytics** - Performance and attendance reports
- **🤖 AI Assistant** - Ask questions in natural language
- **🔐 Role-Based Access** - Admin, Teacher, Student roles

## 🚀 Quick Start

### Prerequisites
- Used Python 3.10+ Venv
- Docker & Docker Compose
- Mysql Database

### Installation
```bash
# 1. Clone the project
git clone https://github.com/immsamyak/ClassTrack.git
cd PyProject

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start database
docker-compose up -d

# 4. Run application
python main.py
```

### Manual Database Setup 

- Install Mysql server
- Create Database 
- Import class ``` classtrack_db.sql ```
- Setup ```localhost user root password ``` on ``` database_config.py```
``` 
def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.database = 'classtrack_db'
        self.username = 'admin'
        self.password = 'admin123'
 ```


## 🔑 Default Login

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 | admin
| Teacher | teacher1 | teacher123 |
| Student | (roll number) | student123 |

## 📁 Project Structure

```
PyProject/
├── main.py                    # Application entry point
├── dashboard.py               # Main dashboard
├── database_config.py         # Database setup
├── student_management.py      # Student CRUD operations
├── attendance_management.py   # Attendance tracking
├── marks_management.py        # Marks and grades
├── teacher_management.py      # Teacher management
├── subject_management.py      # Subject management
├── ai_chatbot.py             # AI assistant
└── requirements.txt          # Dependencies

```

## 🎯 User Guide

### For Admins/Teachers
1. **Add Students**: Navigate to Students → Fill form → Add Student
2. **Mark Attendance**: Go to Attendance → Select date/subject → Mark present/absent
3. **Enter Marks**: Go to Marks → Select exam details → Enter marks for students
4. **View Reports**: Check Reports section for analytics

### For Students  
1. **Login**: Use roll number (lowercase) as username
2. **View Data**: Check "My Attendance", "My Marks", "My Subjects"
3. **AI Assistant**: Ask questions like "What's my attendance?" or "Show my marks"

## 🤖 AI Assistant

Ask natural language questions:

**Students:**
- "What's my attendance percentage?"
- "How did I do in my last exam?"
- "Show my profile"

**Teachers/Admins:**
- "How is the class performing?"
- "Show attendance summary"
- "List all teachers"

## 🗄️ Database Access

**phpMyAdmin:** http://localhost:8080  
**Credentials:** admin / admin123

## 🔧 Troubleshooting

**Database issues:**
```bash
docker-compose down
docker-compose up -d
```

**Module errors:**
```bash
pip install -r requirements.txt
```

## 👥 Contributors

**BCSIT 2nd Semester Team:**
- @immsamyak         
- @lavye  
- Alisha Thapa
- Manjit Khadka
**OUR LC Numbers**
Alisha Thapa- LC00014001857
Manjit Khadka-LC00014001899
Samyak Kumar Chaudhary- LC00014001933
Saraswoti Shrestha- LC00014001937
---

*Built for - BCSIT 2nd Semester Python Project*
