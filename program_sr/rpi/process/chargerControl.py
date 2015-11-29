import MySQLdb
import pigpio
import sys
import time

def main():
    #Run pigpiod is called on getSensorData script

    #Init charger control
    try:
        pi = pigpio.pi()
        while True:
            #Read from DB
            db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
            curs = db.cursor()
            cmd = "SELECT srVBat FROM sensorDataCurrent ORDER BY srVBat ASC LIMIT 1"
            curs.execute(cmd)
            value = curs.fetchone()
            vbat = value[0]
            db.close()
            print vbat
            #print type(vbat)
            
            #!!! Handler if vbat is NULL !!!
            if vbat is not None and vbat < 50:
                #charging
                pi.write(21,1)
                time.sleep(600)
                pi.write(21,0)
            time.sleep(30)
    except:
        print 'Error charger control'
        pi.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()
