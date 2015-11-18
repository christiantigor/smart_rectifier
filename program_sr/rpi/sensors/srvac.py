#!/usr/bin/env python
import os
import gc
import logging
import MySQLdb

class srVAC(object):
    def __init__(self):
        gc.enable()

    @staticmethod
    def get_kind():
        """
        return sensor kind
        """
        return "mpsrvac"

    @staticmethod
    def get_sensordef(testing=False):
        """
        Definition of the sensor and data to be shown in the PRTG WebGUI
        """
        sensordefinition = {
            "kind": srVAC.get_kind(),
            "name": "SR AC Voltage",
            "description": "Returns AC Voltage",
            "default": "yes",
            "help": "Returns AC Voltage",
            "tag": "mpsrvac",
            "fields": [],
            "groups": []
        }
        return sensordefinition

    @staticmethod
    def get_data(data, out_queue):
        srvac = srVAC()
        try:
            srvacData = srvac.read_volt(data)
            logging.debug("Running sensor: %s" % srvac.get_kind())
        except Exception as e:
            logging.error("Ooops Something went wrong with '%s' sensor %s. Error: %s" % (srvac.get_kind(),data['sensorid'],e))
            data = {
                "sensorid": int(data['sensorid']),
                "error": "Exception",
                "code": 1,
                "message": "VAC sensor failed. See log for details."
            }
            out_queue.put(data)
            return 1
        voltData = []
        for element in srvacData:
            voltData.append(element)
        data = {
            "sensorid": int(data['sensorid']),
            "message": "OK",
            "channel": voltData
        }
        del srvac
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
        cmd = "SELECT srVAC FROM sensorDataCurrent ORDER BY srVAC ASC LIMIT 1"
        curs.execute(cmd)
        value = curs.fetchone()
        db.close()
        data.append(value[0])

        for i in range(len(data)):
            chandata.append({"name": "AC Voltage",
                             "mode": "float",
                             "unit": "Custom",
                             "customunit": "Volt",
                             "LimitMode": 1,
                             "LimitMaxError": 260.0,
                             "LimitMaxWarning": 240.0,
                             "LimitMinWarning": 200.0,
                             "LimitMinError": 180.0,
                             "value": float(data[i])})
        return chandata
