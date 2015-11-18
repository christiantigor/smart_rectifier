#!/usr/bin/env python
import os
import gc
import logging
import MySQLdb

class srBUC(object):
    def __init__(self):
        gc.enable()

    @staticmethod
    def get_kind():
        """
        return sensor kind
        """
        return "mpsrbuc"

    @staticmethod
    def get_sensordef(testing=False):
        """
        Definition of the sensor and data to be shown in the PRTG WebGUI
        """
        sensordefinition = {
            "kind": srBUC.get_kind(),
            "name": "SR BUC Voltage",
            "description": "Returns BUC Voltage",
            "default": "yes",
            "help": "Returns BUC Voltage",
            "tag": "mpsrbuc",
            "fields": [],
            "groups": []
        }
        return sensordefinition

    @staticmethod
    def get_data(data, out_queue):
        srbuc = srBUC()
        try:
            srbucData = srbuc.read_volt(data)
            logging.debug("Running sensor: %s" % srbuc.get_kind())
        except Exception as e:
            logging.error("Ooops Something went wrong with '%s' sensor %s. Error: %s" % (srbuc.get_kind(),data['sensorid'],e))
            data = {
                "sensorid": int(data['sensorid']),
                "error": "Exception",
                "code": 1,
                "message": "BUC sensor failed. See log for details."
            }
            out_queue.put(data)
            return 1
        voltData = []
        for element in srbucData:
            voltData.append(element)
        data = {
            "sensorid": int(data['sensorid']),
            "message": "OK",
            "channel": voltData
        }
        del srbuc
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
        cmd = "SELECT srBUC FROM sensorDataCurrent ORDER BY srBUC ASC LIMIT 1"
        curs.execute(cmd)
        value = curs.fetchone()
        db.close()
        data.append(value[0])

        for i in range(len(data)):
            chandata.append({"name": "BUC Voltage",
                             "mode": "float",
                             "unit": "Custom",
                             "customunit": "Volt",
                             "LimitMode": 1,
                             "LimitMaxError": 60.0,
                             "LimitMaxWarning": 50.0,
                             "LimitMinWarning": 30.0,
                             "LimitMinError": 20.0,
                             "value": float(data[i])})
        return chandata
