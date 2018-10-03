#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:54:42 2018

@author: arjun
"""
from flask import Flask, jsonify,request
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_restful import reqparse, abort, Api, Resource
import json
#from flask.ext.potion.contrib.mongoengine.manager import MongoEngineManager
from sakhacabs.xpal import *
# from sakhacabs import documents
app = Flask(__name__)
app.config.update(
    MONGODB_HOST = 'localhost',
    MONGODB_PORT = '27017',
    MONGODB_DB = 'sakhacabs',
)
CORS(app)
me = MongoEngine(app)
app.logger=sakhacabsxpal.logger

api = Api(app)
parser = reqparse.RequestParser()  

class DriverResource(Resource):
    def get(self,tgid=None,mobile_num=None,docid=None,driver_id=None):
        if docid:
            if documents.Driver.objects.with_id(docid):
                return jsonify({"resp": [json.loads(documents.Driver.objects.with_id(docid).to_json())]})
            else:
                return jsonify({"resp":[]})
        elif tgid:
            return jsonify({"resp": json.loads(documents.Driver.objects(tgid=tgid).to_json())})
        elif mobile_num:
            return jsonify({"resp": json.loads(documents.Driver.objects(mobile_num=mobile_num).to_json())})
        elif driver_id:
            return jsonify({"resp": json.loads(documents.Driver.objects(driver_id=driver_id).to_json())})
        else:
            return jsonify({"resp": json.loads(documents.Driver.objects.to_json())})
api.add_resource(DriverResource,"/driver",endpoint="driver")
api.add_resource(DriverResource,"/driver/by_tgid/<int:tgid>",endpoint="tgid")
api.add_resource(DriverResource,"/driver/by_mobile/<string:mobile_num>",endpoint="mobile")
api.add_resource(DriverResource,"/driver/by_id/<string:docid>",endpoint="driver_docid")
api.add_resource(DriverResource,"/driver/by_driver_id/<string:driver_id>",endpoint="driverid")

class VehicleResource(Resource):
    def get(self,vehicle_id=None,docid=None):
        if docid:
            if documents.Vehicle.objects.with_id(docid):
                return jsonify({"resp": [json.loads(documents.Vehicle.objects.with_id(docid).to_json())]})
            else:
                return jsonify({"resp":[]})
        elif vehicle_id:
            return jsonify({"resp": json.loads(documents.Vehicle.objects(vehicle_id=vehicle_id).to_json())})
        else:
            return jsonify({"resp": json.loads(documents.Vehicle.objects.to_json())})
api.add_resource(VehicleResource,"/vehicle",endpoint="vehicle")
api.add_resource(VehicleResource,"/vehicle/by_id/<string:docid>",endpoint="vehicle_docid")
api.add_resource(VehicleResource,"/vehicle/by_vehicle_id/<string:vehicle_id>",endpoint="vehicleid")

class LocationUpdateResource(Resource):
    def get(self,docid=None):
        if docid:
            if documents.LocationUpdate.objects.with_id(docid):
                return jsonify({"resp": [json.loads(documents.LocationUpdate.objects.with_id(docid).to_json())]})
            else:
                return jsonify({"resp":[]})   
        else:
            return jsonify({"resp": json.loads(documents.LocationUpdate.objects.to_json())})
    def post(self):
        app.logger.info("{}".format(request.get_json().keys()))
        respdict=request.get_json()
        try:
            driver=documents.Driver.objects(driver_id=respdict["driver_id"])[0]
            timestamp=datetime.datetime.fromtimestamp(respdict['timestamp']['$date']/1000)
            if respdict["vehicle_id"]:
                vehicle=documents.Vehicle.objects(vehicle_id=respdict["vehicle_id"])[0]
            else:
                vehicle=None
            locupdate=new_locationupdate(driver,timestamp,vehicle=vehicle)
            #locupdate=documents.LocationUpdate.from_json(json.dumps(request.get_json()))
            app.logger.info("{}".format(locupdate.to_json()))
            locupdate.save()
            return jsonify({"resp": [json.loads(locupdate.to_json())]})
        except Exception as e:
            app.logger.info("{}".format(str(e)))
            return jsonify({"resp":[]})   
        #args = parser.parse_args()
        #app.logger.info("{}".format(args))
        #todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        #todo_id = 'todo%i' % todo_id
        #TODOS[todo_id] = {'task': args['task']}
        #return TODOS[todo_id], 201    
        return "{}"
     
    def put(self,docid=None):
        app.logger.info("{} {}".format(docid,request.get_json()))
        respdict=request.get_json()
        if "_id" in respdict.keys():
            del respdict["_id"]
        if docid:
            if documents.LocationUpdate.objects.with_id(docid):
                try:
                    locupdate=documents.LocationUpdate.objects.with_id(docid)
                    locupdate=locupdate.from_json(json.dumps(request.get_json()))
                    app.logger.info("{}".format(locupdate.to_json()))
                    locupdate.save()
                    return jsonify({"resp": [json.loads(locupdate.to_json())]})
                except Exception as e:
                    app.logger.info("{}".format(str(e)))
                    return jsonify({"resp":[]})   
            else:
                return jsonify({"resp":[]})   
        else:
            return jsonify({"resp":[]})   
        #args = parser.parse_args()
        #app.logger.info("{}".format(args))
        #todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        #todo_id = 'todo%i' % todo_id
        #TODOS[todo_id] = {'task': args['task']}
        #return TODOS[todo_id], 201    
        
api.add_resource(LocationUpdateResource,"/locupdate",endpoint="locupdate")
api.add_resource(LocationUpdateResource,"/locupdate/by_id/<string:docid>",endpoint="locupdate_docid")

class BookingResource(Resource):
    def get(self,docid=None):
        if docid:
            if documents.Booking.objects.with_id(docid):
                return jsonify({"resp": [json.loads(documents.Booking.objects.with_id(docid).to_json())]})
            else:
                return jsonify({"resp":[]})
       
        else:
            return jsonify({"resp": json.loads(documents.Booking.objects.to_json())})
api.add_resource(BookingResource,"/booking",endpoint="booking")
api.add_resource(BookingResource,"/booking/by_id/<string:docid>",endpoint="booking_docid")

