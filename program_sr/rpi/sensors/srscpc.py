#!/usr/bin/env python
import os
import gc
import logging
import MySQLdb

class srSCPC(object):
    def __init__(self):
        gc.enable()

    @staticmethod
    def get_kind():
        """
        return sensor kind
        """
        return "mpsrscpc"

    @staticmethod
    def get_sensordef(testing=False):
        """
        Definition of the sensor and data to be shown in the PRTG WebGUI
        """
        sensordefinition = {
            "kind": srSCPC.get_kind(),
            "name": "SR SCPC Voltage",
            "description": "Returns SCPC Voltage",
            "default": "yes",
            "help": "Returns SCPC Voltage",
            "tag": "mpsrscpc",
            "fields": [],
            "groups": []
        }
        return sensordefinition

    @staticmethod
    def get_data(data, out_queue):
        srscpc = srSCPC()
        try:
            srscpcData = srscpc.read_volt(data)
            logging.debug("Running sensor: %s" % srscpc.get_kind())
        except Exception as e:
            logging.error("Ooops Something went wrong with '%s' sensor %s. Error: %s" % (srscpc.get_kind(),data['sensorid'],e))
            data = {
                "sensorid": int(data['sensorid']),
                "error": "Exception",
                "code": 1,
                "message": "SCPC sensor failed. See log for details."
            }
            out_queue.put(data)
            return 1
        voltData = []
        for element in srscpcData:
            voltData.append(element)
        data = {
            "sensorid": int(data['sensorid']),
            "message": "OK",
            "channel": voltData
        }
        del srscpc
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
        cmd = "SELECT srSCPC FROM sensorDataCurrent ORDER BY srSCPC ASC LIMIT 1"
        curs.execute(cmd)
        value = curs.fetchone()
        db.close()
        data.append(value[0])

        for i in range(len(data)):
            chandata.append({"name": "SCPC Voltage",
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
