#!/usr/bin/python

import re
import subprocess
import time

def main():
    #check chargerControl
    cmd = 'ps aux | grep chargerControl.py | grep -v grep'
    psCheck = subprocess.Popen(
        [cmd],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = True
    )
    out, err = psCheck.communicate()

    if not bool(re.search('chargerControl.py',out)):
        cmd = 'python chargerControl.py'
        psRun = subprocess.Popen(
            [cmd],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )
        time.sleep(3)
        psRun.terminate()
        psRun.wait()
        print 'start chargerControl.py'
    else:
        print 'chargerControl.py is running'

    #Check getSensorData
    cmd = 'ps aux | grep getSensorData.py | grep -v grep'
    psCheck = subprocess.Popen(
        [cmd],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = True
    )
    out, err = psCheck.communicate()

    if not bool(re.search('getSensorData.py',out)):
        cmd = 'python getSensorData.py'
        psRun = subprocess.Popen(
            [cmd],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )
        time.sleep(3)
        psRun.terminate()
        psRun.wait()
        print 'start getSensorData.py'
    else:
        print 'getSensorData.py is running'

    #Check resetDevice
    cmd = 'ps aux | grep resetDevice.py | grep -v grep'
    psCheck = subprocess.Popen(
        [cmd],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = True
    )
    out, err = psCheck.communicate()

    if not bool(re.search('resetDevice.py',out)):
        cmd = 'python resetDevice.py'
        psRun = subprocess.Popen(
            [cmd],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )
        time.sleep(3)
        psRun.terminate()
        psRun.wait()
        print 'start resetDevice.py'
    else:
        print 'resetDevice.py is running'

if __name__ == '__main__':
    main()
