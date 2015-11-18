#!/usr/bin/env python
import os
import gc
import logging
import MySQLdb

class srMdm1(object):
    def __init__(self):
        gc.enable()

    @staticmethod
    def get_kind():
        """
        return sensor kind
        """
        return "mpsrmdm1"

    @staticmethod
    def get_sensordef(testing=False):
        """
        Definition of the sensor and data to be shown in the PRTG WebGUI
        """
        sensordefinition = {
            "kind": srMdm1.get_kind(),
            "name": "SR Modem Supply (13.5V)",
            "description": "Monitor 13.5V Supply",
            "default": "yes",
            "help": "Monitor 13.5V Supply",
            "tag": "mpsrmdm1",
            "fields": [],
            "groups": []
        }
        return sensordefinition

    @staticmethod
    def get_data(data, out_queue):
        srmdm1 = srMdm1()
        try:
            srmdm1Data = srmdm1.read_volt(data)
            logging.debug("Running sensor: %s" % srmdm1.get_kind())
        except Exception as e:
            logging.error("Ooops Something went wrong with '%s' sensor %s. Error: %s" % (srmdm1.get_kind(),data['sensorid'],e))
            data = {
                "sensorid": int(data['sensorid']),
                "error": "Exception",
                "code": 1,
                "message": "13.5V Supply Sensor failed. See log for details."
            }
            out_queue.put(data)
            return 1
        voltData = []
        for element in srmdm1Data:
            voltData.append(element)
        data = {
            "sensorid": int(data['sensorid']),
            "message": "OK",
            "channel": voltData
        }
        del srmdm1
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
        cmd = "SELECT srMdm1 FROM sensorDataCurrent ORDER BY srMdm1 ASC LIMIT 1"
        curs.execute(cmd)
        value = curs.fetchone()
        db.close()
        data.append(value[0])

        for i in range(len(data)):
            chandata.append({"name": "Modem Supply (13.5V)",
                             "mode": "float",
                             "unit": "Custom",
                             "customunit": "Volt",
                             "LimitMode": 1,
                             "LimitMaxError": 18.0,
                             "LimitMaxWarning": 16.0,
                             "LimitMinWarning": 12.0,
                             "LimitMinError": 10.0,
                             "value": float(data[i])})
        return chandata
