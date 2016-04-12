import pigpio
import sys
import time
import subprocess

def main():
    #Run pigpiod is called on getSensorData script

    #Init button
    try:
        pi = pigpio.pi()
        button = 18
        #pi.set_mode(button,pigpio.INPUT)
        pressCount = 0
        time.sleep(5)
        while True:
            state = pi.read(button)
            print state

			#check state
            if state == 0:
                pressCount += 1
			else:
			    pressCount = 0
				
			#check pressCount
            if pressCount > 5:
                #Copy default config
                #cmd = 'sudo cp /etc/network/interfaces.default /etc/network/aus'
                cmd = 'sudo cp /etc/network/interfaces.default /etc/network/interfaces'
                psCopy = subprocess.Popen(
                    [cmd],
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    shell = True
                )
                out, err = psCopy.communicate()

                #Change file permission
                #cmd = 'sudo chmod 666 /etc/network/aus'
                cmd = 'sudo chmod 666 /etc/network/interfaces'
                psChange = subprocess.Popen(
                    [cmd],
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    shell = True
                )
                out, err = psChange.communicate()
                print 'pressCount overflow'
                pressCount = 0
                time.sleep(3)

                #Shutdown
                #cmd = 'sudo shutdown -h now'
                #psShut = subprocess.Popen(
                #    [cmd],
                #    stdout = subprocess.PIPE,
                #    stderr = subprocess.PIPE,
                #    shell = True
                #)
                #out, err = psShut.communicate()

            time.sleep(1)
    except:
        print 'Error set default config'
        pi.stop()
        sys.exit(1)

if __name__ == '__main__':
    main()
