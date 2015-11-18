#!/usr/bin/python

import re
import subprocess
import time

def main():
    #check chargerControl
    

    #check getSensorData
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
    

    #check PRTGMiniProbe
    cmd = 'sudo service prtgprobe status'
    psCheck = subprocess.Popen(
        [cmd],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = True
    )   
    out, err = psCheck.communicate()
    #print out
        
    if bool(re.search('failed!',out)):
        cmd = 'sudo service prtgprobe start'
        psRun = subprocess.Popen(
            [cmd],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell = True
        )
        out, err = psRun.communicate()
        print 'start prtgprobe'
    else:
        print 'prtgprobe is running'
    
    #check sendSensorData
    #check ledFlasher

if __name__ == '__main__':
    main()

