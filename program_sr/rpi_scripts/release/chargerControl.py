import MySQLdb
import pigpio
import sys
import time

def main():
    #Run pigpiod is called on getSensorData script

    #Init charger control
    CTRL_CHARGING = 18
    try:
        pi = pigpio.pi()
        while True:
            #Read from DB
            db = MySQLdb.connect("localhost","monitor","1234","srDB")
            curs = db.cursor()
            cmd = "SELECT srVBat FROM srCurrent ORDER BY srVBat ASC LIMIT 1"
            curs.execute(cmd)
            value = curs.fetchone()
            vbat = value[0]
            db.close()
            print vbat
            print type(vbat)

            #Charging logic
            #if vbat is NULL, charging 50%
            #if vbat < 50, charging 100%
            #if vbat < 55, charging 75%
            #else, not charging
            #sleep for 1 min to make bat voltage return to normal
            if vbat is None:
                pi.set_PWM_dutycycle(CTRL_CHARGING, 128) #PWM 1/2 on
                time.sleep(600)
                pi.set_PWM_dutycycle(CTRL_CHARGING, 0)   #PWM off
            elif vbat < 50:
                pi.set_PWM_dutycycle(CTRL_CHARGING, 255) #PWM full on
                time.sleep(600)
                pi.set_PWM_dutycycle(CTRL_CHARGING, 0)   #PWM off
            elif vbat < 55:
                pi.set_PWM_dutycycle(CTRL_CHARGING, 192) #PWM 3/4 on
                time.sleep(600)
                pi.set_PWM_dutycycle(CTRL_CHARGING, 0)   #PWM off
            else:
                pi.set_PWM_dutycycle(CTRL_CHARGING, 0)   #PWM off
            time.sleep(30)
    except:
        print 'Error charger control'
        pi.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()
