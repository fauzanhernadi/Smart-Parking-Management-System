#include <Servo.h>  // includes the servo library

Servo myServo;
Servo backServo;
#define ir_enter 2
#define ir_back 4
#define ir_car1 5
#define ir_car2 6
#define ir_car3 7
#define ir_car4 3
#define ir_keluar1 8
#define ir_keluar2 11

int S1 = 0, S2 = 0, S3 = 0, S4 = 0;
int flag1 = 0, flag2 = 0;
int slot = 4;
int buzzer = 12;

void readSensor() {
  S1 = digitalRead(ir_car1);
  S2 = digitalRead(ir_car2);
  S3 = digitalRead(ir_car3);
  S4 = digitalRead(ir_car4);
}

void setup() {
  Serial.begin(9600);

  pinMode(ir_car1, INPUT);
  pinMode(ir_car2, INPUT);
  pinMode(ir_car3, INPUT);
  pinMode(ir_car4, INPUT);
  pinMode(ir_enter, INPUT);
  pinMode(ir_back, INPUT);
  pinMode(ir_keluar1, INPUT);
  pinMode(ir_keluar2, INPUT);

  myServo.attach(9);
  backServo.attach(10);
  backServo.write(180);
  myServo.write(90);
  pinMode(buzzer, OUTPUT);
  readSensor();
}

void loop() {
  if (slot <= 0) {
    Serial.println(" Sorry Parking Full ");
    digitalWrite(buzzer, HIGH);
    delay(1000);
  } else {
    readSensor();

    if (S1 == LOW) {
      delay(1000);
      Serial.println("S1: Fill ");
      slot = slot - 1;
    } else {
      delay(1000);
      Serial.println("S1: Empty");
    }

    if (S2 == LOW) {
      delay(500);
      Serial.println("S2: Fill ");
      slot = slot - 1;
    } else {
      delay(500);
      Serial.println("S2: Empty");
    }

    if (S3 == LOW) {
      delay(500);
      Serial.println("S3: Fill ");
      slot = slot - 1;
    } else {
      delay(500);
      Serial.println("S3: Empty");
    }

    if (S4 == LOW) {
      delay(500);
      Serial.println("S4: Fill ");
      slot = slot - 1;
    } else {
      delay(500);
      Serial.println("S4: Empty");
    }

    if (S1 == HIGH && S2 == HIGH && S3 == HIGH && S4 == HIGH) {
      // Tidak ada mobil di semua slot, kembalikan slot ke nilai awal
      slot = 4;
    }

    if (digitalRead(ir_enter) == LOW && flag1 == 0) {
      if (slot > 0) {
        flag1 = 1;
        if (flag2 == 0) {
          myServo.write(180);
        }
      }
    }

    if (digitalRead(ir_back) == LOW && flag2 == 0) {
      flag2 = 1;
      if (flag1 == 0) {
        myServo.write(180);
      }
    }

    if (flag1 == 1 && flag2 == 1) {
      delay(1000);
      myServo.write(90);
      flag1 = 0, flag2 = 0;
    }

    if (digitalRead(ir_keluar1) == LOW && flag1 == 0) {
      if (flag2 == 0) {
        backServo.write(180);
      }
      delay(100);
    }

    if (digitalRead(ir_keluar2) == LOW && flag1 == 0) {
      if (flag2 == 0) {
        backServo.write(90);
        slot++;  // Increment slot when ir_keluar2 detects an object
      }
      delay(100);
    }

    Serial.println("   Have Slot: ");
    Serial.println(slot);
    Serial.println("    ");
    delay(100);
  }
}