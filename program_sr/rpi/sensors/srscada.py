#!/usr/bin/env python
import os
import gc
import logging
import MySQLdb

class srSCADA(object):
    def __init__(self):
        gc.enable()

    @staticmethod
    def get_kind():
        """
        return sensor kind
        """
        return "mpsrscada"

    @staticmethod
    def get_sensordef(testing=False):
        """
        Definition of the sensor and data to be shown in the PRTG WebGUI
        """
        sensordefinition = {
            "kind": srSCADA.get_kind(),
            "name": "SR SCADA Voltage",
            "description": "Returns SCADA Voltage",
            "default": "yes",
            "help": "Returns SCADA Voltage",
            "tag": "mpsrscada",
            "fields": [],
            "groups": []
        }
        return sensordefinition

    @staticmethod
    def get_data(data, out_queue):
        srscada = srSCADA()
        try:
            srscadaData = srscada.read_volt(data)
            logging.debug("Running sensor: %s" % srscada.get_kind())
        except Exception as e:
            logging.error("Ooops Something went wrong with '%s' sensor %s. Error: %s" % (srscada.get_kind(),data['sensorid'],e))
            data = {
                "sensorid": int(data['sensorid']),
                "error": "Exception",
                "code": 1,
                "message": "SCADA sensor failed. See log for details."
            }
            out_queue.put(data)
            return 1
        voltData = []
        for element in srscadaData:
            voltData.append(element)
        data = {
            "sensorid": int(data['sensorid']),
            "message": "OK",
            "channel": voltData
        }
        del srscada
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
        cmd = "SELECT srSCADA FROM sensorDataCurrent ORDER BY srSCADA ASC LIMIT 1"
        curs.execute(cmd)
        value = curs.fetchone()
        db.close()
        data.append(value[0])

        #Update data to NULL
        db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
        curs = db.cursor()
        with db:
            cmd = 'UPDATE sensorDataCurrent SET srSCADA = NULL WHERE name = "currentData"'
            curs.execute(cmd)
        db.close()

        for i in range(len(data)):
            chandata.append({"name": "SCADA Voltage",
                             "mode": "float",
                             "unit": "Custom",
                             "customunit": "Volt",
                             "LimitMode": 1,
                             "LimitMaxError": 16.0,
                             "LimitMaxWarning": 14.0,
                             "LimitMinWarning": 10.0,
                             "LimitMinError": 8.0,
                             "value": float(data[i])})
        return chandata
