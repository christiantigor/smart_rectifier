import pigpio
import MySQLdb
import os
import signal
import subprocess
import sys
import time
from tsrParams import *
import urllib2

#Input: file name of led flasher
def turnLedOn(led):
    cmd = 'python ' + led
    ps = subprocess.Popen(
        [cmd],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = True
    )

#Input pid
def checkPid(pid):
    try:
        os.kill(pid,0)
    except OSError:
        return False
    else:
        return True

#Input: file name of led flasher
def turnLedOff(led):
    cmd = 'pgrep -f "python ' + led + '"'
    ps = subprocess.Popen(
        [cmd],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = True
    )
    out, err = ps.communicate()
    pids = out.split()
    for pid in pids:
        if checkPid(int(pid)):
            os.kill(int(pid),signal.SIGTERM)

def checkInet(host):
    try:
        response = urllib2.urlopen(host,timeout=1) #Longer timeout if no network
        return True
    except urllib2.URLError as err: pass
    return False

def main():
    #Algorithm
    #Set all pin low
    #Kill any led blinking process

    #Supply voltage
    #Read srCurrent
    #Normal slow blinking blue
    #Error off (or on)

    #Health
    #Normal slow blinking green
    #Network or temp error slow blinking red

    #Set all pin low
    #Run pigpiod is called on getSensorData script
    pi = pigpio.pi()
    pi.write(ledPin['INDC_SPLY_OUTS'],0)
    pi.write(ledPin['INDC_HEALTH_GREEN'],0)
    pi.write(ledPin['INDC_HEALTH_RED'],0)
    pi.stop()

    #Kill any led blinking process
    try:
        for led in leds:
            turnLedOff(led)
    except Exception as e:
        print e
        print 'Error kill led blinking process'
        sys.exit(1)
    
    try:
        err = 0.05 #5%
        stat = False
        lastStat = None
        statInet = False
        statTemp = False
        lastStatHealth = None
        host = 'http://google.com'
        global temp
        while True:
            #Supply voltage
            #Read srCurrent
            #Normal slow blinking blue
            #Error off (or on)
            try:
                db = MySQLdb.connect("localhost","monitor","1234","srDB")
                curs = db.cursor()
                cmd = "SELECT * FROM srCurrent"
                curs.execute(cmd)
                value = curs.fetchone()
                db.close()
                v = list(value)
                temp = v[-1]
                del v[-1] #Delete srTemp
                del v[5] #Delete srILoad data
                del v[4] #Delete srIBat data
                del v[0] #Delete id data
                #print v
                
                if defSen['srVAC']*(1-err) < v[0] < defSen['srVAC']*(1+err):
                    stat = True
                else:
                    stat = False
                    print 'Error srVAC'
                
                if defSen['srVPS']*(1-err) < v[1] < defSen['srVPS']*(1+err):
                    stat = stat and True
                else:
                    stat = False
                    print 'Error srVPS'
                
                if defSen['srVBat']*(1-err) < v[2] < defSen['srVBat']*(1+err):
                    stat = stat and True
                else:
                    stat = False
                    print 'Error srVBat'
                
                if defSen['sr6V5']*(1-err) < v[3] < defSen['sr6V5']*(1+err):
                    stat = stat and True
                else:
                    stat = False
                    print 'Error sr6V5'
                
                if defSen['sr12V']*(1-err) < v[4] < defSen['sr12V']*(1+err):
                    stat = stat and True
                else:
                    stat = False
                    print 'Error sr12V'
                
                if defSen['sr13V5']*(1-err) < v[5] < defSen['sr13V5']*(1+err):
                    stat = stat and True
                else:
                    stat = False
                    print 'Error sr13V5'
                
                if defSen['sr19V5']*(1-err) < v[6] < defSen['sr19V5']*(1+err):
                    stat = stat and True
                else:
                    stat = False
                    print 'Error sr19V5'
                
                if defSen['sr24V']*(1-err) < v[7] < defSen['sr24V']*(1+err):
                    stat = stat and True
                else:
                    stat = False
                    print 'Error sr24V'
                
                if defSen['sr48V_A']*(1-err) < v[8] < defSen['sr48V_A']*(1+err):
                    stat = stat and True
                else:
                    stat = False
                    print 'Error sr48V_A'
                
                if defSen['sr48V_B']*(1-err) < v[9] < defSen['sr48V_B']*(1+err):
                    stat = stat and True
                else:
                    stat = False
                    print 'Error sr48V_B'
                
                #Led
                if stat == True and (lastStat == False or lastStat is None):
                    print 'slow blinking blue'
                    turnLedOn('ledSupplyBlue.py')
                    lastStat = True
                elif stat == False and (lastStat == True or lastStat is None):
                    print 'turn off blinking'
                    turnLedOff('ledSupplyBlue.py')
                    lastStat = False
                else:
                    pass
            except:
                print 'Error indicator supply voltage'
                sys.exit(1)

            #Health
            #Normal slow blinking green
            #Network or temp error slow blinking red
            #try:
            #    #Check network
            #    if checkInet(host):
            #        statInet = True
            #        print 'Network ok'
            #    else:
            #        statInet = False
            #        print 'Error Network'
            #    #Check temp
            #    if defSen['srTemp']*(1-err) < temp < defSen['srTemp']*(1+err):
            #        statTemp = True
            #        print 'Temp ok'
            #    else:
            #        statTemp = False
            #        print 'Error Temp'
            #
            #    #Led
            #    if statInet == True and statTemp == True and (lastStatHealth == False or lastStatHealth is None):
            #        print 'slow blinking green'
            #        #turnLedOff('ledHealthRed.py')
            #        #turnLedOn('ledHealthGreen.py')
            #        lastStatHealth = True
            #    elif statInet == False or statTemp == False and (lastStatHealth == True or lastStatHealth is None):
            #        print 'slow blinking red'
            #        #turnLedOff('ledHealthGreen.py')
            #        #turnLedOn('ledHealthRed.py')
            #        lastStatHealth = False
            #    else:
            #        pass
            #except:
            #    print 'Error indicator health'
            #    sys.exit(1)
            
            time.sleep(5)
    except:
        print 'Error led flasher'
        turnLedOff('ledSupplyBlue.py')
        turnLedOff('ledHealthGreen.py')
        turnLedOff('ledHealthRed.py')
        sys.exit(1)

if __name__ == '__main__':
    main()
