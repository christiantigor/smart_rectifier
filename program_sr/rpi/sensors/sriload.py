#!/usr/bin/env python
import os
import gc
import logging
import MySQLdb

class srILoad(object):
    def __init__(self):
        gc.enable()

    @staticmethod
    def get_kind():
        """
        return sensor kind
        """
        return "mpsriload"

    @staticmethod
    def get_sensordef(testing=False):
        """
        Definition of the sensor and data to be shown in the PRTG WebGUI
        """
        sensordefinition = {
            "kind": srILoad.get_kind(),
            "name": "SR Load Current",
            "description": "Returns Load Current",
            "default": "yes",
            "help": "Returns Load Current",
            "tag": "mpsriload",
            "fields": [],
            "groups": []
        }
        return sensordefinition

    @staticmethod
    def get_data(data, out_queue):
        sriload = srILoad()
        try:
            sriloadData = sriload.read_current(data)
            logging.debug("Running sensor: %s" % sriload.get_kind())
        except Exception as e:
            logging.error("Ooops Something went wrong with '%s' sensor %s. Error: %s" % (sriload.get_kind(),data['sensorid'],e))
            data = {
                "sensorid": int(data['sensorid']),
                "error": "Exception",
                "code": 1,
                "message": "ILoad sensor failed. See log for details."
            }
            out_queue.put(data)
            return 1
        currentData = []
        for element in sriloadData:
            currentData.append(element)
        data = {
            "sensorid": int(data['sensorid']),
            "message": "OK",
            "channel": currentData
        }
        del sriload
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
        cmd = "SELECT srILoad FROM sensorDataCurrent ORDER BY srILoad ASC LIMIT 1"
        curs.execute(cmd)
        value = curs.fetchone()
        db.close()
        data.append(value[0])

        #Update data to NULL
        db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
        curs = db.cursor()
        with db:
            cmd = 'UPDATE sensorDataCurrent SET srILoad = NULL WHERE name = "currentData"'
            curs.execute(cmd)
        db.close()

        for i in range(len(data)):
            chandata.append({"name": "Load Current",
                             "mode": "float",
                             "unit": "Custom",
                             "customunit": "Amp",
                             "LimitMode": 1,
                             "LimitMaxError": 20.0,
                             "LimitMaxWarning": 15.0,
                             "value": float(data[i])})
        return chandata
