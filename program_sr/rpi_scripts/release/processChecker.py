#!/usr/bin/python

import re
import subprocess
import time

def main():
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

if __name__ == '__main__':
    main()
