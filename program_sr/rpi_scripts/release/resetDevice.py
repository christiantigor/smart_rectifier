import pigpio
import subprocess
import sys
import time
from tsrParams import rstButton

def main():
    #Run pigpiod is called on getSensorData script

    #Active Low
    try:
        pi = pigpio.pi()
        pi.set_mode(rstButton, pigpio.INPUT)
        pi.set_pull_up_down(rstButton, pigpio.PUD_UP)
        pressCount = 0
        while True:
            state = pi.read(rstButton)
            print state

            if state == 0:
                pressCount += 1

            if pressCount > 5:
                print 'Reset device'
                pressCount = 0

                #Copy default network parameter
                cmd = cmd = 'sudo cp /etc/network/interfaces.default /etc/network/interfaces'
                psCopy = subprocess.Popen(
                    [cmd],
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    shell = True
                )
                psCopy.communicate()

                #Change file permission
                cmd = 'sudo chmod 666 /etc/network/interfaces'
                psChange = subprocess.Popen(
                    [cmd],
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    shell = True
                )
                psChange.communicate()

                #Reboot device
                cmd = 'sudo reboot'
                psReboot = subprocess.Popen(
                    [cmd],
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    shell = True
                )
                psReboot.communicate()
                while True:
                    pass
            time.sleep(1)
    except:
        print 'Error reset device'
        pi.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()
