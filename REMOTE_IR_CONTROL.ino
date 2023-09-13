#define IR_SEND_PIN 3
#define IR_RECEIVE_PIN 11
#include <IRremote.h>

//byte RECV_PIN = 11;
//byte SEND_PIN = 3;
byte MODE; //1-SEND, 2-RECV

IRrecv irrecv(IR_RECEIVE_PIN);
decode_results results;
IRsend irsend;

void setup() {
  Serial.begin(9600);
  irsend.enableIROut(38);
//  irrecv.enableIRIn();
//  pinMode(IR_RECEIVE_PIN, INPUT);
//  pinMode(IR_SEND_PIN, OUTPUT);
  MODE = 0x01;
}

void loop() {
  byte command[1];
  if (MODE == 0x01) {
    if (Serial.available()>0) {
      Serial.readBytes(command, 1);
      if (command[0] == 0xF1) { //SEND
        byte LEN[1];
        Serial.readBytes(LEN,1);
        byte IR_CODE[LEN[0]];
        Serial.readBytes(IR_CODE, LEN[0]);
        long IR_CODE_LONG = 0;
        for (int i=0; i<LEN[0];i++) {
          IR_CODE_LONG <<= 8;
          IR_CODE_LONG |= IR_CODE[i];
        }
        irsend.sendNEC(IR_CODE_LONG, 32); 
        Serial.print(IR_CODE_LONG,HEX);
      }
      if (command[0] == 0xF2) { //switch to RECV
        irrecv.enableIRIn();
        MODE = 0x02;
      }
      delay(200);
    }
  } else if (MODE == 0x02) {
    delay(200);
    if (Serial.available()>0) {
      Serial.readBytes(command, 1);
      if (command[0] == 0xF2) { //switch to SEND
        irrecv.disableIRIn();
//        irsend.enableIROut(38);
        MODE = 0x01;
      }
    }
    if (irrecv.decode(&results) && results.value != 0xFFFFFFFF) {
      Serial.println(results.value, HEX);
      irrecv.disableIRIn();
      delay(100);
      irrecv.enableIRIn();
    }
  }
}
