"""
AI Chatbot Module for Class Track - Student Management System
This module provides an intelligent chatbot interface for students, teachers, and admins
to query information from the system using natural language.

Features:
- Natural language query processing
- Role-based access control
- Database integration for real-time data
- GUI integration with Tkinter
- Contextual responses based on user role
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re
import json
from datetime import datetime, timedelta
from database_config import DatabaseConfig
import threading


class ClassTrackChatbot:
    """
    Main chatbot class that handles natural language processing,
    database queries, and response generation for the Class Track system.
    """
    
    def __init__(self, user_id, user_role, user_name):
        self.user_id = user_id
        self.user_role = user_role
        self.user_name = user_name
        self.db_config = DatabaseConfig()
        
        # Initialize conversation context
        self.conversation_history = []
        self.last_query_type = None
        
        # Define query patterns and their handlers
        self.query_patterns = {
            # Attendance queries
            'attendance': {
                'patterns': [
                    r'attendance|present|absent|missing|attend',
                    r'how many (days|classes) (did i|have i) (miss|attend)',
                    r'my attendance|attendance rate|attendance percentage'
                ],
                'handler': self.handle_attendance_query
            },
            
            # Marks and grades queries
            'marks': {
                'patterns': [
                    r'marks|grade|score|exam|test|result',
                    r'how (did i do|am i doing) in',
                    r'my (performance|results|grades)'
                ],
                'handler': self.handle_marks_query
            },
            
            # Student information queries
            'student_info': {
                'patterns': [
                    r'my (profile|information|details)',
                    r'student (profile|info|details)',
                    r'contact|phone|email|address'
                ],
                'handler': self.handle_student_info_query
            },
            
            # Class/Subject information
            'subjects': {
                'patterns': [
                    r'subjects|classes|courses',
                    r'what (subjects|classes) (do i have|am i taking)',
                    r'my (subjects|classes|courses)'
                ],
                'handler': self.handle_subjects_query
            },
            
            # Teacher queries (for admins/teachers)
            'teachers': {
                'patterns': [
                    r'teachers|faculty|staff',
                    r'who (teaches|is teaching)',
                    r'teacher (for|of)'
                ],
                'handler': self.handle_teachers_query
            },
            
            # Statistics and reports (for teachers/admins)
            'statistics': {
                'patterns': [
                    r'statistics|stats|report|summary',
                    r'class (performance|attendance)',
                    r'how is (the class|my class) doing'
                ],
                'handler': self.handle_statistics_query
            },
            
            # General help
            'help': {
                'patterns': [
                    r'help|what can you do|commands',
                    r'how to|how do i',
                    r'what (questions|queries) can i ask'
                ],
                'handler': self.handle_help_query
            }
        }
        
    def process_query(self, user_query):
        """
        Process a natural language query and return an appropriate response.
        
        Args:
            user_query (str): The user's natural language query
            
        Returns:
            str: The chatbot's response
        """
        # Normalize the query
        query_lower = user_query.lower().strip()
        
        # Store in conversation history
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user_query': user_query,
            'query_type': None,
            'response': None
        })
        
        # Try to match query patterns
        query_type = self.identify_query_type(query_lower)
        
        if query_type:
            # Update conversation history
            self.conversation_history[-1]['query_type'] = query_type
            self.last_query_type = query_type
            
            # Get handler and process query
            handler = self.query_patterns[query_type]['handler']
            response = handler(query_lower, user_query)
        else:
            # Handle unknown queries
            response = self.handle_unknown_query(query_lower)
        
        # Store response in history
        self.conversation_history[-1]['response'] = response
        
        return response
    
    def identify_query_type(self, query):
        """
        Identify the type of query based on pattern matching.
        
        Args:
            query (str): Normalized user query
            
        Returns:
            str: Query type or None if not identified
        """
        for query_type, config in self.query_patterns.items():
            for pattern in config['patterns']:
                if re.search(pattern, query):
                    return query_type
        return None
    
    def handle_attendance_query(self, query, original_query):
        """Handle attendance-related queries."""
        try:
            if self.user_role == 'student':
                return self._get_student_attendance()
            elif self.user_role in ['teacher', 'admin']:
                # Check if asking about specific student or class
                if 'class' in query or 'all students' in query:
                    return self._get_class_attendance_summary()
                else:
                    return self._get_student_attendance()
            else:
                return "I'm sorry, I don't have access to attendance information for your role."
        except Exception as e:
            return f"I encountered an error while retrieving attendance information: {str(e)}"
    
    def _get_student_attendance(self):
        """Get attendance information for the current user (if student) or general info."""
        connection = self.db_config.get_connection()
        if not connection:
            return "I'm sorry, I couldn't connect to the database right now."
        
        try:
            cursor = connection.cursor()
            
            if self.user_role == 'student':
                # Get student's own attendance
                query = """
                SELECT 
                    s.subject_name,
                    COUNT(*) as total_classes,
                    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as attended_classes,
                    ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as attendance_percentage
                FROM attendance a
                JOIN subjects s ON a.subject_id = s.subject_id
                JOIN students st ON a.student_id = st.student_id
                WHERE st.user_id = %s
                GROUP BY s.subject_id, s.subject_name
                """
                cursor.execute(query, (self.user_id,))
                results = cursor.fetchall()
                
                if not results:
                    return "I couldn't find any attendance records for you yet."
                
                response = f"📊 **Your Attendance Summary:**\n\n"
                total_attended = 0
                total_classes = 0
                
                for subject, total, attended, percentage in results:
                    response += f"**{subject}:**\n"
                    response += f"  • Attended: {attended}/{total} classes\n"
                    response += f"  • Attendance Rate: {percentage}%\n\n"
                    total_attended += attended
                    total_classes += total
                
                if total_classes > 0:
                    overall_percentage = round((total_attended / total_classes) * 100, 2)
                    response += f"**Overall Attendance: {overall_percentage}%**\n"
                    
                    if overall_percentage >= 85:
                        response += "🎉 Excellent attendance! Keep it up!"
                    elif overall_percentage >= 75:
                        response += "👍 Good attendance, but try to attend more classes."
                    else:
                        response += "⚠️ Your attendance is low. Please attend more classes."
                
                return response
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
        finally:
            cursor.close()
            connection.close()
    
    def _get_class_attendance_summary(self):
        """Get class attendance summary for teachers/admins."""
        connection = self.db_config.get_connection()
        if not connection:
            return "I'm sorry, I couldn't connect to the database right now."
        
        try:
            cursor = connection.cursor()
            
            # Get overall class attendance statistics
            query = """
            SELECT 
                s.subject_name,
                s.class_name,
                COUNT(DISTINCT st.student_id) as total_students,
                COUNT(*) as total_attendance_records,
                SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as total_present,
                ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as class_attendance_rate
            FROM attendance a
            JOIN subjects s ON a.subject_id = s.subject_id
            JOIN students st ON a.student_id = st.student_id
            GROUP BY s.subject_id, s.subject_name, s.class_name
            ORDER BY s.class_name, s.subject_name
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            if not results:
                return "No attendance data found for any classes."
            
            response = "📈 **Class Attendance Summary:**\n\n"
            
            current_class = None
            for subject, class_name, total_students, total_records, total_present, attendance_rate in results:
                if current_class != class_name:
                    if current_class is not None:
                        response += "\n"
                    response += f"**{class_name}:**\n"
                    current_class = class_name
                
                response += f"  • {subject}: {attendance_rate}% attendance\n"
                response += f"    ({total_present}/{total_records} classes attended)\n"
            
            return response
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
        finally:
            cursor.close()
            connection.close()
    
    def handle_marks_query(self, query, original_query):
        """Handle marks and grades related queries."""
        try:
            if self.user_role == 'student':
                return self._get_student_marks()
            elif self.user_role in ['teacher', 'admin']:
                if 'class' in query or 'all students' in query:
                    return self._get_class_marks_summary()
                else:
                    return "Please specify if you want to see class performance or ask about a specific student."
            else:
                return "I don't have access to marks information for your role."
        except Exception as e:
            return f"I encountered an error while retrieving marks information: {str(e)}"
    
    def _get_student_marks(self):
        """Get marks information for the current student."""
        connection = self.db_config.get_connection()
        if not connection:
            return "I'm sorry, I couldn't connect to the database right now."
        
        try:
            cursor = connection.cursor()
            
            query = """
            SELECT 
                s.subject_name,
                m.exam_type,
                m.marks_obtained,
                m.total_marks,
                m.grade,
                m.exam_date
            FROM marks m
            JOIN subjects s ON m.subject_id = s.subject_id
            JOIN students st ON m.student_id = st.student_id
            WHERE st.user_id = %s
            ORDER BY m.exam_date DESC, s.subject_name
            """
            cursor.execute(query, (self.user_id,))
            results = cursor.fetchall()
            
            if not results:
                return "I couldn't find any marks records for you yet."
            
            response = "📝 **Your Academic Performance:**\n\n"
            
            # Group by subject
            subjects = {}
            for subject, exam_type, marks_obtained, total_marks, grade, exam_date in results:
                if subject not in subjects:
                    subjects[subject] = []
                subjects[subject].append({
                    'exam_type': exam_type,
                    'marks': marks_obtained,
                    'total': total_marks,
                    'grade': grade,
                    'date': exam_date
                })
            
            for subject, exams in subjects.items():
                response += f"**{subject}:**\n"
                for exam in exams:
                    percentage = round((exam['marks'] / exam['total']) * 100, 2) if exam['total'] > 0 else 0
                    response += f"  • {exam['exam_type']}: {exam['marks']}/{exam['total']} ({percentage}%) - Grade: {exam['grade']}\n"
                
                # Calculate average for subject
                if exams:
                    total_marks = sum(exam['marks'] for exam in exams)
                    total_possible = sum(exam['total'] for exam in exams)
                    avg_percentage = round((total_marks / total_possible) * 100, 2) if total_possible > 0 else 0
                    response += f"  **Subject Average: {avg_percentage}%**\n\n"
            
            return response
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
        finally:
            cursor.close()
            connection.close()
    
    def _get_class_marks_summary(self):
        """Get class marks summary for teachers/admins."""
        connection = self.db_config.get_connection()
        if not connection:
            return "I'm sorry, I couldn't connect to the database right now."
        
        try:
            cursor = connection.cursor()
            
            query = """
            SELECT 
                s.subject_name,
                s.class_name,
                m.exam_type,
                COUNT(*) as total_students,
                AVG(m.marks_obtained) as avg_marks,
                MAX(m.marks_obtained) as max_marks,
                MIN(m.marks_obtained) as min_marks,
                m.total_marks
            FROM marks m
            JOIN subjects s ON m.subject_id = s.subject_id
            GROUP BY s.subject_id, s.subject_name, s.class_name, m.exam_type, m.total_marks
            ORDER BY s.class_name, s.subject_name, m.exam_type
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            if not results:
                return "No marks data found for any classes."
            
            response = "📊 **Class Performance Summary:**\n\n"
            
            current_class = None
            for subject, class_name, exam_type, total_students, avg_marks, max_marks, min_marks, total_marks in results:
                if current_class != class_name:
                    if current_class is not None:
                        response += "\n"
                    response += f"**{class_name}:**\n"
                    current_class = class_name
                
                avg_percentage = round((avg_marks / total_marks) * 100, 2) if total_marks > 0 else 0
                response += f"  • {subject} - {exam_type}:\n"
                response += f"    Average: {avg_marks:.1f}/{total_marks} ({avg_percentage}%)\n"
                response += f"    Range: {min_marks}-{max_marks} marks\n"
                response += f"    Students: {total_students}\n"
            
            return response
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
        finally:
            cursor.close()
            connection.close()
    
    def handle_student_info_query(self, query, original_query):
        """Handle student profile information queries."""
        if self.user_role != 'student':
            return "Student profile information is only available to students."
        
        connection = self.db_config.get_connection()
        if not connection:
            return "I'm sorry, I couldn't connect to the database right now."
        
        try:
            cursor = connection.cursor()
            
            query = """
            SELECT 
                st.roll_number,
                st.full_name,
                st.class_name,
                st.phone,
                st.email,
                st.address,
                st.enrollment_date,
                st.gender,
                st.date_of_birth,
                st.guardian_name,
                st.guardian_phone
            FROM students st
            JOIN users u ON st.user_id = u.user_id
            WHERE u.user_id = %s
            """
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()
            
            if not result:
                return "I couldn't find your profile information."
            
            (roll_number, full_name, class_name, phone, email, address, 
             enrollment_date, gender, date_of_birth, guardian_name, guardian_phone) = result
            
            response = f"👤 **Your Profile Information:**\n\n"
            response += f"**Personal Details:**\n"
            response += f"  • Name: {full_name}\n"
            response += f"  • Roll Number: {roll_number}\n"
            response += f"  • Class: {class_name}\n"
            response += f"  • Gender: {gender or 'Not specified'}\n"
            response += f"  • Date of Birth: {date_of_birth or 'Not specified'}\n\n"
            
            response += f"**Contact Information:**\n"
            response += f"  • Phone: {phone or 'Not provided'}\n"
            response += f"  • Email: {email or 'Not provided'}\n"
            response += f"  • Address: {address or 'Not provided'}\n\n"
            
            if guardian_name or guardian_phone:
                response += f"**Guardian Information:**\n"
                response += f"  • Guardian Name: {guardian_name or 'Not provided'}\n"
                response += f"  • Guardian Phone: {guardian_phone or 'Not provided'}\n\n"
            
            response += f"**Academic Information:**\n"
            response += f"  • Enrollment Date: {enrollment_date}\n"
            
            return response
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
        finally:
            cursor.close()
            connection.close()
    
    def handle_subjects_query(self, query, original_query):
        """Handle subjects/classes information queries."""
        connection = self.db_config.get_connection()
        if not connection:
            return "I'm sorry, I couldn't connect to the database right now."
        
        try:
            cursor = connection.cursor()
            
            if self.user_role == 'student':
                # Get subjects for the student's class
                query = """
                SELECT DISTINCT 
                    s.subject_name,
                    s.subject_code,
                    u.full_name as teacher_name
                FROM subjects s
                LEFT JOIN users u ON s.teacher_id = u.user_id
                JOIN students st ON s.class_name = st.class_name
                WHERE st.user_id = %s
                ORDER BY s.subject_name
                """
                cursor.execute(query, (self.user_id,))
                results = cursor.fetchall()
                
                if not results:
                    return "I couldn't find any subjects for your class."
                
                response = "📚 **Your Subjects:**\n\n"
                for subject_name, subject_code, teacher_name in results:
                    response += f"• **{subject_name}** ({subject_code})\n"
                    if teacher_name:
                        response += f"  Teacher: {teacher_name}\n"
                    response += "\n"
                
            elif self.user_role in ['teacher', 'admin']:
                # Get all subjects or subjects taught by teacher
                if self.user_role == 'teacher':
                    query = """
                    SELECT 
                        s.subject_name,
                        s.subject_code,
                        s.class_name,
                        COUNT(DISTINCT st.student_id) as student_count
                    FROM subjects s
                    LEFT JOIN students st ON s.class_name = st.class_name
                    WHERE s.teacher_id = %s
                    GROUP BY s.subject_id, s.subject_name, s.subject_code, s.class_name
                    ORDER BY s.class_name, s.subject_name
                    """
                    cursor.execute(query, (self.user_id,))
                    response = "📚 **Subjects You Teach:**\n\n"
                else:  # admin
                    query = """
                    SELECT 
                        s.subject_name,
                        s.subject_code,
                        s.class_name,
                        u.full_name as teacher_name,
                        COUNT(DISTINCT st.student_id) as student_count
                    FROM subjects s
                    LEFT JOIN users u ON s.teacher_id = u.user_id
                    LEFT JOIN students st ON s.class_name = st.class_name
                    GROUP BY s.subject_id, s.subject_name, s.subject_code, s.class_name, u.full_name
                    ORDER BY s.class_name, s.subject_name
                    """
                    cursor.execute(query)
                    response = "📚 **All Subjects:**\n\n"
                
                results = cursor.fetchall()
                
                if not results:
                    return "No subjects found."
                
                current_class = None
                for row in results:
                    if self.user_role == 'admin':
                        subject_name, subject_code, class_name, teacher_name, student_count = row
                    else:
                        subject_name, subject_code, class_name, student_count = row
                        teacher_name = None
                    
                    if current_class != class_name:
                        if current_class is not None:
                            response += "\n"
                        response += f"**{class_name}:**\n"
                        current_class = class_name
                    
                    response += f"  • {subject_name} ({subject_code})\n"
                    if teacher_name and self.user_role == 'admin':
                        response += f"    Teacher: {teacher_name}\n"
                    response += f"    Students: {student_count}\n"
            
            return response
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
        finally:
            cursor.close()
            connection.close()
    
    def handle_teachers_query(self, query, original_query):
        """Handle teacher information queries."""
        if self.user_role not in ['teacher', 'admin']:
            return "Teacher information is only available to teachers and administrators."
        
        connection = self.db_config.get_connection()
        if not connection:
            return "I'm sorry, I couldn't connect to the database right now."
        
        try:
            cursor = connection.cursor()
            
            query = """
            SELECT 
                t.employee_id,
                t.full_name,
                t.department,
                t.qualification,
                t.experience_years,
                t.email,
                t.phone,
                COUNT(DISTINCT s.subject_id) as subjects_count
            FROM teachers t
            LEFT JOIN users u ON u.full_name = t.full_name AND u.role = 'teacher'
            LEFT JOIN subjects s ON s.teacher_id = u.user_id
            GROUP BY t.teacher_id, t.employee_id, t.full_name, t.department, t.qualification, t.experience_years, t.email, t.phone
            ORDER BY t.full_name
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            if not results:
                return "No teacher information found."
            
            response = "👨‍🏫 **Teaching Staff:**\n\n"
            
            for emp_id, name, department, qualification, experience, email, phone, subject_count in results:
                response += f"**{name}** ({emp_id})\n"
                response += f"  • Department: {department or 'Not specified'}\n"
                response += f"  • Qualification: {qualification or 'Not specified'}\n"
                response += f"  • Experience: {experience or 0} years\n"
                response += f"  • Subjects Teaching: {subject_count}\n"
                if self.user_role == 'admin':
                    response += f"  • Email: {email or 'Not provided'}\n"
                    response += f"  • Phone: {phone or 'Not provided'}\n"
                response += "\n"
            
            return response
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
        finally:
            cursor.close()
            connection.close()
    
    def handle_statistics_query(self, query, original_query):
        """Handle statistics and reports queries."""
        if self.user_role not in ['teacher', 'admin']:
            return "Statistics are only available to teachers and administrators."
        
        connection = self.db_config.get_connection()
        if not connection:
            return "I'm sorry, I couldn't connect to the database right now."
        
        try:
            cursor = connection.cursor()
            
            # Get overall statistics
            stats = {}
            
            # Total students
            cursor.execute("SELECT COUNT(*) FROM students")
            stats['total_students'] = cursor.fetchone()[0]
            
            # Total teachers
            cursor.execute("SELECT COUNT(*) FROM teachers")
            stats['total_teachers'] = cursor.fetchone()[0]
            
            # Total subjects
            cursor.execute("SELECT COUNT(*) FROM subjects")
            stats['total_subjects'] = cursor.fetchone()[0]
            
            # Average attendance rate
            cursor.execute("""
                SELECT AVG(
                    CASE WHEN total_classes > 0 
                    THEN (present_classes * 100.0 / total_classes) 
                    ELSE 0 END
                ) as avg_attendance
                FROM (
                    SELECT 
                        student_id,
                        COUNT(*) as total_classes,
                        SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_classes
                    FROM attendance
                    GROUP BY student_id
                ) as student_attendance
            """)
            result = cursor.fetchone()
            stats['avg_attendance'] = round(result[0], 2) if result[0] else 0
            
            # Recent attendance (last 7 days)
            cursor.execute("""
                SELECT attendance_date, 
                       COUNT(*) as total_records,
                       SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_count
                FROM attendance 
                WHERE attendance_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                GROUP BY attendance_date
                ORDER BY attendance_date DESC
                LIMIT 7
            """)
            recent_attendance = cursor.fetchall()
            
            response = "📊 **System Statistics:**\n\n"
            response += f"**Overview:**\n"
            response += f"  • Total Students: {stats['total_students']}\n"
            response += f"  • Total Teachers: {stats['total_teachers']}\n"
            response += f"  • Total Subjects: {stats['total_subjects']}\n"
            response += f"  • Average Attendance Rate: {stats['avg_attendance']}%\n\n"
            
            if recent_attendance:
                response += "**Recent Attendance (Last 7 Days):**\n"
                for date, total, present in recent_attendance:
                    percentage = round((present / total) * 100, 2) if total > 0 else 0
                    response += f"  • {date}: {present}/{total} ({percentage}%)\n"
            
            return response
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
        finally:
            cursor.close()
            connection.close()
    
    def handle_help_query(self, query, original_query):
        """Handle help and usage queries."""
        response = "🤖 **ClassTrack AI Assistant Help**\n\n"
        response += "I can help you with the following types of queries:\n\n"
        
        if self.user_role == 'student':
            response += "**📊 Attendance Queries:**\n"
            response += "  • 'What's my attendance?'\n"
            response += "  • 'How many classes did I miss?'\n"
            response += "  • 'My attendance percentage'\n\n"
            
            response += "**📝 Marks & Grades:**\n"
            response += "  • 'What are my marks?'\n"
            response += "  • 'How did I do in exams?'\n"
            response += "  • 'My performance in [subject]'\n\n"
            
            response += "**👤 Profile Information:**\n"
            response += "  • 'My profile information'\n"
            response += "  • 'My contact details'\n\n"
            
            response += "**📚 Subjects:**\n"
            response += "  • 'What subjects do I have?'\n"
            response += "  • 'My classes and teachers'\n\n"
            
        elif self.user_role in ['teacher', 'admin']:
            response += "**📊 Class Statistics:**\n"
            response += "  • 'Class attendance summary'\n"
            response += "  • 'How is my class doing?'\n"
            response += "  • 'Class performance report'\n\n"
            
            response += "**📝 Academic Reports:**\n"
            response += "  • 'Class marks summary'\n"
            response += "  • 'Student performance statistics'\n\n"
            
            response += "**👨‍🏫 Staff Information:**\n"
            response += "  • 'List of teachers'\n"
            response += "  • 'Teaching staff details'\n\n"
            
            response += "**📚 Subject Management:**\n"
            response += "  • 'What subjects do I teach?' (Teachers)\n"
            response += "  • 'All subjects and teachers' (Admins)\n\n"
        
        response += "**💡 Tips:**\n"
        response += "  • Ask questions in natural language\n"
        response += "  • Be specific about what information you need\n"
        response += "  • I understand various ways of asking the same question\n\n"
        
        response += "Just type your question naturally, and I'll do my best to help! 😊"
        
        return response
    
    def handle_unknown_query(self, query):
        """Handle queries that don't match any pattern."""
        suggestions = []
        
        # Provide role-specific suggestions
        if self.user_role == 'student':
            suggestions = [
                "Try asking about your attendance: 'What's my attendance?'",
                "Ask about your marks: 'How did I do in my exams?'",
                "Get your profile info: 'Show my profile information'",
                "See your subjects: 'What subjects do I have?'"
            ]
        elif self.user_role in ['teacher', 'admin']:
            suggestions = [
                "Ask about class performance: 'How is my class doing?'",
                "Get attendance statistics: 'Class attendance summary'",
                "View teaching staff: 'List of teachers'",
                "See system statistics: 'Show me system statistics'"
            ]
        
        response = "🤔 I'm not sure what you're asking about. Here are some things you can try:\n\n"
        for suggestion in suggestions:
            response += f"  • {suggestion}\n"
        
        response += "\nType 'help' to see all available commands, or try rephrasing your question."
        
        return response


class ChatbotGUI:
    """
    GUI interface for the ClassTrack Chatbot.
    Integrates with the main dashboard and provides a chat window interface.
    """
    
    def __init__(self, parent, user_id, user_role, user_name):
        self.parent = parent
        self.user_id = user_id
        self.user_role = user_role
        self.user_name = user_name
        self.is_active = True  # Track if GUI is still active
        
        # Initialize chatbot
        self.chatbot = ClassTrackChatbot(user_id, user_role, user_name)
        
        # Create GUI elements
        self.create_chatbot_interface()
        
    def create_chatbot_interface(self):
        """Create the chatbot GUI interface."""
        # Main container frame
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            self.main_frame,
            text="🤖 ClassTrack AI Assistant",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle with user info
        subtitle_label = ttk.Label(
            self.main_frame,
            text=f"Welcome, {self.user_name} ({self.user_role.title()})",
            font=("Arial", 10)
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Chat display area
        self.chat_frame = ttk.Frame(self.main_frame)
        self.chat_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Chat history text widget with scrollbar
        self.chat_text = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Arial", 10),
            state='disabled'
        )
        self.chat_text.pack(fill='both', expand=True)
        
        # Configure text tags for formatting
        self.chat_text.tag_configure("user", foreground="#2E86AB", font=("Arial", 10, "bold"))
        self.chat_text.tag_configure("bot", foreground="#A23B72", font=("Arial", 10))
        self.chat_text.tag_configure("timestamp", foreground="#666666", font=("Arial", 8))
        
        # Input frame
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Query input
        self.query_var = tk.StringVar()
        self.query_entry = ttk.Entry(
            input_frame,
            textvariable=self.query_var,
            font=("Arial", 11),
            width=60
        )
        self.query_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.query_entry.bind('<Return>', self.on_send_query)
        
        # Send button
        self.send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.on_send_query
        )
        self.send_button.pack(side='right')
        
        # Quick action buttons frame
        quick_actions_frame = ttk.LabelFrame(self.main_frame, text="Quick Actions")
        quick_actions_frame.pack(fill='x', pady=(0, 10))
        
        # Create quick action buttons based on user role
        self.create_quick_action_buttons(quick_actions_frame)
        
        # Status frame
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill='x')
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready to help! Type your question or click a quick action button.",
            font=("Arial", 9),
            foreground="#666666"
        )
        self.status_label.pack(side='left')
        
        # Clear chat button
        clear_button = ttk.Button(
            status_frame,
            text="Clear Chat",
            command=self.clear_chat
        )
        clear_button.pack(side='right')
        
        # Add welcome message
        self.add_welcome_message()
        
        # Focus on input
        self.query_entry.focus()
    
    def create_quick_action_buttons(self, parent):
        """Create quick action buttons based on user role."""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill='x', padx=5, pady=5)
        
        if self.user_role == 'student':
            quick_actions = [
                ("📊 My Attendance", "What's my attendance?"),
                ("📝 My Marks", "Show my marks"),
                ("👤 My Profile", "Show my profile information"),
                ("📚 My Subjects", "What subjects do I have?"),
                ("❓ Help", "help")
            ]
        elif self.user_role in ['teacher', 'admin']:
            quick_actions = [
                ("📊 Class Stats", "Show class statistics"),
                ("📈 Attendance Report", "Class attendance summary"),
                ("📝 Performance Report", "Class performance summary"),
                ("👨‍🏫 Teachers", "List of teachers"),
                ("❓ Help", "help")
            ]
        else:
            quick_actions = [("❓ Help", "help")]
        
        for i, (text, query) in enumerate(quick_actions):
            btn = ttk.Button(
                buttons_frame,
                text=text,
                command=lambda q=query: self.send_quick_query(q)
            )
            btn.grid(row=i//3, column=i%3, padx=2, pady=2, sticky='ew')
        
        # Configure column weights for even distribution
        for i in range(3):
            buttons_frame.columnconfigure(i, weight=1)
    
    def add_welcome_message(self):
        """Add a welcome message to the chat."""
        welcome_msg = f"Hello {self.user_name}! 👋\n\n"
        welcome_msg += "I'm your ClassTrack AI Assistant. I can help you with:\n"
        
        if self.user_role == 'student':
            welcome_msg += "• Checking your attendance and marks\n"
            welcome_msg += "• Viewing your profile information\n"
            welcome_msg += "• Getting information about your subjects\n"
        elif self.user_role in ['teacher', 'admin']:
            welcome_msg += "• Class attendance and performance statistics\n"
            welcome_msg += "• Student and teacher information\n"
            welcome_msg += "• Academic reports and summaries\n"
        
        welcome_msg += "\nJust ask me a question in natural language, or use the quick action buttons below!"
        
        self.add_message_to_chat("Assistant", welcome_msg, is_bot=True)
    
    def on_send_query(self, event=None):
        """Handle sending a query to the chatbot."""
        query = self.query_var.get().strip()
        if not query:
            return
        
        # Clear input
        self.query_var.set("")
        
        # Add user message to chat
        self.add_message_to_chat("You", query, is_bot=False)
        
        # Update status
        self.status_label.config(text="Processing your query...")
        self.parent.update()
        
        # Process query directly for better stability
        try:
            response = self.chatbot.process_query(query)
            self.handle_query_response(response)
        except Exception as e:
            error_msg = f"I encountered an error while processing your query: {str(e)}"
            self.handle_query_response(error_msg)
    
    def send_quick_query(self, query):
        """Send a predefined quick query."""
        self.query_var.set(query)
        self.on_send_query()
    
    def process_query_threaded(self, query):
        """Process query in a separate thread."""
        if not self.is_active:
            return
            
        try:
            response = self.chatbot.process_query(query)
            
            # Update GUI in main thread - check if window still exists
            if self.is_active:
                try:
                    self.parent.after(0, lambda: self.handle_query_response(response))
                except (tk.TclError, RuntimeError):
                    # Window was closed or main thread not in loop
                    self.is_active = False
            
        except Exception as e:
            error_msg = f"I encountered an error while processing your query: {str(e)}"
            if self.is_active:
                try:
                    self.parent.after(0, lambda: self.handle_query_response(error_msg))
                except (tk.TclError, RuntimeError):
                    # Window was closed or main thread not in loop
                    self.is_active = False
    
    def handle_query_response(self, response):
        """Handle the chatbot response in the main thread."""
        # Add bot response to chat
        self.add_message_to_chat("Assistant", response, is_bot=True)
        
        # Update status
        self.status_label.config(text="Ready to help! Type your next question.")
        
        # Focus back on input
        self.query_entry.focus()
    
    def add_message_to_chat(self, sender, message, is_bot=False):
        """Add a message to the chat display."""
        self.chat_text.config(state='normal')
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")
        
        # Add sender and timestamp
        if is_bot:
            self.chat_text.insert(tk.END, f"🤖 {sender} ({timestamp})\n", "bot")
        else:
            self.chat_text.insert(tk.END, f"👤 {sender} ({timestamp})\n", "user")
        
        # Add message content
        self.chat_text.insert(tk.END, f"{message}\n\n")
        
        # Scroll to bottom
        self.chat_text.config(state='disabled')
        self.chat_text.see(tk.END)
    
    def clear_chat(self):
        """Clear the chat history."""
        result = messagebox.askyesno(
            "Clear Chat",
            "Are you sure you want to clear the chat history?"
        )
        
        if result:
            self.chat_text.config(state='normal')
            self.chat_text.delete(1.0, tk.END)
            self.chat_text.config(state='disabled')
            
            # Clear chatbot conversation history
            self.chatbot.conversation_history = []
            
            # Add welcome message again
            self.add_welcome_message()
    
    def cleanup(self):
        """Clean up resources when GUI is being destroyed."""
        self.is_active = False


class ChatbotWindow:
    """
    Standalone chatbot window that can be opened from the main dashboard.
    """
    
    def __init__(self, user_id, user_role, user_name):
        self.user_id = user_id
        self.user_role = user_role
        self.user_name = user_name
        
        # Create window
        self.window = tk.Toplevel()
        self.window.title("ClassTrack AI Assistant")
        self.window.geometry("900x700")
        self.window.configure(bg='#f0f0f0')
        
        # Make window modal
        self.window.transient()
        self.window.grab_set()
        
        # Center window
        self.center_window()
        
        # Create chatbot GUI
        self.chatbot_gui = ChatbotGUI(self.window, user_id, user_role, user_name)
        
        # Handle window closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center the window on screen."""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"900x700+{x}+{y}")
    
    def on_closing(self):
        """Handle window closing."""
        # Cleanup the chatbot GUI
        if hasattr(self, 'chatbot_gui'):
            self.chatbot_gui.cleanup()
        
        self.window.grab_release()
        self.window.destroy()


# Example usage and integration
def show_chatbot_window(user_id, user_role, user_name):
    """
    Function to show the chatbot window from the main dashboard.
    This function should be called from your main application.
    
    Args:
        user_id (int): Current user's ID
        user_role (str): Current user's role (student/teacher/admin)
        user_name (str): Current user's full name
    """
    chatbot_window = ChatbotWindow(user_id, user_role, user_name)
    return chatbot_window


# Test function for standalone testing
def test_chatbot():
    """Test function to run the chatbot independently."""
    print("Testing ClassTrack Chatbot...")
    
    # Create test window
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    # Test with different user roles
    test_cases = [
        (1, 'student', 'John Doe'),
        (2, 'teacher', 'Jane Smith'), 
        (3, 'admin', 'Admin User')
    ]
    
    for user_id, role, name in test_cases:
        print(f"Testing chatbot for {name} ({role})...")
        
        # Create chatbot instance
        chatbot = ClassTrackChatbot(user_id, role, name)
        
        # Test queries
        test_queries = [
            "What's my attendance?",
            "Show my marks",
            "Help",
            "What subjects do I have?"
        ]
        
        for query in test_queries:
            print(f"Query: {query}")
            response = chatbot.process_query(query)
            print(f"Response: {response[:100]}...")
            print("-" * 50)
        
        break  # Test only first user for demo
    
    root.destroy()


if __name__ == "__main__":
    # Run standalone test
    test_chatbot()
