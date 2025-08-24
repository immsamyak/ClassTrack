# RFID Setup for Windows PC

## Recommended Option: USB RFID Reader

### **Best Choice: USB HID RFID Reader**
- **Price:** $15-25 on Amazon/eBay
- **Pros:** Plug & play, no drivers needed, works immediately
- **Search terms:** "USB RFID Reader 125KHz" or "USB RFID Card Reader HID"

### **Alternative: USB Serial RFID Reader**  
- **Price:** $20-35
- **Pros:** More reliable, dedicated communication
- **Search terms:** "USB RFID Reader Serial COM Port"

## Setup Steps

### 1. **Purchase USB HID RFID Reader**
Popular models:
- **Ehuiby USB RFID Reader** (Amazon ~$20)
- **KKmoon USB RFID Card Reader** (eBay ~$15)
- **Geizhals USB Proximity Sensor** (AliExpress ~$12)

### 2. **Test the Reader**
1. Plug into USB port
2. Open Notepad
3. Scan an RFID card
4. Should type numbers like: `0012345678`

### 3. **Install Required Python Package**
```bash
pip install pynput
```

### 4. **Integration Code**

Here's the code to integrate with your existing system:
