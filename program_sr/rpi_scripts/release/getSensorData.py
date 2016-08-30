import difflib
import json
import MySQLdb
import pigpio
import re
import subprocess
import sys
import time

RXD = 15
baud = 57600

saveLoop = 15	#Save once per saveLoop and one loop is about 1 second

def isJson(myJson):
    try:
        obj = json.loads(myJson)
    except ValueError,e:
        return False
    return True

def main():
    #Run pigpiod (Move to new file)
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
            
            #Update latest data to current DB
            if isJson(latestData):
                jsonObj = json.loads(latestData)
                db = MySQLdb.connect("localhost","monitor","1234","srDB")
                curs = db.cursor()
                with db:
                    cmd = ('UPDATE srCurrent SET ' +
                          'srVAC = ' + str(jsonObj.get("VAC","NULL")) + ', ' +
                          'srVPS = ' + str(jsonObj.get("VPS","NULL")) + ', ' +
                          'srVBat = ' + str(jsonObj.get("VBat","NULL")) + ', ' +
                          'srIBat = ' + str(jsonObj.get("IBat","NULL")) + ', ' +
                          'srILoad = ' + str(jsonObj.get("ILoad","NULL")) + ', ' +
                          'sr6V5 = ' + str(jsonObj.get("6V5","NULL")) + ', ' +
                          'sr12V = ' + str(jsonObj.get("12V","NULL")) + ', ' +
                          'sr13V5 = ' + str(jsonObj.get("13V5","NULL")) + ', ' +
                          'sr19V5 = ' + str(jsonObj.get("19V5","NULL")) + ', ' +
                          'sr24V = ' + str(jsonObj.get("24V","NULL")) + ', ' +
                          'sr48V_A = ' + str(jsonObj.get("48V_A","NULL")) + ', ' +
                          'sr48V_B = ' + str(jsonObj.get("48V_B","NULL")) + ', ' +
                          'srTemp = ' + str(jsonObj.get("Temp","NULL")) + ' ' +
                          'WHERE id = 0'
                          )
                    #print cmd
                    print 'update srCurrent'
                    curs.execute(cmd)
                db.close()

            #Count number record on history DB
            db = MySQLdb.connect("localhost","monitor","1234","srDB")
            curs = db.cursor()
            with db:
                cmd = ('SELECT COUNT(*) FROM srHistory')
                #print cmd
                curs.execute(cmd)
                fo = curs.fetchone()
                num = fo[0]
                if num > 10000:
                    cmd = ('DELETE FROM srHistory WHERE sendStat = 1 LIMIT 10')
                    #print cmd
                    print 'delete'
                    curs.execute(cmd)
                if num > 1000000:
                    cmd = ('TRUNCATE srHistory')
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
                dtDateTime = dtDate + ' ' + dtTime
                
                db = MySQLdb.connect("localhost","monitor", "1234", "srDB")
                curs = db.cursor()
                with db:
                    cmd = ('INSERT INTO srHistory ' +
                          'values(NULL,"' + dtDateTime + '",' +
                          str(jsonObj.get("VAC","NULL")) + ',' +
                          str(jsonObj.get("VPS","NULL")) + ',' +
                          str(jsonObj.get("VBat","NULL")) + ',' +
                          str(jsonObj.get("IBat","NULL")) + ',' +
                          str(jsonObj.get("ILoad","NULL")) + ',' +
                          str(jsonObj.get("6V5","NULL")) + ',' +
                          str(jsonObj.get("12V","NULL")) + ',' +
                          str(jsonObj.get("13V5","NULL")) + ',' +
                          str(jsonObj.get("19V5","NULL")) + ',' +
                          str(jsonObj.get("24V","NULL")) + ',' +
                          str(jsonObj.get("48V_A","NULL")) + ',' +
                          str(jsonObj.get("48V_B","NULL")) + ',' +
                          str(jsonObj.get("Temp","NULL")) + ',' +
                          '0)')
                    #print cmd
                    print 'insert srHistory'
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
