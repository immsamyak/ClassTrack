@echo off
echo Installing RFID Reader Dependencies...
echo.

echo Installing pynput for USB HID RFID readers...
pip install pynput

echo.
echo Installing pyserial for USB Serial RFID readers...
pip install pyserial

echo.
echo Installation complete!
echo.
echo To test your RFID reader:
echo 1. Plug in your USB RFID reader
echo 2. Open Notepad and scan a card to test
echo 3. Run: python windows_rfid_reader.py
echo.
pause
