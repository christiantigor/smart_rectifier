#!/usr/bin/env python
import os
import gc
import logging
import MySQLdb

class srVBat(object):
    def __init__(self):
        gc.enable()

    @staticmethod
    def get_kind():
        """
        return sensor kind
        """
        return "mpsrvbat"

    @staticmethod
    def get_sensordef(testing=False):
        """
        Definition of the sensor and data to be shown in the PRTG WebGUI
        """
        sensordefinition = {
            "kind": srVBat.get_kind(),
            "name": "SR Battery Voltage",
            "description": "Returns Battery Voltage",
            "default": "yes",
            "help": "Returns Battery Voltage",
            "tag": "mpsrvbat",
            "fields": [],
            "groups": []
        }
        return sensordefinition

    @staticmethod
    def get_data(data, out_queue):
        srvbat = srVBat()
        try:
            srvbatData = srvbat.read_volt(data)
            logging.debug("Running sensor: %s" % srvbat.get_kind())
        except Exception as e:
            logging.error("Ooops Something went wrong with '%s' sensor %s. Error: %s" % (srvbat.get_kind(),data['sensorid'],e))
            data = {
                "sensorid": int(data['sensorid']),
                "error": "Exception",
                "code": 1,
                "message": "VBat sensor failed. See log for details."
            }
            out_queue.put(data)
            return 1
        voltData = []
        for element in srvbatData:
            voltData.append(element)
        data = {
            "sensorid": int(data['sensorid']),
            "message": "OK",
            "channel": voltData
        }
        del srvbat
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
        cmd = "SELECT srVBat FROM sensorDataCurrent ORDER BY srVBat ASC LIMIT 1"
        curs.execute(cmd)
        value = curs.fetchone()
        db.close()
        data.append(value[0])

        #Update data to NULL
        db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
        curs = db.cursor()
        with db:
            cmd = 'UPDATE sensorDataCurrent SET srVBat = NULL WHERE name = "currentData"'
            curs.execute(cmd)
        db.close()

        for i in range(len(data)):
            chandata.append({"name": "Battery Voltage",
                             "mode": "float",
                             "unit": "Custom",
                             "customunit": "Volt",
                             "LimitMode": 1,
                             "LimitMaxError": 70.0,
                             "LimitMaxWarning": 50.0,
                             "LimitMinWarning": 40.0,
                             "LimitMinError": 30.0,
                             "value": float(data[i])})
        return chandata
