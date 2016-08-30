import pigpio
import sys
import time

def main():
    #Run pigpiod is called on getSensorData script

    #Init led flasher
    INDC_SPLY_OUTS	= 16
    INDC_HEALTH_RED	= 26
    INDC_HEALTH_GREEN	= 20
    INDC_HEALTH_BLUE	= 19

    #Supply voltage
    #Related to srCurrent
    #Normal off, error blinking

    #Health
    #Normal blinking green
    #Network error blinking red
    #Temp error blinking yellow
    #CPU utilization error blinking yellow
    try:
        pi = pigpio.pi()
        while True:
            #time.sleep(4)
            time.sleep(0.2)
            pi.write(23,1)
            time.sleep(0.2)
            pi.write(23,0)
    except:
        print 'Error init led flasher'
        pi.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()

