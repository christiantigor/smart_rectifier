#!/usr/bin/python

import MySQLdb

#Read from DB
db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
curs = db.cursor()
cmd = "SELECT srMdm3 FROM sensorDataCurrent ORDER BY srTemp ASC LIMIT 1"
curs.execute(cmd)
value = curs.fetchone()
db.close()
print value[0]*1000
