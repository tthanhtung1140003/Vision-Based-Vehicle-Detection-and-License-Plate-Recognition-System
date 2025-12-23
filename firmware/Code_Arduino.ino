#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define RST_PIN 9
#define SS_PIN 10

MFRC522 rfid(SS_PIN, RST_PIN);
Servo myServo;  
void setup() {
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();
  
  myServo.attach(6);
  myServo.write(0);  
}
void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();  
    Serial.print(receivedChar);
    if (receivedChar == 'A' || receivedChar == 'a') {
      Serial.println("Command received: A"); 
      myServo.write(90);
      delay(3000); 
      myServo.write(0);
    }
  }
  if (!rfid.PICC_IsNewCardPresent()) {
    delay(500); 
    return;
  }
  if (!rfid.PICC_ReadCardSerial()) {
    return;
  }
  Serial.print("ID:");
  for (byte i = 0; i < rfid.uid.size; i++) {
    Serial.print(rfid.uid.uidByte[i], HEX);
  }
  Serial.println();
  rfid.PICC_HaltA();
}
