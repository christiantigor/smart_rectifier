import pigpio
import sys
import time
from tsrParams import ledPin

def main():
    #Run pigpiod is called on getSensorData script

    #Init led control
    pin = ledPin['INDC_SPLY_OUTS']
    try:
        pi = pigpio.pi()
        while True:
            pi.write(pin,1)
            time.sleep(0.5)
            pi.write(pin,0)
            time.sleep(0.5)
    except:
        print 'Error led control'
        pi.write(pin,0)
        pi.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()
