# USB RFID Reader Setup Guide

## Hardware Options

### 1. USB HID RFID Reader (Keyboard Emulation)
- **Price:** $15-30
- **Pros:** Plug & play, no drivers needed
- **Cons:** Acts like keyboard, can interfere with typing

### 2. USB Serial RFID Reader
- **Price:** $20-40  
- **Pros:** Dedicated communication, no interference
- **Cons:** May need drivers

## Setup for HID RFID Reader

### Python Code for HID Reader

```python
import time
from pynput import keyboard
import threading
import queue

class HIDRFIDReader:
    def __init__(self, callback_function):
        self.callback = callback_function
        self.current_input = ""
        self.rfid_queue = queue.Queue()
        self.is_reading = False
        
        # Start keyboard listener
        self.listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        
    def start_reading(self):
        """Start the RFID reader"""
        self.is_reading = True
        self.listener.start()
        
        # Start processing thread
        self.process_thread = threading.Thread(target=self.process_rfid_input)
        self.process_thread.daemon = True
        self.process_thread.start()
        
        print("HID RFID Reader started. Scan a card...")
        
    def stop_reading(self):
        """Stop the RFID reader"""
        self.is_reading = False
        self.listener.stop()
        
    def on_key_press(self, key):
        """Handle key press events"""
        try:
            if key == keyboard.Key.enter:
                if self.current_input and len(self.current_input) >= 8:  # Typical RFID length
                    self.rfid_queue.put(self.current_input)
                self.current_input = ""
            elif hasattr(key, 'char') and key.char:
                self.current_input += key.char
        except AttributeError:
            pass  # Special keys
            
    def on_key_release(self, key):
        """Handle key release events"""
        pass
        
    def process_rfid_input(self):
        """Process RFID input from queue"""
        while self.is_reading:
            try:
                rfid_id = self.rfid_queue.get(timeout=1)
                print(f"RFID Scanned: {rfid_id}")
                self.callback(rfid_id)
            except queue.Empty:
                continue

# Usage Example
def handle_rfid_scan(rfid_id):
    """Handle when RFID is scanned"""
    print(f"Processing RFID: {rfid_id}")
    # Add your attendance marking logic here

# Start the reader
reader = HIDRFIDReader(handle_rfid_scan)
reader.start_reading()

# Keep running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    reader.stop_reading()
    print("RFID Reader stopped")
```

## Setup for Serial RFID Reader

### Required Libraries
```bash
pip install pyserial
```

### Python Code for Serial Reader

```python
import serial
import time
import threading

class SerialRFIDReader:
    def __init__(self, port='COM3', baudrate=9600, callback=None):
        self.port = port
        self.baudrate = baudrate
        self.callback = callback
        self.serial_connection = None
        self.is_reading = False
        
    def connect(self):
        """Connect to the RFID reader"""
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            print(f"Connected to RFID reader on {self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False
            
    def start_reading(self):
        """Start reading RFID cards"""
        if not self.connect():
            return False
            
        self.is_reading = True
        self.read_thread = threading.Thread(target=self._read_loop)
        self.read_thread.daemon = True
        self.read_thread.start()
        
        print("Serial RFID Reader started...")
        return True
        
    def stop_reading(self):
        """Stop reading RFID cards"""
        self.is_reading = False
        if self.serial_connection:
            self.serial_connection.close()
        print("RFID Reader stopped")
        
    def _read_loop(self):
        """Main reading loop"""
        while self.is_reading:
            try:
                if self.serial_connection.in_waiting:
                    data = self.serial_connection.readline()
                    rfid_id = data.decode('utf-8').strip()
                    
                    if rfid_id and len(rfid_id) >= 8:  # Valid RFID
                        print(f"RFID Scanned: {rfid_id}")
                        if self.callback:
                            self.callback(rfid_id)
                            
                time.sleep(0.1)  # Small delay
                
            except Exception as e:
                print(f"Reading error: {e}")
                time.sleep(1)

# Usage Example
def handle_rfid_scan(rfid_id):
    """Handle RFID scan"""
    print(f"Processing RFID: {rfid_id}")

# Auto-detect COM port (Windows)
import serial.tools.list_ports

def find_rfid_port():
    """Find the RFID reader COM port"""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Found port: {port.device} - {port.description}")
        # Try to connect and test
        try:
            test_serial = serial.Serial(port.device, 9600, timeout=2)
            test_serial.close()
            return port.device
        except:
            continue
    return None

# Start the reader
port = find_rfid_port()
if port:
    reader = SerialRFIDReader(port=port, callback=handle_rfid_scan)
    reader.start_reading()
else:
    print("No RFID reader found")
```

## Troubleshooting USB Readers

### Windows:
1. **Check Device Manager:** Look for "Human Interface Devices" or "Ports (COM & LPT)"
2. **Install Drivers:** Some readers need specific drivers
3. **Test in Notepad:** HID readers should type when cards are scanned

### Linux:
```bash
# Check USB devices
lsusb

# Check serial ports
ls /dev/ttyUSB* /dev/ttyACM*

# Add user to dialout group for serial access
sudo usermod -a -G dialout $USER
```

### Testing:
1. **HID Reader:** Open notepad, scan card, should type numbers
2. **Serial Reader:** Use serial terminal (PuTTY, screen) to test communication
