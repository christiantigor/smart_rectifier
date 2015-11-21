#!/usr/bin/env python
import os
import gc
import logging
import MySQLdb

class srTemp(object):
    def __init__(self):
        gc.enable()

    @staticmethod
    def get_kind():
        """
        return sensor kind
        """
        return "mpsrtemp"

    @staticmethod
    def get_sensordef(testing=False):
        """
        Definition of the sensor and data to be shown in the PRTG WebGUI
        """
        sensordefinition = {
            "kind": srTemp.get_kind(),
            "name": "SR Temperature",
            "description": "Returns Temperature",
            "default": "yes",
            "help": "Returns Temperature",
            "tag": "mpsrtemp",
            "fields": [],
            "groups": []
        }
        return sensordefinition

    @staticmethod
    def get_data(data, out_queue):
        srtemp = srTemp()
        try:
            srtempData = srtemp.read_volt(data)
            logging.debug("Running sensor: %s" % srtemp.get_kind())
        except Exception as e:
            logging.error("Ooops Something went wrong with '%s' sensor %s. Error: %s" % (srtemp.get_kind(),data['sensorid'],e))
            data = {
                "sensorid": int(data['sensorid']),
                "error": "Exception",
                "code": 1,
                "message": "Temp sensor failed. See log for details."
            }
            out_queue.put(data)
            return 1
        tempData = []
        for element in srtempData:
            tempData.append(element)
        data = {
            "sensorid": int(data['sensorid']),
            "message": "OK",
            "channel": tempData
        }
        del srtemp
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
        cmd = "SELECT srTemp FROM sensorDataCurrent ORDER BY srTemp ASC LIMIT 1"
        curs.execute(cmd)
        value = curs.fetchone()
        db.close()
        data.append(value[0])

        #Update data to NULL
        db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
        curs = db.cursor()
        with db:
            cmd = 'UPDATE sensorDataCurrent SET srTemp = NULL WHERE name = "currentData"'
            curs.execute(cmd)
        db.close()

        for i in range(len(data)):
            chandata.append({"name": "Temperature",
                             "mode": "float",
                             "unit": "Custom",
                             "customunit": "C",
                             "LimitMode": 1,
                             "LimitMaxError": 90.0,
                             "LimitMaxWarning": 80.0,
                             "value": float(data[i])})
        return chandata
