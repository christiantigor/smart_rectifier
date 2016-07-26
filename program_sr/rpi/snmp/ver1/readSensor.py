#!/usr/bin/python

#How to use this file
#python readSensor srVAC
#col as input argument
#if col is not defined, it will select srVAC

import MySQLdb
import sys
sys.path.append('/home/pi/tsr/release')
from tsrParams import *

try:
    col = sys.argv[1]
    if col in cols:
        pass
    else:
        col = 'srVAC'
except IndexError:
    col = 'srVAC'

#Construct cmd
cmd = "SELECT "+col+" FROM srCurrent WHERE id = 0"
#Read from DB
db = MySQLdb.connect("localhost","monitor","1234","srDB")
curs = db.cursor()
curs.execute(cmd)
value = curs.fetchone()
db.close()
print value[0]*1000
