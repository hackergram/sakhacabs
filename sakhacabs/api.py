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

import json,datetime
#from flask.ext.potion.contrib.mongoengine.manager import MongoEngineManager
#from sakhacabs.xpal import *
from sakhacabs import xpal
# from sakhacabs import documents
app = Flask(__name__)
app.config.update(
    MONGODB_HOST = 'localhost',
    MONGODB_PORT = '27017',
    MONGODB_DB = 'sakhacabs',
)
CORS(app)
me = MongoEngine(app)
app.logger=xpal.sakhacabsxpal.logger

api = Api(app)
parser = reqparse.RequestParser()  


class DriverResource(Resource):
    def get(self,tgid=None,mobile_num=None,docid=None,driver_id=None, command=None):
		if command!=None:
			app.logger.info("BookingResource: Received Command {}".format(command))
			if command=="export":
				try:
					resp=xpal.export_drivers()
					status="success"
				except Exception as e:
					app.logger.error("{} {}".format(type(e),str(e)))
					resp="{} {}".format(type(e),str(e))
					status="error"	
			else:
				resp="Unrecognized command"
				status="error"	
		elif docid!=None:
			resp=[xpal.documents.documents.Driver.objects.with_id(docid)]
		elif tgid!=None:
			resp=xpal.documents.Driver.objects(tgid=tgid)
		elif mobile_num!=None:
			resp=xpal.documents.Driver.objects(mobile_num=mobile_num)
		elif driver_id!=None:
			resp=xpal.documents.Driver.objects(driver_id=driver_id)
		else:
			resp=xpal.documents.Driver.objects.all()
		if type(resp)==list and resp!=[]:
			status="success"
		else:
			status="error"
		return jsonify({"resp":resp,"status":status}) 
    def post(self, command=None):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		if command==None:
			try:
				if xpal.validate_driver_dict(respdict)['status']==True:
					resp=xpal.create_driver(respdict)
					if type(resp)!=list:
						status="error"
					else:
						status="success"
				else:
					status="error"
					resp=xpal.validate_driver_dict(respdict)['message']
			except Exception as e:
				app.logger.error("{} {}".format(type(e),str(e)))
				resp="{} {}".format(type(e),str(e))
				status="error"			
		else:
			resp="Unrecognized command"
			status="error"
		return jsonify({"resp":resp,"status":status}) 
    def put(self,driver_id):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		try:
			if xpal.validate_driver_dict(respdict,new=False)['status']==True:
				resp=xpal.update_driver(driver_id,respdict)
				if type(resp)!=list:
					status="error"
				else:
					status="success"
			else:
				status="error"
				resp=xpal.validate_driver_dict(respdict,new=False)['message']
		except Exception as e:
			app.logger.error("{} {}".format(type(e),str(e)))
			resp="{} {}".format(type(e),str(e))
			status="error"
		return jsonify({"resp":resp,"status":status}) 		
    def delete(self,driver_id=None):
		if driver_id==None:
			resp="No driver ID"
			status="error"
		else:
			app.logger.info("DriverResource: Trying to delete driver {}".format(driver_id))
			try:
				resp=xpal.delete_driver(driver_id)
				if type(resp)==list:
					status="success"
				else:
					status="error"
			except Exception as e:
				app.logger.error("{} {}".format(type(e),str(e)))
				resp="{} {}".format(type(e),str(e))
				status="error"
		return jsonify({"resp":resp,"status":status})
api.add_resource(DriverResource,"/driver",endpoint="driver")
api.add_resource(DriverResource,"/driver/by_tgid/<int:tgid>",endpoint="tgid")
api.add_resource(DriverResource,"/driver/by_mobile/<string:mobile_num>",endpoint="mobile")
api.add_resource(DriverResource,"/driver/by_id/<string:docid>",endpoint="driver_docid")
api.add_resource(DriverResource,"/driver/by_driver_id/<string:driver_id>",endpoint="driverid")
api.add_resource(DriverResource,"/driver/<string:command>",endpoint="driver_command")

class VehicleResource(Resource):
    def get(self,vehicle_id=None,docid=None,command=None):
        if command!=None:
			app.logger.info("BookingResource: Received Command {}".format(command))
			if command=="export":
				try:
					resp=xpal.export_vehicles()
					status="success"
				except Exception as e:
					app.logger.error("{} {}".format(type(e),str(e)))
					resp="{} {}".format(type(e),str(e))
					status="error"	
			else:
				resp="Unrecognized command"
				status="error"	
		
        elif docid!=None:
            resp=[xpal.documents.Vehicle.objects.with_id(docid)]
        elif vehicle_id!=None:
            resp=xpal.documents.Vehicle.objects(vehicle_id=vehicle_id)
        else:
            resp=xpal.documents.Vehicle.objects.all()
        if type(resp)==list and resp!=[]:
			status="success"
        else:
			status="error"
        return jsonify({"resp":resp,"status":status}) 
    def post(self,command=None):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		if command==None:
			try:
				if xpal.validate_vehicle_dict(respdict)['status']==True:
					resp=xpal.create_vehicle(respdict)
					if type(resp)!=list:
						status="error"
					else:
						status="success"
				else:
					status="error"
					resp=xpal.validate_vehicle_dict(respdict)['message']
			except Exception as e:
				app.logger.error("{} {}".format(type(e),str(e)))
				resp="{} {}".format(type(e),str(e))
				status="error"			
		else:
			resp="Unrecognized command"
			status="error"
		return jsonify({"resp":resp,"status":status}) 
    def put(self,vehicle_id=None):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		try:
			if xpal.validate_vehicle_dict(respdict,new=False)['status']==True:
				resp=xpal.update_vehicle(vehicle_id,respdict)
				if type(resp)!=list:
					status="error"
				else:
					status="success"
			else:
				status="error"
				resp=xpal.validate_vehicle_dict(respdict,new=False)['message']
		except Exception as e:
			app.logger.error("{} {}".format(type(e),str(e)))
			resp="{} {}".format(type(e),str(e))
			status="error"
		return jsonify({"resp":resp,"status":status})	
    def delete(self,vehicle_id=None):
		if vehicle_id==None:
			resp="No vehicle ID"
			status="error"
		else:
			app.logger.info("vehicleResource: Trying to delete vehicle {}".format(vehicle_id))
			try:
				resp=xpal.delete_vehicle(vehicle_id)
				if type(resp)==list:
					status="success"
				else:
					status="error"
			except Exception as e:
				app.logger.error("{} {}".format(type(e),str(e)))
				resp="{} {}".format(type(e),str(e))
				status="error"
		return jsonify({"resp":resp,"status":status})
api.add_resource(VehicleResource,"/vehicle",endpoint="vehicle")
api.add_resource(VehicleResource,"/vehicle/by_id/<string:docid>",endpoint="vehicle_docid")
api.add_resource(VehicleResource,"/vehicle/by_vehicle_id/<string:vehicle_id>",endpoint="vehicleid")
api.add_resource(VehicleResource,"/vehicle/<string:command>",endpoint="vehicle_command")

class LocationUpdateResource(Resource):
    def get(self,docid=None,command=None):
		if command!=None:
			app.logger.info("LocationUpdateResource: Received Command {}".format(command))
			if command=="export":
				try:
					resp=xpal.export_locupdates()
					status="success"
				except Exception as e:
					app.logger.error("{} {}".format(type(e),str(e)))
					resp="{} {}".format(type(e),str(e))
					status="error"	
			else:
				resp="Unrecognized command"
				status="error"	
		elif docid:
			resp=[xpal.documents.LocationUpdate.objects.with_id(docid)]
		else:
			resp=xpal.documents.LocationUpdate.objects.all()
		if type(resp)==list and resp !=[]:
			status="success"
		else:
			status="error"
		return jsonify({"resp":resp,"status":status})
    def post(self):
        app.logger.info("{}".format(request.get_json()))
        respdict=request.get_json()
        try:
			if xpal.validate_locupdate_dict(respdict)['status']==True:
				driver=xpal.documents.Driver.objects(driver_id=respdict["driver_id"])[0]
				timestamp=datetime.datetime.fromtimestamp(respdict['timestamp']['$date']/1000)
				if respdict["vehicle_id"]:
					vehicle=xpal.documents.Vehicle.objects(vehicle_id=respdict["vehicle_id"])[0]
				else:
					vehicle=None
				locupdate=new_locationupdate(driver,timestamp,vehicle=vehicle)
				#locupdate=xpal.documents.LocationUpdate.from_json(json.dumps(request.get_json()))
				app.logger.info("{}".format(locupdate.to_json()))
				locupdate.save()
				resp =[locupdate]
				status="success"
			else:
				resp=xpal.validate_locupdate_dict(respdict)['message']
				status="error"
        except Exception as e:
			app.logger.error("{} {}".format(type(e),str(e)))
			resp="{} {}".format(type(e),str(e))
			status="error"	
        return jsonify({"resp":resp,"status":status})
    def put(self,docid=None):
        app.logger.info("{} {}".format(docid,request.get_json()))
        respdict=request.get_json()
        if "_id" in respdict.keys():
            del respdict["_id"]
        if docid:
            if xpal.documents.LocationUpdate.objects.with_id(docid):
                try:
                    locupdate=xpal.documents.LocationUpdate.objects.with_id(docid)
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
		if len(xpal.documents.LocationUpdate.objects.with_id(docid))>0:
			xpal.documents.LocationUpdate.objects.with_id(docid).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})
api.add_resource(LocationUpdateResource,"/locupdate",endpoint="locupdate")
api.add_resource(LocationUpdateResource,"/locupdate/by_id/<string:docid>",endpoint="locupdate_docid")
api.add_resource(LocationUpdateResource,"/locupdate/<string:command>",endpoint="locupdate_command")

class BookingResource(Resource):
    def get(self,docid=None,booking_id=None,command=None):
		if command!=None:
			app.logger.info("BookingResource: Received Command {}".format(command))
			if command=="export":
				try:
					resp=xpal.export_bookings()
					status="success"
				except Exception as e:
					app.logger.error("{} {}".format(type(e),str(e)))
					resp="{} {}".format(type(e),str(e))
					status="error"	
			else:
				resp="Unrecognized command"
				status="error"	
		elif docid!=None:
			app.logger.info("BookingResource: Booking Get By Doc ID {}".format(docid))
			if xpal.documents.Booking.objects.with_id(docid):
				resp=json.loads(xpal.documents.Booking.objects.with_id(docid).to_json())
				status="success"
			else:
				resp="No booking with that id"
				status="error"
		elif booking_id!=None:
			app.logger.info("BookingResource: Booking Get By Booking ID {}".format(booking_id))
			if xpal.documents.Booking.objects(booking_id=booking_id)!=[]:
				resp=json.loads(xpal.documents.Booking.objects(booking_id=booking_id).to_json())
				status="success"
			else:
				resp="No booking with that id"
				status="error"
		else:
			app.logger.info("BookingResource: Getting all Bookings")
			resp=xpal.documents.Booking.objects.all()
			status="success"
		return jsonify({"resp":resp,"status":status})
    def post(self,command=None):	
		app.logger.info("BookingResource: {}".format(request.get_json()))
		respdict=request.get_json()
		app.logger.info("BookingResource: Received Command {}".format(command))
		if command=="single":
			app.logger.info("BookingResource: Trying to save single booking")
			if xpal.validate_booking_dict(respdict)['status']==True:
				try:
					resp=xpal.new_booking(respdict)
					if type(resp)!=list:
						status="error"
					else:
						status="success"
				except Exception as e:
					resp="{} {}".format(type(e),str(e))
					status="error"
				
			else:
				resp=xpal.validate_booking_dict(respdict)['message']
				status="error"
		elif command=="updatestatus":
				try:
					#TODO xpal.update_dutyslip_status(dsid), move to put and take dsid from by_id - needs fix in UI as well #82
					booking=xpal.documents.Booking.objects.with_id(respdict['booking_id'])
					booking.status=respdict['status']
					booking.save()
					resp="Status updated."
					status="success"
				except Exception as e:
					app.logger.error("{} {} \n {}".format(type(e),str(e),respdict))
					resp="{} {}".format(type(e),str(e))
					status="error"	
		elif command=="import":
			try:
				#replace with bookinglist=xpal.importbookings(respdict) #91 #83
				resp=xpal.import_bookings(respdict)
				if type(resp)!=list:
					status="error"
				else:
					status="success"
			except Exception as e:
				resp="{} {}".format(type(e),str(e))
				status="error"
		else:	
			resp="Unrecognized command or no provided"
			status="success"
		return jsonify({"resp":resp,"status":status})	
    def put(self,booking_id=None):
		#PUT to /booking/by_booking_id/<booking_id>
        #Training Note: If more than one booking is linked in an assignment, the assignment reporting time will reflect that of the last updated booking. If something else is needed best to delete the assignment and create a new one. 
        if booking_id==None:
			resp="No booking id provided"
			status="error"
        else:
			app.logger.info("Trying to update booking id {} with data {}".format(booking_id,request.get_json()))
			respdict=request.get_json()
			if xpal.validate_booking_dict(respdict, new=False)['status']==True:
				try:
					resp=xpal.update_booking(booking_id,respdict)
					if type(resp)!=list:
						status="error"
					else:
						status="success"
				except Exception as e:
					resp="{} {}".format(type(e),str(e))
					status="error"
			else:
				resp=xpal.validate_booking_dict(respdict,new=False)['message']
				status="error"
        return jsonify({"resp":resp,"status":status})  
    def delete(self,booking_id=None):
		if booking_id==None:
			resp="No booking id provided"
			status="error"
		else:
			app.logger.info("Trying to delete booking id {}".format(booking_id))
			try:
				resp=xpal.delete_booking(booking_id)
				if type(resp)!=list:
					status="error"
				else:
					status="success"
			except Exception as e:
				resp="{} {}".format(type(e),str(e))
				status="error"
		return jsonify({"resp":resp,"status":status})
api.add_resource(BookingResource,"/booking",endpoint="booking")
api.add_resource(BookingResource,"/booking/by_id/<string:docid>",endpoint="booking_docid")
api.add_resource(BookingResource,"/booking/by_booking_id/<string:booking_id>",endpoint="booking_id")
api.add_resource(BookingResource,"/booking/<string:command>",endpoint="booking_command")

class AssignmentResource(Resource):
    def get(self,docid=None):
        if docid!=None:
			app.logger.info("AssignmentResource: Getting assignment with id {}".format(docid))
			queryset=[xpal.documents.Assignment.objects.with_id(docid)]
			#app.logger.info("Getting assignment {}".format(queryset))
        else:
			app.logger.info("AssignmentResource: Getting all assignments")
			queryset=xpal.documents.Assignment.objects.order_by("reporting_timestamp").all()
        try:
			app.logger.info("AssignmentResource: Trying to fill dutyslips in assignments")
			assignmentlist=[]
			for assignment in queryset:
				assignmentdict={}
				assignmentdict['assignment']=json.loads(assignment.to_json())
				assignmentdict['dutyslips']=json.loads(xpal.documents.DutySlip.objects(assignment=assignment).to_json())
				assignmentlist.append(assignmentdict)
			#return jsonify({"resp": json.loads(queryset.to_json())})
			resp=assignmentlist
			status="success"
        except Exception as e:
			app.logger.error("{} {}".format(type(e),str(e)))
			resp="{} {}".format(type(e),str(e))
			status="error"
        return jsonify({"resp": resp,"status":status})
    def post(self,command=None):
        app.logger.info("AssignmentResource: {}".format(request.get_json()))
        respdict=request.get_json()
        if command==None:
			app.logger.info("AssignmentResource: Trying to create new assignment")
			try:
				bookings=[xpal.documents.Booking.objects.with_id(x['_id']['$oid']) for x in respdict['assignment']['bookings']]
				respdict['assignment']['cust_id']=bookings[0].cust_id
				if xpal.validate_assignment_dict(respdict)['status']==True:
					resp=xpal.save_assignment(respdict)
					status="success"
					#return jsonify({"resp": [json.loads(assignment.to_json())],"status":"success"})
				else:
					resp=xpal.validate_assignment_dict(respdict)['message']
					status="error"
			except Exception as e:
				app.logger.error("{} {} \n {}".format(type(e),str(e),respdict))
				resp="{} {}".format(type(e),str(e))
				status="error"
        elif command=="updatestatus":
			app.logger.info("AssignmentResource: Trying to update assignment status")
			try:
				assignment=xpal.documents.Assignment.objects.with_id(respdict['assignment_id'])
				assignment.status=respdict['status']
				assignment.save()
				for booking in assignment.bookings:
					booking.status=assignment.status
					booking.save()
				resp="Status updated successfully"
				status="success"
				#return jsonify({"resp": "Status updated.","status":"success"})
			except Exception as e:
				app.logger.error("{} {} \n {}".format(type(e),str(e),respdict))
				resp="{} {}".format(type(e),str(e))
				status="error"	
        elif command=="search":
			app.logger.info("AssignmentResource: Searching assignments")
			try:
				search_keys=respdict
				date_frm=None
				date_to=None
				cust_id=None
				app.logger.info(search_keys)
				if "date_frm" in search_keys and search_keys['date_frm']!="":
					date_frm=datetime.datetime.strptime(search_keysr['date_frm'],"%Y-%m-%d %H:%M:%S")
				if "date_to" in search_keys and search_keys['date_to']!="":
					date_to=datetime.datetime.strptime(search_keys['date_to'],"%Y-%m-%d %H:%M:%S")
				if "cust_id" in search_keys and search_keys['cust_id']!="0":
					cust_id=search_keys['cust_id']
				queryset=xpal.search_assignments(cust_id=cust_id,date_frm=date_frm,date_to=date_to)
				assignmentlist=[]
				app.logger.info(queryset)
				for assignment in queryset:
					assignmentdict={}
					assignmentdict['assignment']=json.loads(assignment.to_json())
					assignmentdict['dutyslips']=json.loads(xpal.documents.DutySlip.objects(assignment=assignment).to_json())
					assignmentlist.append(assignmentdict)
				resp=assignmentlist
				status="success"
			except Exception as e:
				app.logger.error("{} {} \n {}".format(type(e),str(e),respdict))
				resp="{} {}".format(type(e),str(e))
				status="error"        
        return jsonify({"resp":resp,"status":status})
    def delete(self,docid=None):
		if docid==None:
			resp="No assignment ID"
			status="error"
		else:
			app.logger.info("AssignmentResource: Trying to delete assignment {}".format(docid))
			try:
				resp=xpal.delete_assignment(docid)
				if type(resp)==list:
					status="success"
				else:
					status="error"
			except Exception as e:
				app.logger.error("{} {}".format(type(e),str(e)))
				resp="{} {}".format(type(e),str(e))
				status="error"
		return jsonify({"resp":resp,"status":status})
api.add_resource(AssignmentResource,"/assignment",endpoint="assignment")
api.add_resource(AssignmentResource,"/assignment/by_id/<string:docid>",endpoint="assignment_docid")
api.add_resource(AssignmentResource,"/assignment/<string:command>",endpoint="assignment_command")

class DutySlipResource(Resource):
    def get(self,docid=None,assignment_id=None,driver_id=None):
        if docid!=None:
            resp=[xpal.documents.DutySlip.objects.with_id(docid)]
        elif assignment_id!=None:
			resp=xpal.documents.DutySlip.objects(assignment=xpal.documents.Assignment.objects.with_id(assignment_id))
        elif driver_id!=None:
            resp=xpal.documents.DutySlip.objects(driver=driver_id)
        else:
            resp=xpal.documents.DutySlip.objects.all()
        if resp==[]:
			status="error"
        else:
			status="success"
        return jsonify({"resp": resp,"status":status})
		
    def post(self,command=None):
        app.logger.info("{}".format(request.get_json()))
        respdict=request.get_json()
        if command=="updatestatus":
			try:
				dutyslip=xpal.documents.DutySlip.objects.with_id(respdict['dsid'])
				dutyslip.status=respdict['status']
				dutyslip.save()
				resp="Status updated."
				status="success"
			except Exception as e:
				app.logger.error("{} {} \n {}".format(type(e),str(e),respdict))
				resp="{} {}".format(type(e),str(e))
				status="error"	
        else:
			resp="Unrecognized command or no command provided"
			status="error"
        return jsonify({"resp": resp,"status":status})
    
    def put(self,docid):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		if "_id" in respdict.keys():
			del respdict['_id']
		if 'created_time' in respdict.keys():
			#respdict['created_time']=datetime.datetime.fromtimestamp(respdict['created_time']/1000)
			respdict.pop('created_time')
		'''	
		if 'open_time' in respdict.keys():
			#respdict['open_time']=datetime.datetime.fromtimestamp(respdict['open_time']/1000)
			app.logger.info("Type for open_time {}".format(type(respdict['open_time'])))
			if type(respdict['open_time'])==dict:
				respdict['open_time']=datetime.datetime.fromtimestamp(respdict['open_time']['$date']/1000)
			if type(respdict['open_time'])==unicode:
				respdict['open_time']=xpal.utils.get_utc_ts(datetime.datetime.strptime(respdict['open_time'],"%Y-%m-%d %H:%M:%S"))
			app.logger.info("Timestamp - {}".format(respdict['open_time']))
		if 'close_time' in respdict.keys():
			#respdict['close_time']=datetime.datetime.fromtimestamp(respdict['close_time']/1000)
			app.logger.info("Type for close_time {}".format(type(respdict['close_time'])))
			if type(respdict['close_time'])==dict:
				respdict['close_time']=datetime.datetime.fromtimestamp(respdict['close_time']['$date']/1000)
			if type(respdict['close_time'])==unicode:
				respdict['close_time']=xpal.utils.get_utc_ts(datetime.datetime.strptime(respdict['close_time'],"%Y-%m-%d %H:%M:%S"))
			app.logger.info("Timestamp - {}".format(respdict['close_time']))
		'''
		#TODO: dutyslip=xpal.update_dutyslip(docid,respdict) #82
		if xpal.validate_dutyslip_dict(respdict,False)['status']==True:
			try:
				resp=xpal.update_dutyslip(docid,respdict)
				if type(resp)==list:
					status="success"
				else:
					status="error"
			except Exception as e:
				app.logger.error("{} {} \n {}".format(type(e),str(e),respdict))
				resp="{} {}".format(type(e),str(e))
				status="error"        
		else:
			resp=xpal.validate_dutyslip_dict(respdict,False)['messages']
			status="error"
		return jsonify({"resp": resp,"status":status})

    def delete(self,docid):
		#TODO: xpal.delete_dutyslip(docid) for #82
		if docid==None:
			resp="No dutyslip ID"
			status="error"
		else:
			app.logger.info("DutySlipResource: Trying to delete dutyslip {}".format(docid))
			try:
				resp=xpal.delete_dutyslip(docid)
				if type(resp)==list:
					status="success"
				else:
					status="error"
			except Exception as e:
				app.logger.error("{} {}".format(type(e),str(e)))
				resp="{} {}".format(type(e),str(e))
				status="error"
		return jsonify({"resp":resp,"status":status})
api.add_resource(DutySlipResource,"/dutyslip",endpoint="dutyslip")
api.add_resource(DutySlipResource,"/dutyslip/by_id/<string:docid>",endpoint="dutyslip_docid")
api.add_resource(DutySlipResource,"/dutyslip/by_assignment_id/<string:assignment_id>",endpoint="dutyslip_assid")
api.add_resource(DutySlipResource,"/dutyslip/by_driver_id/<string:driver_id>",endpoint="dutyslip_driverid")
api.add_resource(DutySlipResource,"/dutyslip/<string:command>",endpoint="dutyslip_command")

class CustomerResource(Resource):
    def get(self,cust_id=None,docid=None,command=None):
        if command!=None:
			app.logger.info("BookingResource: Received Command {}".format(command))
			if command=="export":
				try:
					resp=xpal.export_customers()
					status="success"
				except Exception as e:
					app.logger.error("{} {}".format(type(e),str(e)))
					resp="{} {}".format(type(e),str(e))
					status="error"	
			else:
				resp="Unrecognized command"
				status="error"	
		
        elif docid!=None:
            resp=[xpal.documents.Customer.objects.with_id(docid)]
        elif cust_id!=None:
            resp=xpal.documents.Customer.objects(cust_id=cust_id)
        else:
            resp=xpal.documents.Customer.objects.all()
        if resp==[]:
			status="error"
        else:
			status="success"
        return jsonify({"resp":resp,"status":status}) 
    def post(self,command=None):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		if command==None:
			try:
				if xpal.validate_customer_dict(respdict)['status']==True:
					resp=xpal.create_customer(respdict)
					if type(resp)!=list:
						status="error"
					else:
						status="success"
				else:
					status="error"
					resp=xpal.validate_customer_dict(respdict)['message']
			except Exception as e:
				app.logger.error("{} {}".format(type(e),str(e)))
				resp="{} {}".format(type(e),str(e))
				status="error"			
		else:
			resp="Unrecognized command"
			status="error"
		return jsonify({"resp":resp,"status":status}) 
    def put(self,cust_id=None):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		try:
			if xpal.validate_customer_dict(respdict,new=False)['status']==True:
				resp=xpal.update_customer(cust_id,respdict)
				if type(resp)!=list:
					status="error"
				else:
					status="success"
			else:
				status="error"
				resp=xpal.validate_customer_dict(respdict,new=False)['message']
		except Exception as e:
			app.logger.error("{} {}".format(type(e),str(e)))
			resp="{} {}".format(type(e),str(e))
			status="error"
		return jsonify({"resp":resp,"status":status})	
    def delete(self,cust_id=None):
		if cust_id==None:
			resp="No customer ID"
			status="error"
		else:
			app.logger.info("customerResource: Trying to delete customer {}".format(cust_id))
			try:
				resp=xpal.delete_customer(cust_id)
				if type(resp)==list:
					status="success"
				else:
					status="error"
			except Exception as e:
				app.logger.error("{} {}".format(type(e),str(e)))
				resp="{} {}".format(type(e),str(e))
				status="error"
		return jsonify({"resp":resp,"status":status})
		
api.add_resource(CustomerResource,"/customer",endpoint="customer")
api.add_resource(CustomerResource,"/customer/by_tgid/<int:tgid>",endpoint="cust_tgid")
api.add_resource(CustomerResource,"/customer/by_mobile/<string:mobile_num>",endpoint="cust_mobile")
api.add_resource(CustomerResource,"/customer/by_id/<string:docid>",endpoint="customer_docid")
api.add_resource(CustomerResource,"/customer/by_cust_id/<string:cust_id>",endpoint="cust_id")

class ProductResource(Resource):
    def get(self,product_id=None,docid=None,command=None):
        if command!=None:
			app.logger.info("BookingResource: Received Command {}".format(command))
			if command=="export":
				try:
					resp=xpal.export_products()
					status="success"
				except Exception as e:
					app.logger.error("{} {}".format(type(e),str(e)))
					resp="{} {}".format(type(e),str(e))
					status="error"	
			else:
				resp="Unrecognized command"
				status="error"	
		
        elif docid!=None:
            resp=[xpal.documents.Product.objects.with_id(docid)]
        elif product_id!=None:
            resp=xpal.documents.Product.objects(product_id=product_id)
        else:
            resp=xpal.documents.Product.objects.all()
        if resp==[]:
			status="error"
        else:
			status="success"
        return jsonify({"resp":resp,"status":status})
    def post(self,command=None):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		if command==None:
			try:
				if xpal.validate_product_dict(respdict)['status']==True:
					resp=xpal.create_product(respdict)
					if type(resp)!=list:
						status="error"
					else:
						status="success"
				else:
					status="error"
					resp=xpal.validate_product_dict(respdict)['message']
			except Exception as e:
				app.logger.error("{} {}".format(type(e),str(e)))
				resp="{} {}".format(type(e),str(e))
				status="error"			
		else:
			resp="Unrecognized command"
			status="error"
		return jsonify({"resp":resp,"status":status}) 
    def put(self,product_id=None):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		try:
			if xpal.validate_product_dict(respdict,new=False)['status']==True:
				resp=xpal.update_product(product_id,respdict)
				if type(resp)!=list:
					status="error"
				else:
					status="success"
			else:
				status="error"
				resp=xpal.validate_product_dict(respdict,new=False)['message']
		except Exception as e:
			app.logger.error("{} {}".format(type(e),str(e)))
			resp="{} {}".format(type(e),str(e))
			status="error"
		return jsonify({"resp":resp,"status":status})	
    def delete(self,product_id=None):
		if product_id==None:
			resp="No product ID"
			status="error"
		else:
			app.logger.info("productResource: Trying to delete product {}".format(product_id))
			try:
				resp=xpal.delete_product(product_id)
				if type(resp)==list:
					status="success"
				else:
					status="error"
			except Exception as e:
				app.logger.error("{} {}".format(type(e),str(e)))
				resp="{} {}".format(type(e),str(e))
				status="error"
		return jsonify({"resp":resp,"status":status})
api.add_resource(ProductResource,"/product",endpoint="product")
api.add_resource(ProductResource,"/product/by_id/<string:docid>",endpoint="product_docid")
api.add_resource(ProductResource,"/product/by_product_id/<string:product_id>",endpoint="product_id")
api.add_resource(ProductResource,"/product/<string:command>",endpoint="product_command")

class InvoiceResource(Resource):
	def post(self):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		assignments=xpal.documents.Assignment.objects.filter(id__in=respdict)
		invoice=get_invoice(assignments)
	
		return jsonify({"resp":invoice,"status":"success"})
api.add_resource(InvoiceResource,"/invoice",endpoint="invoice")

if __name__ == '__main__':
   app.run(host="0.0.0.0")


