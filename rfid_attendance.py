# rfid_attendance.py - RFID-based attendance system for future implementation
"""
RFID Attendance System
This module provides the foundation for RFID-based attendance tracking.
It includes demo functionality and placeholders for hardware integration.

Hardware Requirements (for future implementation):
- RFID Reader (e.g., RC522 module)
- RFID Cards/Tags for students
- Raspberry Pi or Arduino (optional for standalone operation)
- USB RFID Reader for PC integration

Software Requirements:
- pyscard (for smart card readers)
- pyserial (for serial communication)
- RPi.GPIO (for Raspberry Pi GPIO control)
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
from datetime import datetime, timedelta
from database_config import DatabaseConfig

class RFIDAttendanceSystem:
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.is_scanning = False
        self.rfid_reader_connected = False
        self.auto_attendance_mode = True
        self.time_window_minutes = 15
        self.current_subject_id = None
        
        # Student RFID mapping (this would be stored in database in real implementation)
        self.student_rfid_mapping = {
            "RFID001": {"student_id": 1, "name": "John Doe", "roll": "BCS001"},
            "RFID002": {"student_id": 2, "name": "Jane Smith", "roll": "BCS002"},
            "RFID003": {"student_id": 3, "name": "Bob Wilson", "roll": "BCS003"},
        }
    
    def initialize_rfid_reader(self):
        """Initialize RFID reader hardware"""
        try:
            # For Windows USB HID RFID Reader
            try:
                from pynput import keyboard
                self.use_hid_reader = True
                self.current_input = ""
                self.rfid_reader_connected = True
                print("✓ USB HID RFID Reader initialized successfully")
                return True
            except ImportError:
                print("⚠️ pynput not installed. Install with: pip install pynput")
                print("Falling back to demo mode...")
                
            # Fallback to demo mode
            self.use_hid_reader = False
            self.rfid_reader_connected = True
            print("RFID Reader initialized successfully (Demo Mode)")
            return True
            
        except Exception as e:
            print(f"Failed to initialize RFID reader: {str(e)}")
            return False
    
    def start_rfid_scanning(self, subject_id=None):
        """Start RFID scanning for attendance"""
        if not self.rfid_reader_connected:
            if not self.initialize_rfid_reader():
                return False
        
        self.current_subject_id = subject_id
        self.is_scanning = True
        
        # Start scanning in a separate thread
        scan_thread = threading.Thread(target=self._scan_rfid_cards, daemon=True)
        scan_thread.start()
        
        print("RFID scanning started...")
        return True
    
    def stop_rfid_scanning(self):
        """Stop RFID scanning"""
        self.is_scanning = False
        print("RFID scanning stopped.")
    
    def _scan_rfid_cards(self):
        """Main RFID scanning loop (hardware integration point)"""
        while self.is_scanning:
            try:
                if hasattr(self, 'use_hid_reader') and self.use_hid_reader:
                    # Real USB HID RFID Reader
                    self._scan_hid_rfid()
                else:
                    # Demo simulation
                    self._simulate_rfid_scan()
                
                time.sleep(2)  # Scan interval
                
            except Exception as e:
                print(f"RFID scanning error: {str(e)}")
                time.sleep(5)  # Wait before retrying
    
    def _simulate_rfid_scan(self):
        """Simulate RFID card scanning for demo purposes"""
        # Randomly simulate an RFID scan
        if random.random() < 0.1:  # 10% chance each iteration
            rfid_ids = list(self.student_rfid_mapping.keys())
            scanned_rfid = random.choice(rfid_ids)
            self.process_rfid_scan(scanned_rfid)
    
    def _scan_hid_rfid(self):
        """Scan for USB HID RFID reader input"""
        try:
            from pynput import keyboard
            import queue
            
            # Set up keyboard listener if not already done
            if not hasattr(self, 'rfid_queue'):
                self.rfid_queue = queue.Queue()
                self.current_rfid_input = ""
                
                def on_key_press(key):
                    try:
                        if key == keyboard.Key.enter:
                            if self.current_rfid_input and len(self.current_rfid_input) >= 6:
                                self.rfid_queue.put(self.current_rfid_input.strip())
                            self.current_rfid_input = ""
                        elif hasattr(key, 'char') and key.char and key.char.isalnum():
                            self.current_rfid_input += key.char
                            if len(self.current_rfid_input) > 20:  # Security limit
                                self.current_rfid_input = ""
                    except AttributeError:
                        pass
                
                # Start listener (non-blocking)
                if not hasattr(self, 'keyboard_listener'):
                    self.keyboard_listener = keyboard.Listener(on_press=on_key_press, suppress=False)
                    self.keyboard_listener.start()
            
            # Check for scanned RFID
            try:
                rfid_id = self.rfid_queue.get_nowait()
                self.process_rfid_scan(rfid_id)
            except queue.Empty:
                pass
                
        except ImportError:
            # Fall back to demo if pynput not available
            self._simulate_rfid_scan()
    
    def process_rfid_scan(self, rfid_id):
        """Process scanned RFID card and mark attendance"""
        print(f"RFID Scanned: {rfid_id}")
        
        # Check if RFID is registered
        if rfid_id not in self.student_rfid_mapping:
            print(f"Unknown RFID: {rfid_id}")
            self.log_rfid_event(rfid_id, "Unknown", "Unknown", "Unknown RFID")
            return
        
        student_info = self.student_rfid_mapping[rfid_id]
        student_id = student_info["student_id"]
        student_name = student_info["name"]
        roll_number = student_info["roll"]
        
        # Check if auto attendance is enabled
        if self.auto_attendance_mode and self.current_subject_id:
            success = self.mark_rfid_attendance(student_id, self.current_subject_id)
            status = "Present" if success else "Already Marked"
        else:
            status = "Scanned (Manual Mode)"
        
        # Log the event
        self.log_rfid_event(rfid_id, student_name, roll_number, status)
        
        print(f"Student: {student_name} ({roll_number}) - Status: {status}")
    
    def mark_rfid_attendance(self, student_id, subject_id):
        """Mark attendance via RFID scan"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                current_date = datetime.now().date()
                current_time = datetime.now().time()
                
                # Check if attendance already marked today
                check_query = """
                SELECT COUNT(*) FROM attendance 
                WHERE student_id = %s AND subject_id = %s AND attendance_date = %s
                """
                cursor.execute(check_query, (student_id, subject_id, current_date))
                
                if cursor.fetchone()[0] > 0:
                    print("Attendance already marked for today")
                    return False
                
                # Check time window (if it's too late, might be leaving)
                # This could be used for entry/exit tracking
                
                # Mark attendance
                insert_query = """
                INSERT INTO attendance (student_id, subject_id, attendance_date, status, marked_by, marked_time)
                VALUES (%s, %s, %s, 'present', 0, %s)
                """
                
                # Add marked_time column if not exists (for RFID timestamp)
                try:
                    cursor.execute("ALTER TABLE attendance ADD COLUMN marked_time TIME")
                    connection.commit()
                except:
                    pass  # Column might already exist
                
                cursor.execute(insert_query, (student_id, subject_id, current_date, current_time))
                connection.commit()
                
                print(f"Attendance marked successfully for student ID: {student_id}")
                return True
                
            except Exception as e:
                print(f"Failed to mark RFID attendance: {str(e)}")
                return False
            finally:
                cursor.close()
                connection.close()
        
        return False
    
    def log_rfid_event(self, rfid_id, student_name, roll_number, status):
        """Log RFID scanning events"""
        # This could be stored in a separate RFID logs table
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] RFID: {rfid_id} | Student: {student_name} | Roll: {roll_number} | Status: {status}"
        print(log_entry)
        
        # Store in file or database for audit trail
        try:
            with open("rfid_logs.txt", "a") as log_file:
                log_file.write(log_entry + "\n")
        except:
            pass
    
    def register_student_rfid(self, student_id, rfid_id):
        """Register RFID card to student (for admin use)"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Add RFID column to students table if not exists
                try:
                    cursor.execute("ALTER TABLE students ADD COLUMN rfid_card_id VARCHAR(50) UNIQUE")
                    connection.commit()
                except:
                    pass  # Column might already exist
                
                # Update student with RFID
                update_query = "UPDATE students SET rfid_card_id = %s WHERE student_id = %s"
                cursor.execute(update_query, (rfid_id, student_id))
                connection.commit()
                
                print(f"RFID {rfid_id} registered to student ID {student_id}")
                return True
                
            except Exception as e:
                print(f"Failed to register RFID: {str(e)}")
                return False
            finally:
                cursor.close()
                connection.close()
        
        return False
    
    def get_student_by_rfid(self, rfid_id):
        """Get student information by RFID"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                SELECT student_id, roll_number, full_name, class_name 
                FROM students 
                WHERE rfid_card_id = %s
                """
                cursor.execute(query, (rfid_id,))
                return cursor.fetchone()
                
            except Exception as e:
                print(f"Failed to get student by RFID: {str(e)}")
                return None
            finally:
                cursor.close()
                connection.close()
        
        return None

# RFID Hardware Integration Examples
class RFIDHardwareInterface:
    """Examples of hardware integration for different RFID readers"""
    
    @staticmethod
    def setup_rc522_raspberry_pi():
        """Setup RC522 RFID reader on Raspberry Pi"""
        setup_code = """
        # Hardware Setup for RC522 on Raspberry Pi
        # Install required libraries:
        # pip install mfrc522 RPi.GPIO spidev
        
        import RPi.GPIO as GPIO
        from mfrc522 import SimpleMFRC522
        
        class RC522Reader:
            def __init__(self):
                self.reader = SimpleMFRC522()
            
            def read_card(self):
                try:
                    id, text = self.reader.read()
                    return str(id)
                except:
                    return None
            
            def write_card(self, text):
                try:
                    self.reader.write(text)
                    return True
                except:
                    return False
        """
        return setup_code
    
    @staticmethod
    def setup_usb_rfid_reader():
        """Setup USB RFID reader"""
        setup_code = """
        # Hardware Setup for USB RFID Reader
        # Install required libraries:
        # pip install pyserial
        
        import serial
        import time
        
        class USBRFIDReader:
            def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
                self.serial_connection = serial.Serial(port, baudrate)
            
            def read_card(self):
                if self.serial_connection.in_waiting:
                    data = self.serial_connection.readline()
                    return data.decode('utf-8').strip()
                return None
            
            def close(self):
                self.serial_connection.close()
        """
        return setup_code
    
    @staticmethod
    def setup_hid_rfid_reader():
        """Setup HID RFID reader (keyboard emulation)"""
        setup_code = """
        # Hardware Setup for HID RFID Reader
        # These readers emulate keyboard input
        # Install required libraries:
        # pip install pynput
        
        from pynput import keyboard
        
        class HIDRFIDReader:
            def __init__(self, callback_function):
                self.callback = callback_function
                self.current_input = ""
                self.listener = keyboard.Listener(on_press=self.on_key_press)
                self.listener.start()
            
            def on_key_press(self, key):
                try:
                    if key == keyboard.Key.enter:
                        if self.current_input:
                            self.callback(self.current_input)
                            self.current_input = ""
                    else:
                        self.current_input += key.char
                except AttributeError:
                    pass  # Special keys
        """
        return setup_code

# Demo function for testing
def demo_rfid_system():
    """Demo function to test RFID system"""
    rfid_system = RFIDAttendanceSystem()
    
    print("Starting RFID Demo...")
    rfid_system.start_rfid_scanning(subject_id=1)  # Demo with subject ID 1
    
    try:
        time.sleep(30)  # Run demo for 30 seconds
    except KeyboardInterrupt:
        pass
    
    rfid_system.stop_rfid_scanning()
    print("RFID Demo completed.")

if __name__ == "__main__":
    demo_rfid_system()
