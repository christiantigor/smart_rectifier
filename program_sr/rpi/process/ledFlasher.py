import pigpio
import sys
import time

def main():
    #Run pigpiod is called on getSensorData script

    #Init led flasher
    try:
        pi = pigpio.pi()
        while True:
            time.sleep(4)
            pi.write(23,1)
            time.sleep(0.5)
            pi.write(23,0)
    except:
        print 'Error init led flasher'
        pi.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()
