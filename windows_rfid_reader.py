"""
Windows RFID Integration for Class Track System
This replaces the demo RFID functionality with real USB HID reader support
"""

import threading
import time
import queue
from datetime import datetime
from pynput import keyboard
from database_config import DatabaseConfig

class WindowsRFIDReader:
    def __init__(self, attendance_callback=None):
        self.attendance_callback = attendance_callback
        self.db_config = DatabaseConfig()
        
        # RFID reading state
        self.current_input = ""
        self.rfid_queue = queue.Queue()
        self.is_reading = False
        self.current_subject_id = None
        
        # Keyboard listener
        self.listener = None
        self.process_thread = None
        
        print("Windows RFID Reader initialized")
        
    def start_reading(self, subject_id=None):
        """Start reading RFID cards"""
        if self.is_reading:
            print("RFID reader already running")
            return
            
        self.current_subject_id = subject_id
        self.is_reading = True
        
        # Start keyboard listener for HID RFID reader
        self.listener = keyboard.Listener(
            on_press=self._on_key_press,
            suppress=False  # Don't suppress keys (allow normal typing)
        )
        self.listener.start()
        
        # Start processing thread
        self.process_thread = threading.Thread(target=self._process_rfid_input, daemon=True)
        self.process_thread.start()
        
        print(f"✓ RFID Reader started for subject ID: {subject_id}")
        print("Scan RFID cards now...")
        
    def stop_reading(self):
        """Stop reading RFID cards"""
        self.is_reading = False
        
        if self.listener:
            self.listener.stop()
            self.listener = None
            
        print("✓ RFID Reader stopped")
        
    def _on_key_press(self, key):
        """Handle keyboard input from HID RFID reader"""
        try:
            if key == keyboard.Key.enter:
                # RFID card scan complete
                if self.current_input and len(self.current_input) >= 6:  # Valid RFID length
                    self.rfid_queue.put(self.current_input.strip())
                self.current_input = ""
                
            elif hasattr(key, 'char') and key.char and key.char.isalnum():
                # Only capture alphanumeric characters (RFID data)
                self.current_input += key.char
                
                # Prevent very long inputs (security)
                if len(self.current_input) > 20:
                    self.current_input = ""
                    
        except AttributeError:
            pass  # Special keys
            
    def _process_rfid_input(self):
        """Process RFID scans from queue"""
        while self.is_reading:
            try:
                rfid_id = self.rfid_queue.get(timeout=1)
                self._handle_rfid_scan(rfid_id)
            except queue.Empty:
                continue
                
    def _handle_rfid_scan(self, rfid_id):
        """Handle a scanned RFID card"""
        print(f"\n🔍 RFID Scanned: {rfid_id}")
        
        # Get student info from database
        student_info = self._get_student_by_rfid(rfid_id)
        
        if not student_info:
            print(f"❌ Unknown RFID card: {rfid_id}")
            self._log_rfid_event(rfid_id, "Unknown", "Unknown", "Unknown RFID")
            return
            
        student_id, roll_number, full_name, class_name = student_info
        print(f"👤 Student: {full_name} ({roll_number})")
        
        # Mark attendance if subject is selected
        if self.current_subject_id:
            success = self._mark_attendance(student_id, self.current_subject_id)
            status = "Present ✓" if success else "Already marked ⚠️"
        else:
            status = "Scanned (No subject selected)"
            
        print(f"📝 Status: {status}")
        self._log_rfid_event(rfid_id, full_name, roll_number, status)
        
        # Call callback if provided
        if self.attendance_callback:
            self.attendance_callback(rfid_id, student_info, status)
            
    def _get_student_by_rfid(self, rfid_id):
        """Get student information by RFID card"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # First check if RFID column exists, if not create it
                try:
                    cursor.execute("ALTER TABLE students ADD COLUMN rfid_card_id VARCHAR(50) UNIQUE")
                    connection.commit()
                except:
                    pass  # Column already exists
                
                # Try to find student by RFID
                query = """
                SELECT student_id, roll_number, full_name, class_name 
                FROM students 
                WHERE rfid_card_id = %s
                """
                cursor.execute(query, (rfid_id,))
                result = cursor.fetchone()
                
                if result:
                    return result
                    
                # If not found, try to find by roll number pattern
                # (Some RFID cards might have roll numbers programmed)
                query = """
                SELECT student_id, roll_number, full_name, class_name 
                FROM students 
                WHERE LOWER(roll_number) = %s
                """
                cursor.execute(query, (rfid_id.lower(),))
                return cursor.fetchone()
                
            except Exception as e:
                print(f"Database error: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        return None
        
    def _mark_attendance(self, student_id, subject_id):
        """Mark attendance for student"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                current_date = datetime.now().date()
                current_time = datetime.now().time()
                
                # Check if already marked today
                check_query = """
                SELECT COUNT(*) FROM attendance 
                WHERE student_id = %s AND subject_id = %s AND attendance_date = %s
                """
                cursor.execute(check_query, (student_id, subject_id, current_date))
                
                if cursor.fetchone()[0] > 0:
                    return False  # Already marked
                
                # Mark attendance
                insert_query = """
                INSERT INTO attendance (student_id, subject_id, attendance_date, status, marked_by)
                VALUES (%s, %s, %s, 'present', 1)
                """
                cursor.execute(insert_query, (student_id, subject_id, current_date))
                connection.commit()
                
                return True
                
            except Exception as e:
                print(f"Failed to mark attendance: {e}")
                return False
            finally:
                cursor.close()
                connection.close()
        return False
        
    def _log_rfid_event(self, rfid_id, student_name, roll_number, status):
        """Log RFID events to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] RFID: {rfid_id} | Student: {student_name} ({roll_number}) | Status: {status}"
        
        try:
            with open("rfid_logs.txt", "a", encoding='utf-8') as log_file:
                log_file.write(log_entry + "\n")
        except Exception as e:
            print(f"Failed to write log: {e}")
            
    def register_student_rfid(self, student_id, rfid_id):
        """Register RFID card to student (for admin setup)"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Update student with RFID
                update_query = "UPDATE students SET rfid_card_id = %s WHERE student_id = %s"
                cursor.execute(update_query, (rfid_id, student_id))
                connection.commit()
                
                print(f"✓ RFID {rfid_id} registered to student ID {student_id}")
                return True
                
            except Exception as e:
                print(f"Failed to register RFID: {e}")
                return False
            finally:
                cursor.close()
                connection.close()
        return False

# Test function
def test_rfid_reader():
    """Test the RFID reader"""
    print("🧪 Testing RFID Reader...")
    print("1. Plug in your USB RFID reader")
    print("2. Make sure it works in Notepad first")
    print("3. Press Ctrl+C to stop testing")
    
    def on_scan(rfid_id, student_info, status):
        print(f"📱 Callback: {student_info[2] if student_info else 'Unknown'} - {status}")
    
    reader = WindowsRFIDReader(attendance_callback=on_scan)
    reader.start_reading(subject_id=1)  # Test with subject 1
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        reader.stop_reading()
        print("\n✓ Test completed")

if __name__ == "__main__":
    test_rfid_reader()
