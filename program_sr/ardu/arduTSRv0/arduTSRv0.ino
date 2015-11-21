#include "DHT.h"

#define DHTPIN  10
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

byte ledCtrl = 0;

//sensor pin
byte pinVAC   = 0;
byte pinIBat  = 1;
byte pinVBat  = 2;
byte pinILoad = 3;
byte pinBUC   = 4;
byte pinSCADA = 5;
byte pinModem = 6;
byte pinSCPC  = 7;

//sensor value
int adcVal       = 0;
float valVAC     = 0.0;
float valIBat    = 0.0;
float valVBat    = 0.0;
float valILoad   = 0.0;
float valBUC     = 0.0;
float valSCADA   = 0.0;
float valSCPC    = 0.0;
float valModem0  = 0.0;
float valModem1  = 0.0;
float valModem2  = 0.0;
float valModem3  = 0.0;
float valTemp    = 0.0;

//control pin
byte pinSelSens1 = 9;
byte pinSelSens2 = 8;
byte pinSelSens3 = 7;

//shift register pin
byte pinLatch = 4;
byte pinClock = 3;
byte pinData  = 5;

//led8 and led9
byte led8 = 12;
byte led9 = 13;

//sensor data to send
char charData[8];
String strJSON;
String strData;

void setup(){
  Serial.begin(9600);
  
  //begin DHT11
  dht.begin();
  delay(2000);
  
  //set control pin as output
  pinMode(pinSelSens1, OUTPUT);
  pinMode(pinSelSens2, OUTPUT);
  pinMode(pinSelSens3, OUTPUT);
  
  //set shift register pin as output
  pinMode(pinLatch, OUTPUT);
  pinMode(pinClock, OUTPUT);
  pinMode(pinData, OUTPUT);
  
  //set led8 and led9 as output
  pinMode(led8, OUTPUT);
  pinMode(led9, OUTPUT);
  
  //set control pin default
  digitalWrite(pinSelSens1, LOW);
  digitalWrite(pinSelSens2, LOW);
  digitalWrite(pinSelSens3, LOW);
  
  //set led8 and led9 default
  digitalWrite(led8, LOW);
  digitalWrite(led9, LOW);
}

void loop(){
  //update indicator
  /*
  setPin(0,HIGH);
  setPin(1,LOW);
  setPin(2,LOW);
  setPin(3,HIGH);
  setPin(4,LOW);
  setPin(5,HIGH);
  setPin(6,LOW);
  setPin(7,HIGH);
  */
  
  //read sensor value
  adcVal = analogRead(pinVAC);  //for future revision
  valVAC = adcVal*1.0;
  if(valVAC < 180 || valVAC > 260) {
    setPin(0,HIGH);
  } else {
    setPin(0,LOW);
  }
  
  adcVal = analogRead(pinIBat);
  valIBat = (adcVal-512.0)*0.073982;
  
  adcVal = analogRead(pinVBat);
  valVBat = adcVal*0.2268288;
  if(valVBat < 30 || valVBat > 70) {
    setPin(2,HIGH);
  } else {
    setPin(2,LOW);
  }
  
  adcVal = analogRead(pinILoad);
  valILoad = (adcVal-512.0)*0.073982;
  
  adcVal = analogRead(pinBUC);
  valBUC = adcVal*0.0537109;
  if(valBUC < 20 || valBUC > 60) {
    setPin(1,HIGH);
  } else {
    setPin(1,LOW);
  }
  
  adcVal = analogRead(pinSCADA);
  valSCADA = adcVal*0.014457;
  if(valSCADA < 8 || valSCADA > 16) {
    setPin(5,HIGH);
  } else {
    setPin(5,LOW);
  }
  
  adcVal = analogRead(pinSCPC);
  valSCPC = adcVal*0.0537109;
  if(valSCPC < 20 || valSCPC > 60) {
    setPin(3,HIGH);
  } else {
    setPin(3,LOW);
  }
  
  //pinSelSens1 = 0; pinSelSens2 = X; pinSelSens3 = 0 -> valModem0 (6.5V)
  digitalWrite(pinSelSens1, LOW);
  digitalWrite(pinSelSens3, LOW);
  delay(100);
  adcVal = analogRead(pinModem);
  valModem0 = adcVal*0.0097656;
  if(valModem0 < 3 || valModem0 > 11) {
    digitalWrite(led8, HIGH);
  } else {
    digitalWrite(led8, LOW);
  }
  
  //pinSelSens1 = 1; pinSelSens2 = 0; pinSelSens3 = X -> valModem1 (13.5V)
  digitalWrite(pinSelSens1, HIGH);
  digitalWrite(pinSelSens2, LOW);
  delay(100);
  adcVal = analogRead(pinModem);
  valModem1 = adcVal*0.014457;
  if(valModem1 < 10 || valModem1 > 18) {
    setPin(6,HIGH);
  } else {
    setPin(6,LOW);
  }
  
  //pinSelSens1 = 0; pinSelSens2 = X; pinSelSens3 = 1 -> valModem2 (19.5V)
  digitalWrite(pinSelSens1, LOW);
  digitalWrite(pinSelSens3, HIGH);
  delay(100);
  adcVal = analogRead(pinModem);
  valModem2 = adcVal*0.0292969;
  if(valModem2 < 16 || valModem2 > 24) {
    digitalWrite(led9, HIGH);
  } else {
    digitalWrite(led9, LOW);
  }
  
  //pinSelSens1 = 1; pinSelSens2 = 1; pinSelSens3 = X -> valModem3 (24V)
  digitalWrite(pinSelSens1, HIGH);
  digitalWrite(pinSelSens2, HIGH);
  delay(100);
  adcVal = analogRead(pinModem);
  valModem3 = adcVal*0.0292969;
  if(valModem3 < 20 || valModem3 > 28) {
    setPin(7,HIGH);
  } else {
    setPin(7,LOW);
  }
  
  //temperature sensor
  valTemp = dht.readTemperature();
  if(isnan(valTemp)) {
    valTemp = 0.0;
  }
  
  //construct data
  strJSON = "{\"VAC\":\"";
  dtostrf(valVAC,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"VBat\":\"";
  dtostrf(valVBat,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"IBat\":\"";
  dtostrf(valIBat,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"ILoad\":\"";
  dtostrf(valILoad,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"Modem0\":\"";
  dtostrf(valModem0,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"Modem1\":\"";
  dtostrf(valModem1,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"Modem2\":\"";
  dtostrf(valModem2,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"Modem3\":\"";
  dtostrf(valModem3,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"BUC\":\"";
  dtostrf(valBUC,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"SCPC\":\"";
  dtostrf(valSCPC,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"SCADA\":\"";
  dtostrf(valSCADA,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"Temp\":\"";
  dtostrf(valTemp,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\"}";
  
  //send data via serial
  Serial.println(strJSON);
  
  //update shift register
  registerWrite();
  
  delay(5000);
}

void setPin(byte whichPin, byte whichState) {
  bitWrite(ledCtrl, whichPin, whichState);
}

void registerWrite() {
  digitalWrite(pinLatch, LOW);
  shiftOut(pinData, pinClock, MSBFIRST, ledCtrl);
  digitalWrite(pinLatch, HIGH);
}
