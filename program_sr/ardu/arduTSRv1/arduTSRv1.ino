#include "DHT.h"

#define DHTPIN  10
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

byte ledCtrl = 0;

//sensor pin
byte pinVAC     = 3;
byte pinVBat    = 1;
byte pinIBat    = 0;
byte pinILoad   = 2;
byte pin48V_A   = 5;
byte pin48V_B   = 4;
byte pin24V     = 7;
byte pinSupply  = 6;

//sensor value
int adcVal        = 0;
int maxAdcVal     = 0;
long sumAdcVal    = 0;
long numReading   = 0;
int numSamples    = 200;
float valVAC      = 0.0;
float valVBat     = 0.0;
float valIBat     = 0.0;
float valILoad    = 0.0;
float val48V_A    = 0.0;
float val48V_B    = 0.0;
float val24V      = 0.0;
float val6V5      = 0.0;
float val12V      = 0.0;
float val13V5     = 0.0;
float val19V5     = 0.0;
float valTemp     = 0.0;

//control pin
byte pinSelSens1 = 11;
byte pinSelSens2 = 12;
byte pinSelSens3 = 13;

//sensor data to send
char charData[8];
String strJSON;
String strData;

int supplyVoltage;
boolean zeroCross = false;
unsigned long start;

void setup(){
  //Serial.begin(9600);
  Serial.begin(57600);
  
  //begin DHT11
  dht.begin();
  delay(2000);
  
  //set sensor pin as input
  
  //set control pin as output
  pinMode(pinSelSens1, OUTPUT);
  pinMode(pinSelSens2, OUTPUT);
  pinMode(pinSelSens3, OUTPUT);
  
  //set control pin default
  digitalWrite(pinSelSens1, LOW);
  digitalWrite(pinSelSens2, LOW);
  digitalWrite(pinSelSens3, LOW);

  //discarding first readings
  for(int i=0; i<numSamples; i++) {
    analogRead(pinVAC);  
  }
}

void loop(){
  //read sensor value
  
  //VAC
  start = millis();
  
  while(true){
    zeroCross = false;
    while(!zeroCross) {
      adcVal = analogRead(pinVAC);
      if(adcVal < 90) {
        Serial.print("\n");
        zeroCross = true;  
      } 
      if((millis()-start)>2000) zeroCross = true;  
    }

    start = millis();
    maxAdcVal = 0;
    while(true){
      adcVal = analogRead(pinVAC);
      if(adcVal > maxAdcVal) {
        maxAdcVal = adcVal;  
      }
      delay(1);
      if((millis()-start)>500) break;
    }
    Serial.println(maxAdcVal);
  }
  
  /*
  start = millis();
  
  zeroCross = false;
  while(!zeroCross) {
    adcVal = analogRead(pinVAC);
    if(adcVal < 90) {
      zeroCross = true;
      //Serial.print("\n");  
    } 
    if((millis()-start)>2000) zeroCross = true;  
  }

  sumAdcVal = 0;
  numReading = 0;
  start = millis();
  while(true){
    adcVal = analogRead(pinVAC);
    sumAdcVal += adcVal;
    numReading++;
    //Serial.println(adcVal);
    delay(1);
    if((millis()-start)>500) break;
  }
  adcVal = int(sumAdcVal/numReading);
  //Serial.println(adcVal);
  
  if(adcVal > 100.0) {
    valVAC = adcVal * 1.0;
    //valVAC = adcVal * 0.723905;
  } else {
    valVAC = 0.0;  //To handle case when (sometimes) there is no VAC, but ADC is not zero
  }
  */
  

  //VBat
  sumAdcVal = 0;
  for(int i=0; i<numSamples; i++) {
    sumAdcVal += analogRead(pinVBat);  
  }
  adcVal = int(sumAdcVal/numSamples);
  valVBat = adcVal * 0.2334090909;
  
  //IBat
  sumAdcVal = 0;
  for(int i=0; i<numSamples; i++) {
    sumAdcVal += analogRead(pinIBat);  
  }
  adcVal = int(sumAdcVal/numSamples);
  valIBat = (adcVal-511.0) * 0.073982;
  //res_adc(V/step) / res_acs(V/A) = A/step
  //5/1024          / 0.066
  
  //ILoad
  sumAdcVal = 0;
  for(int i=0; i<numSamples; i++) {
    sumAdcVal += analogRead(pinILoad);  
  }
  adcVal = int(sumAdcVal/numSamples);
  valILoad = (adcVal-511.0)*0.073982;

  //48V_A
  sumAdcVal = 0;
  for(int i=0; i<numSamples; i++) {
    sumAdcVal += analogRead(pin48V_A);  
  }
  adcVal = int(sumAdcVal/numSamples);
  val48V_A = adcVal * 0.0536163522;
  
  //48V_B
  sumAdcVal = 0;
  for(int i=0; i<numSamples; i++) {
    sumAdcVal += analogRead(pin48V_B);  
  }
  adcVal = int(sumAdcVal/numSamples);
  val48V_B = adcVal * 0.0537605042;
  
  //24V
  sumAdcVal = 0;
  for(int i=0; i<numSamples; i++) {
    sumAdcVal += analogRead(pin24V);  
  }
  adcVal = int(sumAdcVal/numSamples);
  val24V = adcVal * 0.0292653673;
  
  //pinSelSens1 = 0; pinSelSens2 = X; pinSelSens3 = 0 -> 6V5
  digitalWrite(pinSelSens1, LOW);
  digitalWrite(pinSelSens3, LOW);
  delay(10);
  sumAdcVal = 0;
  for(int i=0; i<numSamples; i++) {
    sumAdcVal += analogRead(pinSupply);  
  }
  adcVal = int(sumAdcVal/numSamples);
  val6V5 = adcVal * 0.0097848664;

  //pinSelSens1 = 0; pinSelSens2 = X; pinSelSens3 = 1 -> 12V
  digitalWrite(pinSelSens1, LOW);
  digitalWrite(pinSelSens3, HIGH);
  delay(10);
  sumAdcVal = 0;
  for(int i=0; i<numSamples; i++) {
    sumAdcVal += analogRead(pinSupply);  
  }
  adcVal = int(sumAdcVal/numSamples);
  val12V = adcVal * 0.0144177671;
  
  //pinSelSens1 = 1; pinSelSens2 = 0; pinSelSens3 = X -> 13V5
  digitalWrite(pinSelSens1, HIGH);
  digitalWrite(pinSelSens2, LOW);
  delay(10);
  sumAdcVal = 0;
  for(int i=0; i<numSamples; i++) {
    sumAdcVal += analogRead(pinSupply);  
  }
  adcVal = int(sumAdcVal/numSamples);
  val13V5 = adcVal * 0.0144551282;
  
  //pinSelSens1 = 1; pinSelSens2 = 1; pinSelSens3 = X -> 19V5
  digitalWrite(pinSelSens1, HIGH);
  digitalWrite(pinSelSens2, HIGH);
  delay(10);
  sumAdcVal = 0;
  for(int i=0; i<numSamples; i++) {
    sumAdcVal += analogRead(pinSupply);  
  }
  adcVal = int(sumAdcVal/numSamples);
  val19V5 = adcVal * 0.0293917274;
  
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

  strJSON += "\",\"6V5\":\"";
  dtostrf(val6V5,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"12V\":\"";
  dtostrf(val12V,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"13V5\":\"";
  dtostrf(val13V5,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"19V5\":\"";
  dtostrf(val19V5,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"24V\":\"";
  dtostrf(val24V,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"48V_A\":\"";
  dtostrf(val48V_A,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"48V_B\":\"";
  dtostrf(val48V_B,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\",\"Temp\":\"";
  dtostrf(valTemp,4,2,charData);
  strData = String(charData);
  strJSON += strData;
  
  strJSON += "\"}";
  
  //send data via serial
  Serial.println(strJSON);

  //some delay
  delay(1000);
}
