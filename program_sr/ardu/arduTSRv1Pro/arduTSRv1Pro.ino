//Arduino code for PCB production

#include "DHT.h"
#define DHTPIN  10
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

//sensor pin
byte SENSOR_VAC       = 3;
byte SENSOR_VPS       = 2;
byte SENSOR_IBAT      = 1;
byte SENSOR_ILOAD     = 0;
byte SENSOR_SPLY_A    = 6;  //PCB production use Arduino with swapped pin between A6 and A7
byte SENSOR_SPLY_B    = 7;  //PCB production use Arduino with swapped pin between A6 and A7

//sensor value
int   adcVal        = 0;
int   maxAdcVal     = 0;
long  sumAdcVal     = 0;
long  numReading    = 0;
int   numSamples    = 200;
float valVAC        = 0.0;
float valVPwrSply   = 0.0;
float valVBat       = 0.0;
float valIBat       = 0.0;
float valILoad      = 0.0;
float val48V_A      = 0.0;
float val48V_B      = 0.0;
float val24V        = 0.0;
float val6V5        = 0.0;
float val12V        = 0.0;
float val13V5       = 0.0;
float val19V5       = 0.0;
float valTemp       = 0.0;

//sensor calibration
float calbVAC       = 0.7138157894;
float calbVPS       = 0.2334090909;
float calbVBat      = 0.2334090909;
float calbIBat      = 0.073982;
float calbILoad     = 0.073982;
float calb48V_A     = 0.0536163522;
float calb48V_B     = 0.0537605042;
float calb24V       = 0.0292653673;
float calb6V5       = 0.0097848664;
float calb12V       = 0.0144177671;
float calb13V5      = 0.0144551282;
float calb19V5      = 0.0293917274;

//control pin
byte SEL_SENSOR_1   = 11;
byte SEL_SENSOR_2   = 12;

//sensor data to send
char    charData[8];
String  strJSON;
String  strData;

int     supplyVoltage;
boolean zeroCross = false;
unsigned long start;

void setup(){
  Serial.begin(57600);
  
  //begin DHT11
  dht.begin();
  delay(2000);
  
  //set sensor pin as input
  
  //set control pin as output
  pinMode(SEL_SENSOR_1, OUTPUT);
  pinMode(SEL_SENSOR_2, OUTPUT);
  
  //set control pin default
  digitalWrite(SEL_SENSOR_1, LOW);
  digitalWrite(SEL_SENSOR_2, LOW);

  //discarding first readings
  //for(int i=0; i<numSamples; i++) {
  //  analogRead(SENSOR_VAC);  
  //}
}

void loop(){
  //read sensor value
  
  while(true){
    //VAC
    start = millis();
    zeroCross = false;
    while(!zeroCross) {
      adcVal = analogRead(SENSOR_VAC);
      if(adcVal < 100.0) {
        Serial.print("\n");
        zeroCross = true;  
      } 
      if((millis()-start)>2000) zeroCross = true;  
    }

    //find max ADC val for VAC for certain duration
    //the max ADC value indicate the real VAC voltage
    //we choose this method instead of RMS to make it sense surge voltage
    start = millis();
    maxAdcVal = 0;
    while(true){
      adcVal = analogRead(SENSOR_VAC);
      if(adcVal > maxAdcVal) {
        maxAdcVal = adcVal;  
      }
      delay(1);
      if((millis()-start)>500) break;
    }

    //handle case when there is no VAC, but ADC is not zero
    if(maxAdcVal > 100.0) {
      valVAC = maxAdcVal * calbVAC;
    } else {
      valVAC = 0.0;  
    }
    //Serial.println(valVAC);
	
    //VPS
    sumAdcVal = 0;
    for(int i=0; i<numSamples; i++) {
      sumAdcVal += analogRead(SENSOR_VPS);  
    }
    adcVal = int(sumAdcVal/numSamples);
    valVPwrSply = adcVal * calbVPS;

    //IBat
    sumAdcVal = 0;
    for(int i=0; i<numSamples; i++) {
      sumAdcVal += analogRead(SENSOR_IBAT);  
    }
    adcVal = int(sumAdcVal/numSamples);
    valIBat = (adcVal-511.0) * calbIBat;
    //res_adc(V/step) / res_acs(V/A) = A/step
    //5/1024          / 0.066
    
    //ILoad
    sumAdcVal = 0;
    for(int i=0; i<numSamples; i++) {
      sumAdcVal += analogRead(SENSOR_ILOAD);  
    }
    adcVal = int(sumAdcVal/numSamples);
    valILoad = (adcVal-511.0) * calbILoad;

    //SENSOR_SPLY_A
    //SEL_SENSOR_1 = 0; SEL_SENSOR_2 = 0; -> 24V
    digitalWrite(SEL_SENSOR_1, LOW);
    digitalWrite(SEL_SENSOR_2, LOW);
    delay(10);
    sumAdcVal = 0;
    for(int i=0; i<numSamples; i++) {
      sumAdcVal += analogRead(SENSOR_SPLY_A);  
    }
    adcVal = int(sumAdcVal/numSamples);
    val24V = adcVal * calb24V;
    
    //SEL_SENSOR_1 = 0; SEL_SENSOR_2 = 1; -> 48V_B
    digitalWrite(SEL_SENSOR_1, LOW);
    digitalWrite(SEL_SENSOR_2, HIGH);
    delay(10);
    sumAdcVal = 0;
    for(int i=0; i<numSamples; i++) {
      sumAdcVal += analogRead(SENSOR_SPLY_A);  
    }
    adcVal = int(sumAdcVal/numSamples);
    val48V_B = adcVal * calb48V_B;
    
    //SEL_SENSOR_1 = 1; SEL_SENSOR_2 = 0; -> 48V_A
    digitalWrite(SEL_SENSOR_1, HIGH);
    digitalWrite(SEL_SENSOR_2, LOW);
    delay(10);
    sumAdcVal = 0;
    for(int i=0; i<numSamples; i++) {
      sumAdcVal += analogRead(SENSOR_SPLY_A);  
    }
    adcVal = int(sumAdcVal/numSamples);
    val48V_A = adcVal * calb48V_A;
    
    //SEL_SENSOR_1 = 1; SEL_SENSOR_2 = 1; -> VBat
    digitalWrite(SEL_SENSOR_1, HIGH);
    digitalWrite(SEL_SENSOR_2, HIGH);
    delay(10);
    sumAdcVal = 0;
    for(int i=0; i<numSamples; i++) {
      sumAdcVal += analogRead(SENSOR_SPLY_A);  
    }
    adcVal = int(sumAdcVal/numSamples);
    valVBat = adcVal * calbVBat;

    //SENSOR_SPLY_B
    //SEL_SENSOR_1 = 0; SEL_SENSOR_2 = 0; -> 6V5
    digitalWrite(SEL_SENSOR_1, LOW);
    digitalWrite(SEL_SENSOR_2, LOW);
    delay(10);
    sumAdcVal = 0;
    for(int i=0; i<numSamples; i++) {
      sumAdcVal += analogRead(SENSOR_SPLY_B);  
    }
    adcVal = int(sumAdcVal/numSamples);
    val6V5 = adcVal * calb6V5;

    //SEL_SENSOR_1 = 0; SEL_SENSOR_2 = 1; -> 12V
    digitalWrite(SEL_SENSOR_1, LOW);
    digitalWrite(SEL_SENSOR_2, HIGH);
    delay(10);
    sumAdcVal = 0;
    for(int i=0; i<numSamples; i++) {
      sumAdcVal += analogRead(SENSOR_SPLY_B);  
    }
    adcVal = int(sumAdcVal/numSamples);
    val12V = adcVal * calb12V;
    
    //SEL_SENSOR_1 = 1; SEL_SENSOR_2 = 0; -> 13V5
    digitalWrite(SEL_SENSOR_1, HIGH);
    digitalWrite(SEL_SENSOR_2, LOW);
    delay(10);
    sumAdcVal = 0;
    for(int i=0; i<numSamples; i++) {
      sumAdcVal += analogRead(SENSOR_SPLY_B);  
    }
    adcVal = int(sumAdcVal/numSamples);
    val13V5 = adcVal * calb13V5;
    
    //SEL_SENSOR_1 = 1; SEL_SENSOR_2 = 1; -> 19V5
    digitalWrite(SEL_SENSOR_1, HIGH);
    digitalWrite(SEL_SENSOR_2, HIGH);
    delay(10);
    sumAdcVal = 0;
    for(int i=0; i<numSamples; i++) {
      sumAdcVal += analogRead(SENSOR_SPLY_B);  
    }
    adcVal = int(sumAdcVal/numSamples);
    val19V5 = adcVal * calb19V5;
    
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

    strJSON += "\",\"VPS\":\"";
    dtostrf(valVPwrSply,4,2,charData);
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
}
