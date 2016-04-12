#!/bin/bash
mysql -u monitor --password=1234 smartRectifier -e 'SELECT * FROM sensorDataHistory' > /home/pi/dev/sr/release/sensorDataHistory.txt
