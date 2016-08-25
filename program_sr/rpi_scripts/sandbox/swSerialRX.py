#!/usr/bin/python

import sys
import time
import pigpio

RXD = 15
baud = 57600
i = 0

try:
    pi = pigpio.pi()
    pi.set_mode(RXD,pigpio.INPUT)
    pi.bb_serial_read_open(RXD,baud,8)
    print "Receive - SW Serial"
    while 1:
        (count,data) = pi.bb_serial_read(RXD)
        if count:
            print "[%d]:\r\n" % i
            print data
            i += 1
        time.sleep(5)
except:
    pi.bb_serial_read_close(RXD)
    pi.stop()
    sys.exit(1)

