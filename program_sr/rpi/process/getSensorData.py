import difflib
import json
import MySQLdb
import pigpio
import re
import subprocess
import sys
import time

RXD = 8
baud = 57600
#savePeriod = 15   #In minute
#savePeriod = 5.0  #For battery discharging test - error if run with cron
#savePeriod = 1.0
#savePeriod = 0.25 #0.25 minute or 15 second
#savePeriod = 0.01

#sleepPeriod = 5.0  #In second
#sleepPeriod = 0.5  #In second

saveLoop = 15	#One loop is about 1 second

def isJson(myJson):
    try:
        obj = json.loads(myJson)
    except ValueError,e:
        return False
    return True

def main():
    #Run pigpiod
    try:
        cmd = 'ps -e | grep pigpiod'
        psCheck = subprocess.Popen(
            [cmd],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )
        out, err = psCheck.communicate()
        #print out
        if not bool(re.search('pigpiod',out)):
            #print 'run it'
            cmd = 'sudo pigpiod'
            psRun = subprocess.Popen(
                [cmd],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                shell = True
            )
            out, err = psRun.communicate()
    except:
        print 'Error run pigpiod'
        sys.exit(1)
    
    #Init software serial
    try:
        pi = pigpio.pi()
        pi.set_mode(RXD,pigpio.INPUT)
        pi.bb_serial_read_open(RXD,baud,8)
    except:
        print 'Error init software serial'
        pi.bb_serial_read_close(RXD)
        pi.stop()
        sys.exit(1)

    #Main routine
    loop = 0
    try:
        while True:
            #print 'loop:'
            #print loop    
            #Get data from Arduino
            (count,data) = pi.bb_serial_read(RXD)
            data = str(data)
            #print data

            #Count valid data
            #print 'count:'
            pattern = re.compile(r'(?<={")(\S*?)(?="})')
            listData = re.findall(pattern,data)
            #print len(listData)
            for i, objData in enumerate(listData):
                listData[i] = '{"' + objData  + '"}'
            #print listData
            #for objData in listData:
                #print objData
            
            #Get latest data
            latestData = ''
            if len(listData) > 0:
                latestData = listData[-1]
            
            #Get modem type
            indc0 = pi.read(20)
            indc1 = pi.read(12)
            indc2 = pi.read(16)
            #print 'indc0:%d - indc1:%d - indc2:%d' % (pi.read(20),pi.read(12),pi.read(16))
            if indc0 == 0 and indc1 == 1 and indc2 == 1:
                dtModemType = 'Hughes HX-50'
            elif indc0 == 1 and indc1 == 0 and indc2 == 0:
                dtModemType = 'Hughes HT-1300'
            elif indc0 == 1 and indc1 == 0 and indc2 == 1:
                dtModemType = 'iDirect X-1'
            elif indc0 == 1 and indc1 == 1 and indc2 == 0:
                dtModemType = 'iDirect X-3'
            else:
                dtModemType = 'NULL'
            
            #Update latest data to current DB
            if isJson(latestData):
                jsonObj = json.loads(latestData)
                db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
                curs = db.cursor()
                with db:
                    cmd = ('UPDATE sensorDataCurrent SET ' +
                          'srVAC = ' + str(jsonObj.get("VAC","NULL")) + ', ' +
                          'srVBat = ' + str(jsonObj.get("VBat","NULL")) + ', ' +
                          'srIBat = ' + str(jsonObj.get("IBat","NULL")) + ', ' +
                          'srILoad = ' + str(jsonObj.get("ILoad","NULL")) + ', ' +
                          'mdmType = "' + dtModemType + '", ' +
                          'srMdm0 = ' + str(jsonObj.get("Modem0","NULL")) + ', ' +
                          'srMdm1 = ' + str(jsonObj.get("Modem1","NULL")) + ', ' +
                          'srMdm2 = ' + str(jsonObj.get("Modem2","NULL")) + ', ' +
                          'srMdm3 = ' + str(jsonObj.get("Modem3","NULL")) + ', ' +
                          'srBUC = ' + str(jsonObj.get("BUC","NULL")) + ', ' +
                          'srSCPC = ' + str(jsonObj.get("SCPC","NULL")) + ', ' +
                          'srSCADA = ' + str(jsonObj.get("SCADA","NULL")) + ', ' +
                          'srTemp = ' + str(jsonObj.get("Temp","NULL")) + ' ' +
                          'WHERE name = "currentData"'
                          )
                    #print cmd
                    print 'update'
                    curs.execute(cmd)
                db.close()

            #Count number record on history DB
            db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
            curs = db.cursor()
            with db:
                cmd = ('SELECT COUNT(*) FROM sensorDataHistory')
                #print cmd
                curs.execute(cmd)
                fo = curs.fetchone()
                num = fo[0]
                if num > 10000:
                    cmd = ('DELETE FROM sensorDataHistory WHERE sendStatus = 1 LIMIT 10')
                    #print cmd
                    print 'delete'
                    curs.execute(cmd)
                if num > 1000000:
                    cmd = ('TRUNCATE sensorDataHistory')
                    print cmd
                    curs.execute(cmd)
            db.close()
            
            #Save (only latest) data to history DB
            if(isJson(latestData) and loop > saveLoop):
                jsonObj = json.loads(latestData)
                
                #Get date and time
                cmd = 'sudo hwclock -r'
                dt = subprocess.Popen(
                    [cmd],
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    shell = True
                )
                out, err = dt.communicate()
                dtObj = out.split()
                dtDateSrc = dtObj[1] + ' ' + dtObj[2] + ' ' + dtObj[3]
                dtDateConv = time.strptime(dtDateSrc,"%d %b %Y")
                dtDate = time.strftime("%Y-%m-%d",dtDateConv)
                dtTime = dtObj[4]
                
                db = MySQLdb.connect("localhost","monitor", "1234", "smartRectifier")
                curs = db.cursor()
                with db:
                    cmd = ('INSERT INTO sensorDataHistory ' +
                          'values("' + dtDate + '","' + dtTime  + '",' +
                          str(jsonObj.get("VAC","NULL")) + ',' +
                          str(jsonObj.get("VBat","NULL")) + ',' +
                          str(jsonObj.get("IBat","NULL")) + ',' +
                          str(jsonObj.get("ILoad","NULL")) + ',' +
                          '"' + dtModemType + '",' +
                          str(jsonObj.get("Modem0","NULL")) + ',' +
                          str(jsonObj.get("Modem1","NULL")) + ',' +
                          str(jsonObj.get("Modem2","NULL")) + ',' +
                          str(jsonObj.get("Modem3","NULL")) + ',' +
                          str(jsonObj.get("BUC","NULL")) + ',' +
                          str(jsonObj.get("SCPC","NULL")) + ',' +
                          str(jsonObj.get("SCADA","NULL")) + ',' +
                          str(jsonObj.get("Temp","NULL")) + ',' +
                          '0)')
                    #print cmd
                    print 'insert'
                    curs.execute(cmd)
                db.close()
                loop = 0
            time.sleep(1)
            loop += 1
    except:
        print 'Error main routine'
        pi.bb_serial_read_close(RXD)
        pi.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()
