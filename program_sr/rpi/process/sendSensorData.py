import hashlib
import httplib
import MySQLdb
import os
import pigpio
import re
import serial
import subprocess
import sys
import time

hostName = 'demo.tritronik.com'
hostIP   = '36.80.35.8'
hostPort = 8080
urlName  = '/tsr/tsr/upload'
sleepPeriod = 5 #In second

def gprsIsConnect():
    ser = serial.Serial('/dev/ttyAMA0',baudrate=115200, timeout=3.0)
    try:
        ser.write('AT+CIFSR\r\n')
        rspn = ser.read(100)
        return rspn
    except:
        print 'Error gprsIsConnect'
        ser.close()
        sys.exit(1)

def gprsReset():
    #Run pigpiod is called on getSensorData script

    pwrKey = 18
    try:
        pi = pigpio.pi()
        pi.write(pwrKey,0)
        time.sleep(1)
        pi.write(pwrKey,1)
        time.sleep(2)
        pi.write(pwrKey,0)
        time.sleep(2)
    except:
        print 'Error gprsReset'
        pi.write(pwrKey,0)
        time.sleep(1)
        pi.stop()
        sys.exit(1)

def gprsInit():
    ser = serial.Serial('/dev/ttyAMA0',baudrate=115200, timeout=3.0)

    try:
        ser.write('AT+CIPMUX=1\r\n')
        rspn = ser.read(100)
        #print rspn
        time.sleep(0.5)

        count = 0
        while True:
            ser.write('AT+CSTT="indosatgprs","indosat","indosat"\r\n')
            rspn = ser.read(100)
            #print rspn
            if bool(re.search('OK',rspn)):
                break
            time.sleep(0.5)
            count += 1
            if count > 20:
                break
        
        ser.write('AT+CIICR\r\n')
        rspn = ser.read(100)
        #print rspn
        time.sleep(0.5)

        ser.write('AT+CIFSR\r\n')
        rspn = ser.read(100)
        #print rspn
        time.sleep(0.5)
        ser.close()
        return rspn

    except:
        print 'Error gprsInit'
        ser.close()
        sys.exit(1)

def gprsSend(payload):
    ser = serial.Serial('/dev/ttyAMA0',baudrate=115200, timeout=3.0)
    try:
        count = 0
        while True:
            ser.write('AT+CIPSTART=1,"TCP","' + hostIP + '",' + str(hostPort) + '\r\n')
            rspn = ser.read(100)
            #print rspn
            if bool(re.search('CONNECT OK',rspn)):
                break
            time.sleep(0.5)
            count += 1
            if count > 20:
                break
        data = 'AT+CIPSEND=1,' + str(len(payload)) + '\r\n'
        ser.write(data)
        rspn = ser.read(100)
        ser.close()

        ser = serial.Serial('/dev/ttyAMA0',baudrate=115200, timeout=20.0)
        if bool(re.search('>',rspn)):
            ser.write(payload)
            rspnHTTP = ser.read(600)
            #print rspnHTTP
        else:
            pass
            #print 'no ">"'
        ser.close()

        if not bool(re.search('CLOSED',rspn)):
            ser = serial.Serial('/dev/ttyAMA0',baudrate=115200, timeout=3.0)
            ser.write('AT+CIPCLOSE=1,1\r\n')
            rspn = ser.read(100)
            #print rspn
            ser.close()

        return rspnHTTP
    except:
        print 'Error gprsSend'
        ser.close()
        sys.exit()    

def main():
    #Get MAC address
    myMAC = open('/sys/class/net/eth0/address').read()
    myMAC = myMAC[:-1]
    #print myMAC

    #Calculate HMAC
    text = 'tsr-' + myMAC
    hmac = hashlib.md5(text).hexdigest()
    #print hmac

    #Set HTTP header
    header = {"TSR-HMAC":hmac}
    #print header

    #Main routine
    while True:
        #Read data from DB
        try:
            db = MySQLdb.connect('localhost','monitor','1234','smartRectifier')
            curs = db.cursor()
            with db:
                cmd = ('SELECT * FROM sensorDataHistory WHERE sendStatus = 0 ORDER BY tdate DESC, ttime DESC LIMIT 1')
                curs.execute(cmd)
                data = curs.fetchone()
            db.close()
            #print data
        except:
            print 'Error read data from DB'
            sys.exit(1)

        #Get modem type
        try:
            if bool(re.search('HX',data[6])):
                mdmType = 1
            elif bool(re.search('HT',data[6])):
                mdmType = 2
            elif bool(re.search('X-1',data[6])):
                mdmType = 3
            elif bool(re.search('X-3',data[6])):
                mdmType = 4
            else:
                mdmType = 0
        except:
            print 'Error get modem type'
            sys.exit(1)

        #Get modem voltage
        try:
            if mdmType == 1:		#Hughes HX (6.5 & 19.5)
                vMod1 = data[7]		#sensorModem0
                vMod2 = data[9]		#sensorModem2
            elif mdmType == 2:		#Hughes HT (13.5 & 24)
                vMod1 = data[8]		#sensorModem1
                vMod2 = data[10]	#sensorModem3
            elif mdmType == 3:		#iDirect X-1 (24)
                vMod1 = data[10]
                vMod2 = 0.0
            elif mdmType == 4:		#iDirect X-3 (24)
                vMod1 = data[10]
                vMod2 = 0.0
            else:
                vMod1 = 0.0
                vMod2 = 0.0
        except:
            print 'Error get modem voltage'
            sys.exit(1)

        if data is not None:
            #Construct body
            body = ('{"uid": "' + myMAC +
                    '","type": ' + str(mdmType) +
                    ',"ivac": ' + str(data[2]) +
                    ',"ovdc": ' + '0.0' +
                    ',"bvol": ' + str(data[3]) +
                    ',"bcur": ' + str(data[4]) +
                    ',"lcur": ' + str(data[5]) +
                    ',"vbuc": ' + str(data[11]) +
                    ',"vscpc": ' + str(data[12]) +
                    ',"vmod1": ' + str(vMod1) +
                    ',"vmod2": ' + str(vMod2) +
                    ',"vwifi": ' + str(data[13]) + '}')
            #print body

            #Check whether ETH connected to internet
            rspn = os.system("ping -c 1 -w 3 " + hostName)
            
            if rspn == 0:
                #Send data with ETH
                print 'ETH'
                conn = httplib.HTTPConnection(hostName)
                conn.request('POST',urlName,body,header)
                response = conn.getresponse()
                conn.close()
                respData = response.read()
                #print respData
            else:
                #Check GPRS connection
                print 'GPRS'
                rslt = gprsIsConnect()
                if bool(re.search('CIFSR',rslt)) and bool(re.search('ERROR',rslt)):
                    #GPRS reset
                    #print 'gprsReset twice'
                    gprsReset()
                    time.sleep(0.5)
                    gprsReset()
                    #GPRS init
                    rslt = gprsInit()
                    #print rslt
                elif not bool(re.search('CIFSR',rslt)) and not bool(re.search('ERROR',rslt)):
                    #GPRS reset
                    #print 'gprsReset once'
                    gprsReset()
                    #GPRS init
                    rslt = gprsInit()
                    #print rslt
                else:
                    pass
                    #print rslt

                #Send data with GPRS
                payload = ('POST ' + urlName + ' HTTP/1.1\nHost: ' +
                          hostIP + ':' + str(hostPort) + '\nTSR-HMAC: ' +
                          hmac + '\nContent-Length: ' + str(len(body)) +
                          '\n\n' + body + '\r\n\r\n')
                #print payload
                respData = gprsSend(payload)
                #print respData 

            #Update status on DB
            if bool(re.search('{"status":"success"}',respData)) or bool(re.search('HTTP/1.1 200 OK',respData)):
                print 'update DB status'
                db = MySQLdb.connect('localhost','monitor','1234','smartRectifier')
                curs = db.cursor()
                with db:
                    cmd = ('UPDATE sensorDataHistory SET ' +
                          'sendStatus = 1 ' +
                          'WHERE sendStatus = 0 ORDER BY tdate DESC, ttime DESC LIMIT 1'
                          )
                    #print cmd
                    curs.execute(cmd)
                db.close()
        else:
            print 'All data is sent'

        time.sleep(sleepPeriod)

if __name__ == '__main__':
    main()
