#!/usr/bin/python
 
#Columns of srCurrent table
#Used in:
#readSensor.py
cols = ['srVAC','srVPS','srVBat','srIBat','srILoad','sr6V5','sr12V','sr13V5','sr19V5','sr24V','sr48V_A','sr48V_B','srTemp']

#Coefficient sensor values
coefSen = {
    cols[0]:0.4610389610,
    cols[1]:0.2334090909,
    cols[2]:0.2334090909,
    cols[3]:0.073982,
    cols[4]:0.073982,
    cols[5]:0.0536163522,
    cols[6]:0.0537605042,
    cols[7]:0.0292653673,
    cols[8]:0.0097848664,
    cols[9]:0.0144177671,
    cols[10]:0.0144551282,
    cols[11]:0.0293917274
}

#Default sensor values
defSen = {cols[0]:220, cols[1]:56, cols[2]:56, cols[5]:6.5, cols[6]:12, cols[7]:13.5, cols[8]:19.5, cols[9]:24, cols[10]:56, cols[11]:56, cols[12]:25}

#LED pin
ledPin = {'INDC_SPLY_OUTS':16, 'INDC_HEALTH_RED':20, 'INDC_HEALTH_GREEN':26}

#Blinking routine of each LED
leds = ['ledSupplyBlue.py','ledHealthRed.py','ledHealthGreen.py']
