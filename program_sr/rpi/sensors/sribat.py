#!/usr/bin/env python
import os
import gc
import logging
import MySQLdb

class srIBat(object):
    def __init__(self):
        gc.enable()

    @staticmethod
    def get_kind():
        """
        return sensor kind
        """
        return "mpsribat"

    @staticmethod
    def get_sensordef(testing=False):
        """
        Definition of the sensor and data to be shown in the PRTG WebGUI
        """
        sensordefinition = {
            "kind": srIBat.get_kind(),
            "name": "SR Battery Current",
            "description": "Returns Battery Current",
            "default": "yes",
            "help": "Returns Battery Current",
            "tag": "mpsribat",
            "fields": [],
            "groups": []
        }
        return sensordefinition

    @staticmethod
    def get_data(data, out_queue):
        sribat = srIBat()
        try:
            sribatData = sribat.read_current(data)
            logging.debug("Running sensor: %s" % sribat.get_kind())
        except Exception as e:
            logging.error("Ooops Something went wrong with '%s' sensor %s. Error: %s" % (sribat.get_kind(),data['sensorid'],e))
            data = {
                "sensorid": int(data['sensorid']),
                "error": "Exception",
                "code": 1,
                "message": "IBat sensor failed. See log for details."
            }
            out_queue.put(data)
            return 1
        currentData = []
        for element in sribatData:
            currentData.append(element)
        data = {
            "sensorid": int(data['sensorid']),
            "message": "OK",
            "channel": currentData
        }
        del sribat
        gc.collect()
        out_queue.put(data)
        return 0

    @staticmethod
    def read_current(config):
        data = []
        chandata = []

        #Read from DB
        db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
        curs = db.cursor()
        cmd = "SELECT srIBat FROM sensorDataCurrent ORDER BY srIBat ASC LIMIT 1"
        curs.execute(cmd)
        value = curs.fetchone()
        db.close()
        data.append(value[0])

        for i in range(len(data)):
            chandata.append({"name": "Battery Current",
                             "mode": "float",
                             "unit": "Custom",
                             "customunit": "Amp",
                             "LimitMode": 1,
                             "LimitMaxError": 20.0,
                             "LimitMaxWarning": 15.0,
                             "value": float(data[i])})
        return chandata
