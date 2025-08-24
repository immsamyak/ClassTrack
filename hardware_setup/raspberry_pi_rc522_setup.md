# Raspberry Pi RC522 RFID Setup Guide

## Hardware Connections (Raspberry Pi + RC522)

```
RC522 Pin  →  RPi Pin  →  RPi GPIO
VCC        →  Pin 1    →  3.3V
RST        →  Pin 22   →  GPIO 25
GND        →  Pin 6    →  GND
MISO       →  Pin 21   →  GPIO 9 (SPI0_MISO)
MOSI       →  Pin 19   →  GPIO 10 (SPI0_MOSI)
SCK        →  Pin 23   →  GPIO 11 (SPI0_SCLK)
SDA(SS)    →  Pin 24   →  GPIO 8 (SPI0_CE0_N)
```

## Software Setup

### 1. Enable SPI on Raspberry Pi
```bash
sudo raspi-config
# Navigate to: Interfacing Options → SPI → Enable
# Reboot: sudo reboot
```

### 2. Install Required Packages
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
sudo apt install python3-pip python3-dev python3-spi-dev -y

# Install required Python libraries
pip3 install mfrc522 RPi.GPIO spidev
```

### 3. Test SPI Connection
```bash
# Check if SPI is enabled
lsmod | grep spi
# Should show: spi_bcm2835

# Test SPI devices
ls /dev/spi*
# Should show: /dev/spidev0.0  /dev/spidev0.1
```

## Python Code for Raspberry Pi

```python
#!/usr/bin/env python3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import requests
import json

class RaspberryPiRFIDReader:
    def __init__(self, api_url="http://localhost:5000/rfid-scan"):
        self.reader = SimpleMFRC522()
        self.api_url = api_url
        
    def start_reading(self):
        print("RFID Reader started. Place card near reader...")
        
        try:
            while True:
                print("Waiting for card...")
                rfid_id, text = self.reader.read()
                
                print(f"Card detected: {rfid_id}")
                
                # Send to your Python application
                self.send_to_application(str(rfid_id))
                
                time.sleep(2)  # Prevent multiple reads
                
        except KeyboardInterrupt:
            print("\nStopping RFID reader...")
        finally:
            GPIO.cleanup()
    
    def send_to_application(self, rfid_id):
        """Send RFID data to your main application"""
        try:
            payload = {
                "rfid_id": rfid_id,
                "timestamp": time.time()
            }
            
            # Option 1: HTTP API call
            response = requests.post(self.api_url, json=payload)
            if response.status_code == 200:
                print(f"✓ RFID sent to application: {rfid_id}")
            else:
                print(f"✗ Failed to send RFID: {response.status_code}")
                
        except Exception as e:
            print(f"Error sending RFID: {e}")
            
            # Option 2: Write to file (backup method)
            with open("/tmp/rfid_scans.log", "a") as f:
                f.write(f"{time.time()}:{rfid_id}\n")

if __name__ == "__main__":
    reader = RaspberryPiRFIDReader()
    reader.start_reading()
```

## Troubleshooting

### Common Issues:

1. **SPI Not Working:**
```bash
# Check SPI status
sudo raspi-config  # Enable SPI if disabled
sudo reboot
```

2. **Permission Denied:**
```bash
# Add user to SPI group
sudo usermod -a -G spi $USER
sudo reboot
```

3. **Module Not Found:**
```bash
# Reinstall libraries
pip3 uninstall mfrc522
pip3 install mfrc522
```

4. **Wiring Issues:**
- Double-check all connections
- Ensure 3.3V power (NOT 5V - can damage RPi)
- Use short, quality jumper wires
