# Class Track - Student Management System

A comprehensive GUI-based student management system built with Python and MySQL. This project is designed for educational institutions to manage students, track attendance, record marks, and generate reports.

## Features

### 🎯 Core Modules
- **Student Management**: Add, edit, delete, and search student records
- **Attendance Tracking**: Mark daily attendance with date-wise records
- **Marks & Grades**: Enter marks and auto-generate grades (A, B, C, etc.)
- **Reports & Analytics**: View attendance and academic performance reports
- **AI Chatbot Assistant**: Natural language queries for data and insights
- **Role-based Access**: Admin, Teacher, and Student login roles

### 🤖 AI Assistant Features
- **Natural Language Queries**: Ask questions in plain English
- **Role-Based Responses**: Students see personal data, teachers see class data
- **Real-Time Database**: Fresh information from your MySQL database
- **Smart Insights**: Helpful tips and analysis of your data
- **Quick Actions**: Shortcut buttons for common queries

### 🔐 User Roles
- **Admin**: Full system access, user management, reports, AI insights
- **Teacher**: Student management, attendance marking, marks entry, class analytics
- **Student**: View personal attendance and marks, AI-powered personal insights

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Docker and Docker Compose
- Git (optional)

### Installation Steps

1. **Clone or Download the Project**
   ```bash
   git clone <repository-url>
   cd PyProject
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start MySQL Database with Docker**
   ```bash
   docker-compose up -d
   ```
   This starts:
   - MySQL Server on port 3306
   - phpMyAdmin on port 8080

4. **Run the Application**
   ```bash
   python main.py
   ```

## 🔑 Default Login Credentials

### Admin Access
- **Username**: admin
- **Password**: admin123

### Teacher Access
- **Username**: teacher1
- **Password**: teacher123

### Student Access
Students are created when added through the system. Default password for all students is `student123`.

## 🗄️ Database Access

### phpMyAdmin
- **URL**: http://localhost:8080
- **Username**: admin
- **Password**: admin123

### Direct MySQL Connection
- **Host**: localhost
- **Port**: 3306
- **Database**: classtrack_db
- **Username**: admin
- **Password**: admin123

## 📁 Project Structure

```
PyProject/
├── main.py                     # Main application entry point
├── login.py                    # Login window
├── dashboard.py                # Main dashboard
├── database_config.py          # Database configuration
├── student_management.py       # Student management module
├── attendance_management.py    # Attendance tracking module
├── marks_management.py         # Marks and grades module
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker configuration
└── README.md                   # This file
```

## 🎓 Usage Guide

### 🤖 Using the AI Assistant

1. **Access the AI Assistant**
   - Login to the system
   - Click "🤖 AI Assistant" in the sidebar
   - Start asking questions in natural language

2. **Example Queries**
   
   **Students can ask:**
   - "What's my attendance?"
   - "How did I do in my exams?"
   - "Show my profile information"
   - "What subjects do I have?"

   **Teachers/Admins can ask:**
   - "How is my class doing?"
   - "Show class attendance summary"
   - "List of all teachers"
   - "Class performance report"

3. **Quick Action Buttons**
   - Use shortcut buttons for common queries
   - Different buttons appear based on your role

### For Teachers/Admins

1. **Adding Students**
   - Login with admin/teacher credentials
   - Navigate to "Students" from sidebar
   - Fill the form and click "Add Student"
   - Student login credentials are auto-generated

2. **Marking Attendance**
   - Go to "Attendance" module
   - Select date, subject, and class
   - Click "Load Students"
   - Mark present/absent for each student
   - Click "Save Attendance"

3. **Entering Marks**
   - Go to "Marks" module
   - Select class, subject, and exam type
   - Enter total marks and exam date
   - Click "Load Students"
   - Enter marks for each student
   - Click "Save Marks"

### For Students

1. **Login**
   - Use roll number as username (lowercase)
   - Default password: student123

2. **View Records**
   - Dashboard shows overview
   - "My Attendance" shows attendance records
   - "My Marks" shows academic performance

## 🛠️ Technical Details

### Database Schema

#### Users Table
- user_id (Primary Key)
- username, password, role
- full_name, email
- created_date

#### Students Table
- student_id (Primary Key)
- user_id (Foreign Key)
- roll_number, full_name
- class_name, phone, address
- enrollment_date

#### Subjects Table
- subject_id (Primary Key)
- subject_name, subject_code
- class_name, teacher_id

#### Attendance Table
- attendance_id (Primary Key)
- student_id, subject_id
- attendance_date, status
- marked_by (teacher_id)

#### Marks Table
- mark_id (Primary Key)
- student_id, subject_id
- exam_type, marks_obtained
- total_marks, grade
- exam_date, entered_by

### Grading System
- A+ : 90-100%
- A  : 80-89%
- B+ : 70-79%
- B  : 60-69%
- C+ : 50-59%
- C  : 40-49%
- D  : 32-39%
- F  : Below 32%

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Start Docker containers
   docker-compose up -d
   
   # Check if containers are running
   docker ps
   ```

2. **Module Import Errors**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Port Already in Use**
   ```bash
   # Stop existing containers
   docker-compose down
   
   # Start again
   docker-compose up -d
   ```

### Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# Restart services
docker-compose restart
```

## 📝 Development Notes

This project is designed as a learning exercise for BCSIT 2nd semester students. The code follows beginner-friendly patterns while maintaining functionality:

- Simple, readable code structure
- Clear variable and function names
- Comprehensive comments
- Error handling
- User-friendly interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is created for educational purposes. Feel free to use and modify as needed.

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review database connections
3. Ensure Docker is running
4. Check Python dependencies

---

**Created by BCSIT 2nd Semester Students**  
*Building the future, one line of code at a time* 🚀
