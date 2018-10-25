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

#TODO - Testing - different scenarios
class DriverResource(Resource):
    def get(self,tgid=None,mobile_num=None,docid=None,driver_id=None):
        if docid:
            queryset=documents.Driver.objects.with_id(docid)
        elif tgid:
            queryset=documents.Driver.objects(tgid=tgid)
        elif mobile_num:
			queryset=documents.Driver.objects(mobile_num=mobile_num)
        elif driver_id:
            queryset=documents.Driver.objects(driver_id=driver_id)
        else:
            queryset=documents.Driver.objects.all()
        return jsonify({"resp":json.loads(queryset.to_json())}) 
    def post(self):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		if "_id" in respdict.keys():
			del respdict['_id']
		driver=documents.Driver.objects(driver_id=respdict['driver_id'])
		if len(driver)>0:
			driver=driver[0]
		else:
			driver=documents.Driver.from_json(json.dumps(respdict))
		driver.save()
		return jsonify({"resp":[driver]})
    def put(self,driver_id):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		driver=documents.Driver.objects(driver_id=driver_id)
		if len(driver)==0:
			return jsonify({"resp":[]})
		else:
			driver=driver[0]
		if "_id" in respdict.keys():
			del respdict['_id']
		if "driver_id" in respdict.keys():
			del respdict['driver_id']
		driver.update(**respdict)
		driver.save()
		driver.reload()
		return jsonify({"resp":[driver]})
    def delete(self,docid):
		if len(documents.Driver.objects.with_id(docid))>0:
			documents.Driver.objects.with_id(docid).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})
api.add_resource(DriverResource,"/driver",endpoint="driver")
api.add_resource(DriverResource,"/driver/by_tgid/<int:tgid>",endpoint="tgid")
api.add_resource(DriverResource,"/driver/by_mobile/<string:mobile_num>",endpoint="mobile")
api.add_resource(DriverResource,"/driver/by_id/<string:docid>",endpoint="driver_docid")
api.add_resource(DriverResource,"/driver/by_driver_id/<string:driver_id>",endpoint="driverid")

#TODO - Complete CRUD
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
    def post(self,vehicle_id=None,docid=None):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		return jsonify({"resp":[]})
    def put(self,vehicle_id=None,docid=None):
        return jsonify({"resp":[]})
	def delete(self,docid):
		if len(documents.Vehicle.objects.with_id(docid))>0:
			documents.Vehicle.objects.with_id(docid).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})
api.add_resource(VehicleResource,"/vehicle",endpoint="vehicle")
api.add_resource(VehicleResource,"/vehicle/by_id/<string:docid>",endpoint="vehicle_docid")
api.add_resource(VehicleResource,"/vehicle/by_vehicle_id/<string:vehicle_id>",endpoint="vehicleid")

#TODO - Location validatin and geocode lookup, handoff lookup
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
        app.logger.info("{}".format(request.get_json()))
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
    def delete(self,docid):
		if len(documents.LocationUpdate.objects.with_id(docid))>0:
			documents.LocationUpdate.objects.with_id(docid).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})
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
    def post(self):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		return jsonify({"resp":[]})
    def put(self,docid=None):
        return jsonify({"resp":[]})
    
    def delete(self,docid):
		if len(documents.Booking.objects.with_id(docid))>0:
			documents.Booking.objects.with_id(docid).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})
api.add_resource(BookingResource,"/booking",endpoint="booking")
api.add_resource(BookingResource,"/booking/by_id/<string:docid>",endpoint="booking_docid")

class AssignmentResource(Resource):
    def get(self,docid=None):
        if docid:
			queryset=documents.Assignment.objects.with_id(docid)
        else:
			queryset=documents.Assignment.objects.order_by("-created_timestamp").all()
        return jsonify({"resp": json.loads(queryset.to_json())})
    def post(self):
        app.logger.info("{}".format(request.get_json()))
        respdict=request.get_json()
        app.logger.info("")
        try:
            assignment=save_assignment(respdict)
            return jsonify({"resp": [json.loads(assignment.to_json())]})
        except Exception as e:
            app.logger.info("{}".format(str(e)))
            return jsonify({"resp":[]})   
        return jsonify({"resp":[]})
    def put(self,docid):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		try:
			assignment=save_assignment(respdict,docid)
			return jsonify({"resp": [json.loads(assignment.to_json())]})
		except Exception as e:
			app.logger.info("{}".format(str(e)))
			return jsonify({"resp":[]})   
		return jsonify({"resp":[]})
        
    def delete(self,docid):
		if len(documents.Assignment.objects.with_id(docid))>0:
			documents.Assignment.objects.with_id(docid).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})
api.add_resource(AssignmentResource,"/assignment",endpoint="assignment")
api.add_resource(AssignmentResource,"/assignment/by_id/<string:docid>",endpoint="assignment_docid")

class DutySlipResource(Resource):
    def get(self,docid=None,assignment_id=None,driver_id=None):
        if docid:
            if documents.DutySlip.objects.with_id(docid):
                return jsonify({"resp": [json.loads(documents.DutySlip.objects.with_id(docid).to_json())]})
            else:
                return jsonify({"resp":[]})
        elif assignment_id:
            if documents.DutySlip.objects(assignment=documents.Assignment.objects.with_id(assignment_id)):
                return jsonify({"resp": [json.loads(documents.DutySlip.objects(assignment=documents.Assignment.objects.with_id(assignment_id)).to_json())]})
            else:
                
                return jsonify({"resp":[]})
        elif driver_id:
            if documents.DutySlip.objects(driver=driver_id):
                return jsonify({"resp": [json.loads(documents.DutySlip.objects(driver=driver_id).to_json())]})
            else:
                return jsonify({"resp":[]})
        else:
            return jsonify({"resp": json.loads(documents.DutySlip.objects.to_json())})
    def delete(self,docid):
		if len(documents.DutySlip.objects.with_id(docid))>0:
			documents.DutySlip.objects.with_id(docid).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})

api.add_resource(DutySlipResource,"/dutyslip",endpoint="dutyslip")
api.add_resource(DutySlipResource,"/dutyslip/by_id/<string:docid>",endpoint="dutyslip_docid")
api.add_resource(DutySlipResource,"/dutyslip/by_assignment_id/<string:assignment_id>",endpoint="dutyslip_assid")
api.add_resource(DutySlipResource,"/dutyslip/by_driver_id/<string:driver_id>",endpoint="dutyslip_driverid")
