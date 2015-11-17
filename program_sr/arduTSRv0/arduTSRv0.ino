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

//sensor data to send
char charData[8];
String strJSON;
String strData;

void setup(){
  Serial.begin(9600);
  
  //set control pin as output
  pinMode(pinSelSens1, OUTPUT);
  pinMode(pinSelSens2, OUTPUT);
  pinMode(pinSelSens3, OUTPUT);
  
  //set shift register pin as output
  pinMode(pinLatch, OUTPUT);
  pinMode(pinClock, OUTPUT);
  pinMode(pinData, OUTPUT);
  
  //set control pin default
  digitalWrite(pinSelSens1, LOW);
  digitalWrite(pinSelSens2, LOW);
  digitalWrite(pinSelSens3, LOW);
}

void loop(){
  //read sensor value
  adcVal = analogRead(pinVAC);  //for future revision
  valVAC = adcVal*1.0;
  
  adcVal = analogRead(pinIBat);
  valIBat = (adcVal-512.0)*0.073982;
  
  adcVal = analogRead(pinVBat);
  valVBat = adcVal*0.2268288;
  
  adcVal = analogRead(pinILoad);
  valILoad = (adcVal-512.0)*0.073982;
  
  adcVal = analogRead(pinBUC);
  valBUC = adcVal*0.0537109;
  
  adcVal = analogRead(pinSCADA);
  valSCADA = adcVal*0.014457;
  
  adcVal = analogRead(pinSCPC);
  valSCPC = adcVal*0.0537109;
  
  //pinSelSens1 = 0; pinSelSens2 = X; pinSelSens3 = 0 -> valModem0
  digitalWrite(pinSelSens1, LOW);
  digitalWrite(pinSelSens3, LOW);
  delay(100);
  adcVal = analogRead(pinModem);
  valModem0 = adcVal*0.0097656;
  
  //pinSelSens1 = 1; pinSelSens2 = 0; pinSelSens3 = X -> valModem1
  digitalWrite(pinSelSens1, HIGH);
  digitalWrite(pinSelSens2, LOW);
  delay(100);
  adcVal = analogRead(pinModem);
  valModem1 = adcVal*0.014457;
  
  //pinSelSens1 = 0; pinSelSens2 = X; pinSelSens3 = 1 -> valModem2
  digitalWrite(pinSelSens1, LOW);
  digitalWrite(pinSelSens3, HIGH);
  delay(100);
  adcVal = analogRead(pinModem);
  valModem2 = adcVal*0.0292969;
  
  //pinSelSens1 = 1; pinSelSens2 = 1; pinSelSens3 = X -> valModem3
  digitalWrite(pinSelSens1, HIGH);
  digitalWrite(pinSelSens2, HIGH);
  delay(100);
  adcVal = analogRead(pinModem);
  valModem3 = adcVal*0.0292969;
  
  //update indicator
  //please test registerWrite after indicator PCB is finished
  
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
  
  strJSON += "\"}";
  
  //send data via serial
  Serial.println(strJSON);
  delay(5000);
}

void registerWrite(byte whichPin, byte whichState) {
  byte bitsToSend = 0;
  digitalWrite(pinLatch, LOW);
  bitWrite(bitsToSend, whichPin, whichState);
  shiftOut(pinData, pinClock, MSBFIRST, bitsToSend);
  digitalWrite(pinLatch, HIGH);
}
