#!/usr/bin/env python
import os
import gc
import logging
import MySQLdb

class srMdmType(object):
    def __init__(self):
        gc.enable()

    @staticmethod
    def get_kind():
        """
        return sensor kind
        """
        return "mpsrmdmtype"

    @staticmethod
    def get_sensordef(testing=False):
        """
        Definition of the sensor and data to be shown in the PRTG WebGUI
        """
        sensordefinition = {
            "kind": srMdmType.get_kind(),
            "name": "SR Modem Type",
            "description": "Returns Modem Type",
            "default": "yes",
            "help": "Returns Modem Type",
            "tag": "mpsrmdmtype",
            "fields": [],
            "groups": []
        }
        return sensordefinition

    @staticmethod
    def get_data(data, out_queue):
        srmdmtype = srMdmType()
        try:
            srmdmtypeData = srmdmtype.read_modem_type(data)
            logging.debug("Running sensor: %s" % srmdmtype.get_kind())
        except Exception as e:
            logging.error("Ooops Something went wrong with '%s' sensor %s. Error: %s" % (srmdmtype.get_kind(),data['sensorid'],e))
            data = {
                "sensorid": int(data['sensorid']),
                "error": "Exception",
                "code": 1,
                "message": "Modem Type Sensor failed. See log for details."
            }
            out_queue.put(data)
            return 1
        modemType = []
        for element in srmdmtypeData:
            modemType.append(element)
        data = {
            "sensorid": int(data['sensorid']),
            "message": "OK",
            "channel": modemType
        }
        del srmdmtype
        gc.collect()
        out_queue.put(data)
        return 0

    @staticmethod
    def read_modem_type(config):
        data = []
        chandata = []

        #Read from DB
        db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
        curs = db.cursor()
        cmd = "SELECT mdmType FROM sensorDataCurrent ORDER BY mdmType ASC LIMIT 1"
        curs.execute(cmd)
        value = curs.fetchone()

        #Check value
        if value[0] == "NULL":
            data.append(0)
        else:
            data.append(1)

        db.close()

        #Update data to NULL
        db = MySQLdb.connect("localhost","monitor","1234","smartRectifier")
        curs = db.cursor()
        with db:
            cmd = 'UPDATE sensorDataCurrent SET mdmType = "NULL" WHERE name = "currentData"'
            curs.execute(cmd)
        db.close()

        for i in range(len(data)):
            chandata.append({"name": value[0],
                             "mode": "float",
                             "unit": "Custom",
                             "customunit": "Type",
                             "value": float(data[0])})
        return chandata
