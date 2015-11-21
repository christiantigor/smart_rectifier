#!/usr/bin/env python
import os
import gc
import logging
import MySQLdb

class srMdm0(object):
    def __init__(self):
        gc.enable()

    @staticmethod
    def get_kind():
        """
        return sensor kind
        """
        return "mpsrmdm0"

    @staticmethod
    def get_sensordef(testing=False):
        """
        Definition of the sensor and data to be shown in the PRTG WebGUI
        """
        sensordefinition = {
            "kind": srMdm0.get_kind(),
            "name": "SR Modem Supply (6.5V)",
            "description": "Monitor 6.5V Supply",
            "default": "yes",
            "help": "Monitor 6.5V Supply",
            "tag": "mpsrmdm0",
            "fields": [],
            "groups": []
        }
        return sensordefinition

    @staticmethod
    def get_data(data, out_queue):
        srmdm0 = srMdm0()
        try:
            srmdm0Data = srmdm0.read_volt(data)
            logging.debug("Running sensor: %s" % srmdm0.get_kind())
        except Exception as e:
            logging.error("Ooops Something went wrong with '%s' sensor %s. Error: %s" % (srmdm0.get_kind(),data['sensorid'],e))
            data = {
                "sensorid": int(data['sensorid']),
                "error": "Exception",
                "code": 1,
                "message": "6.5V Supply Sensor failed. See log for details."
            }
            out_queue.put(data)
            return 1
        voltData = []
        for element in srmdm0Data:
            voltData.append(element)
        data = {
            "sensorid": int(data['sensorid']),
            "message": "OK",
            "channel": voltData
        }
        del srmdm0
        gc.collect()
        out_queue.put(data)
        return 0

    @staticmethod
    def read_volt(config):
        data = []
        chandata = []

        #Read from DB
        db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
        curs = db.cursor()
        cmd = "SELECT srMdm0 FROM sensorDataCurrent ORDER BY srMdm0 ASC LIMIT 1"
        curs.execute(cmd)
        value = curs.fetchone()
        db.close()
        data.append(value[0])

        #Update data to NULL
        db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
        curs = db.cursor()
        with db:
            cmd = 'UPDATE sensorDataCurrent SET srMdm0 = NULL WHERE name = "currentData"'
            curs.execute(cmd)
        db.close()

        for i in range(len(data)):
            chandata.append({"name": "Modem Supply (6.5V)",
                             "mode": "float",
                             "unit": "Custom",
                             "customunit": "Volt",
                             "LimitMode": 1,
                             "LimitMaxError": 11.0,
                             "LimitMaxWarning": 9.0,
                             "LimitMinWarning": 5.0,
                             "LimitMinError": 3.0,
                             "value": float(data[i])})
        return chandata
