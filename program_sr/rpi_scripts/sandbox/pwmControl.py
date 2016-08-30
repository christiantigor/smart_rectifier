import MySQLdb
import pigpio
import sys
import time

def main():
    CTRL_CHARGING = 18
    i = 0
    try:
        pi = pigpio.pi()
        while True:
            #PWM control
            if i%4 == 0:
                print "PWM 0%"
                pi.set_PWM_dutycycle(CTRL_CHARGING, 0)
            elif i%4 == 1:
                print "PWM 25%"
                pi.set_PWM_dutycycle(CTRL_CHARGING, 64)
            elif i%4 == 2:
                print "PWM 50%"
                pi.set_PWM_dutycycle(CTRL_CHARGING, 128)
            else:
                print "PWM 100%"
                pi.set_PWM_dutycycle(CTRL_CHARGING, 255)
            time.sleep(10)
            
            #Read from DB
            db = MySQLdb.connect("localhost","monitor","1234","srDB")
            curs = db.cursor()
            cmd = "SELECT srVBat FROM srCurrent ORDER BY srVBat ASC LIMIT 1"
            curs.execute(cmd)
            value = curs.fetchone()
            vbat = value[0]
            db.close()
            print vbat
            time.sleep(5)
            i += 1
    except:
        pi.set_PWM_dutycycle(CTRL_CHARGING, 0)
        pi.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()
