# Arduino RC522 RFID Setup Guide

## Hardware Connections (Arduino Uno + RC522)

```
RC522 Pin  →  Arduino Pin
VCC        →  3.3V
RST        →  Digital Pin 9
GND        →  GND
MISO       →  Digital Pin 12
MOSI       →  Digital Pin 11
SCK        →  Digital Pin 13
SDA(SS)    →  Digital Pin 10
```

## Arduino Code

```cpp
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("RFID Reader Ready - Place card near reader");
}

void loop() {
  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  
  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  
  // Read UID
  String rfidID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    rfidID += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
    rfidID += String(mfrc522.uid.uidByte[i], HEX);
  }
  rfidID.toUpperCase();
  
  // Send to Python via Serial
  Serial.print("RFID:");
  Serial.println(rfidID);
  
  // Stop reading
  mfrc522.PICC_HaltA();
  
  delay(1000); // Prevent multiple reads
}
```

## Required Arduino Libraries
- Install via Arduino IDE Library Manager:
  - MFRC522 by GithubCommunity
  - SPI (usually pre-installed)
