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
		if command=="export":
			fileloc=export_drivers()
			return jsonify({"resp":[fileloc],"status":"success"})
		if docid:
			queryset=xpal.documents.documents.Driver.objects.with_id(docid)
		elif tgid:
			queryset=xpal.documents.Driver.objects(tgid=tgid)
		elif mobile_num:
			queryset=xpal.documents.Driver.objects(mobile_num=mobile_num)
		elif driver_id:
			queryset=xpal.documents.Driver.objects(driver_id=driver_id)
		else:
			queryset=xpal.documents.Driver.objects
		return jsonify({"resp":json.loads(queryset.to_json()),"status":"success"}) 
    def post(self):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		if "_id" in respdict.keys():
			del respdict['_id']
		driver=xpal.documents.Driver.objects(driver_id=respdict['driver_id'])
		if len(driver)>0:
			driver=driver[0]
			return jsonify({"status":"error","resp":"Driver with that ID Exists"})
		else:
			if validate_driver_dict(respdict):
				driver=xpal.documents.Driver.from_json(json.dumps(respdict))
				driver.save()
				return jsonify({"status":"success","resp":[driver]})
			else:
				return jsonify({"status":"error","resp":"Invalid!"})
    def put(self,driver_id):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		driver=xpal.documents.Driver.objects(driver_id=driver_id)
		if len(driver)==0:
			return jsonify({"status":"error","resp":"No driver found"})
		else:
			driver=driver[0]
		if "_id" in respdict.keys():
			del respdict['_id']
		if "driver_id" in respdict.keys():
			if respdict['driver_id']!=driver_id:
				return jsonify({"status":"error","resp":"Driver ID mismatch"})
			del respdict['driver_id']
		driver.update(**respdict)
		driver.save()
		driver.reload()
		return jsonify({"status":"success","resp":[driver]})
    def delete(self,driver_id):
		if len(xpal.documents.Driver.objects(driver_id=driver_id))>0:
			xpal.documents.Driver.objects(driver_id=driver_id).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})
api.add_resource(DriverResource,"/driver",endpoint="driver")
api.add_resource(DriverResource,"/driver/by_tgid/<int:tgid>",endpoint="tgid")
api.add_resource(DriverResource,"/driver/by_mobile/<string:mobile_num>",endpoint="mobile")
api.add_resource(DriverResource,"/driver/by_id/<string:docid>",endpoint="driver_docid")
api.add_resource(DriverResource,"/driver/by_driver_id/<string:driver_id>",endpoint="driverid")
api.add_resource(DriverResource,"/driver/<string:command>",endpoint="driver_command")

class VehicleResource(Resource):
    def get(self,vehicle_id=None,docid=None,command=None):
        if command=="export":
			fileloc=export_vehicles()
			return jsonify({"resp":[fileloc],"status":"success"})
		
        if docid:
            if xpal.documents.Vehicle.objects.with_id(docid):
                return jsonify({"resp": [json.loads(xpal.documents.Vehicle.objects.with_id(docid).to_json())]})
            else:
                return jsonify({"resp":[]})
        elif vehicle_id:
            return jsonify({"resp": json.loads(xpal.documents.Vehicle.objects(vehicle_id=vehicle_id).to_json())})
        else:
            return jsonify({"resp": json.loads(xpal.documents.Vehicle.objects.to_json())})
    def post(self,vehicle_id=None,docid=None):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		return jsonify({"resp":[]})
    def put(self,vehicle_id=None,docid=None):
        return jsonify({"resp":[]})
	def delete(self,docid):
		if len(xpal.documents.Vehicle.objects.with_id(docid))>0:
			xpal.documents.Vehicle.objects.with_id(docid).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})
api.add_resource(VehicleResource,"/vehicle",endpoint="vehicle")
api.add_resource(VehicleResource,"/vehicle/by_id/<string:docid>",endpoint="vehicle_docid")
api.add_resource(VehicleResource,"/vehicle/by_vehicle_id/<string:vehicle_id>",endpoint="vehicleid")
api.add_resource(VehicleResource,"/vehicle/<string:command>",endpoint="vehicle_command")




class LocationUpdateResource(Resource):
    def get(self,docid=None,command=None):
		if command=="export":
			fileloc=export_locupdates()
			return jsonify({"resp":[fileloc],"status":"success"})
		if docid:
			if xpal.documents.LocationUpdate.objects.with_id(docid):
				return jsonify({"resp": [json.loads(xpal.documents.LocationUpdate.objects.with_id(docid).to_json())]})
			else:
				return jsonify({"resp":[]})
		else:
			return jsonify({"resp": json.loads(xpal.documents.LocationUpdate.objects.to_json())})
    def post(self):
        app.logger.info("{}".format(request.get_json()))
        respdict=request.get_json()
        try:
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
        if command=="export":
			fileloc=export_bookings()
			return jsonify({"resp":[fileloc],"status":"success"})
        if docid:
            if xpal.documents.Booking.objects.with_id(docid):
                return jsonify({"resp": [json.loads(xpal.documents.Booking.objects.with_id(docid).to_json())]})
            else:
                return jsonify({"resp":[]})
        if booking_id:
			if xpal.documents.Booking.objects(booking_id=booking_id):
				return jsonify({"resp": [json.loads(xpal.documents.Booking.objects(booking_id=booking_id).to_json())]})
			else:
				return jsonify({"resp":[]})
        else:
            return jsonify({"resp": json.loads(xpal.documents.Booking.objects.to_json())})
    def post(self,command=None):	
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		if command=="single":
			if xpal.validate_booking_dict(respdict):
				booking=xpal.new_booking(respdict)
				return jsonify({"resp":[booking],"status":"success"})
			else:
				return jsonify({"resp":"Invalid Input","status":"error"})
		if command=="import":
			bookinglist=xpal.import_gadv(respdict)
			return jsonify({"resp":bookinglist,"status":"success"})
		return jsonify({"resp":[]})
    def put(self,booking_id=None):
		#PUT to /booking/by_booking_id/<booking_id>
        #Training Note: If more than one booking is linked in an assignment, the assignment reporting time will reflect that of the last updated booking. If something else is needed best to delete the assignment and create a new one. 
        
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		if 'created_timestamp' in respdict.keys():
			respdict['created_timestamp']=datetime.datetime.fromtimestamp(respdict['created_timestamp']['$date']/1000)
		if 'pickup_timestamp' in respdict.keys():
			respdict['pickup_timestamp']=datetime.datetime.fromtimestamp(respdict['pickup_timestamp']['$date']/1000)
		if xpal.validate_booking_dict(respdict):
			resp=xpal.update_booking(booking_id,respdict)
		if type(resp)!=list:
			status="error"
		else:
			status="success"
		return jsonify({"resp":resp,"status":status})
    
    def delete(self,booking_id):
		if len(xpal.documents.Booking.objects(booking_id=booking_id))>0:
			#TODO: xpal.delete_booking(booking_id) #81
			xpal.documents.Booking.objects(booking_id=booking_id).delete()
			return jsonify({"resp":[],"status":"success"})
		else:
			return jsonify({"resp":[],"status":"error"})
api.add_resource(BookingResource,"/booking",endpoint="booking")
api.add_resource(BookingResource,"/booking/by_id/<string:docid>",endpoint="booking_docid")
api.add_resource(BookingResource,"/booking/by_booking_id/<string:booking_id>",endpoint="booking_id")
api.add_resource(BookingResource,"/booking/<string:command>",endpoint="booking_command")

class AssignmentResource(Resource):
    def get(self,docid=None):
        if docid:
			queryset=xpal.documents.Assignment.objects.with_id(docid)
			app.logger.info("Getting assignment {}".format(queryset))
        else:
			queryset=xpal.documents.Assignment.objects.order_by("reporting_timestamp").all()
        
        assignmentlist=[]
        for assignment in queryset:
			assignmentdict={}
			assignmentdict['assignment']=json.loads(assignment.to_json())
			assignmentdict['dutyslips']=json.loads(xpal.documents.DutySlip.objects(assignment=assignment).to_json())
			assignmentlist.append(assignmentdict)
        #return jsonify({"resp": json.loads(queryset.to_json())})
        return jsonify({"resp": assignmentlist,"status":"success"})
    def post(self,command=None):
        app.logger.info("{}".format(request.get_json()))
        respdict=request.get_json()
        if command=="updatestatus":
			assignment=xpal.documents.Assignment.objects.with_id(respdict['assignment_id'])
			assignment.status=respdict['status']
			assignment.save()
			for booking in assignment.bookings:
				booking.status=assignment.status
				booking.save()
			return jsonify({"resp": "Status updated.","status":"success"})	
        if command=="search":
			search_keys=respdict
			date_frm=None
			date_to=None
			cust_id=None
			app.logger.info(search_keys)
			if "date_frm" in search_keys and search_keys['date_frm']!="":
				date_frm=datetime.datetime.strptime(search_keys['date_frm'],"%Y-%m-%d %H:%M:%S")
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
			return jsonify({"resp": assignmentlist	,"status":"success"})
        app.logger.info("Validating assignmentdict")
        if respdict['dutyslips']==[]:
				return jsonify({"resp": "At least one driver must be assigned to create an assignment.","status":"error"})
        if respdict['assignment']['bookings']==[]:
				return jsonify({"resp": "At least one booking must be assigned to create an assignment.","status":"error"})
        bookings=[xpal.documents.Booking.objects.with_id(x['_id']['$oid']) for x in respdict['assignment']['bookings']]
        respdict['assignment']['cust_id']=bookings[0].cust_id
        for booking in bookings:
			if hasattr(booking,"assignment"):
				return jsonify({"resp": "Booking is already assigned! Please delete the old assignment before creating a new one.","status":"error"}) 
			if booking.cust_id!=respdict['assignment']['cust_id']:
				return jsonify({"resp": "Bookings from different customers cannot be assigned together.","status":"error"}) 
        seenvehicles=[]
        for dutyslip in respdict['dutyslips']:
			if "vehicle" in dutyslip.keys():
				if dutyslip['vehicle'] in seenvehicles:
					return jsonify({"resp": "Can't assign the same vehicle to more than one driver in the same assignment.","status":"error"}) 
				seenvehicles.append(dutyslip['vehicle'])
				
        try:
            assignment=xpal.save_assignment(respdict)
            return jsonify({"resp": [json.loads(assignment.to_json())],"status":"success"})
        except Exception as e:
            app.logger.error("{} {} \n {}".format(type(e),str(e),respdict))
            return jsonify({"resp":"Saving assignment failed","status":"error"})   
        return jsonify({"resp":[]})
    def put(self,docid):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		try:
			assignment=xpal.save_assignment(respdict,docid)
			return jsonify({"resp": [json.loads(assignment.to_json())]})
		except Exception as e:
			app.logger.info("{}".format(str(e)))
		return jsonify({"resp":"Error creating assignment!","status":"error"})   
		
    def delete(self,docid):
		if len(xpal.documents.Assignment.objects.with_id(docid))>0:
			dutyslips=xpal.documents.DutySlip.objects(assignment=xpal.documents.Assignment.objects.with_id(docid))
			app.logger.info("Deleting DutySlips {}".format(dutyslips.to_json()))
			dutyslips.delete()
			bookings=xpal.documents.Booking.objects(assignment=docid)
			app.logger.info("Removing Assignment reference from  Bookings {}".format(bookings.to_json()))
			
			for booking in bookings:
				del(booking.assignment)
				booking.save()
			xpal.documents.Assignment.objects.with_id(docid).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})
api.add_resource(AssignmentResource,"/assignment",endpoint="assignment")
api.add_resource(AssignmentResource,"/assignment/by_id/<string:docid>",endpoint="assignment_docid")
api.add_resource(AssignmentResource,"/assignment/<string:command>",endpoint="assignment_command")

class DutySlipResource(Resource):
    def get(self,docid=None,assignment_id=None,driver_id=None):
        if docid:
            if xpal.documents.DutySlip.objects.with_id(docid):
                return jsonify({"resp": [json.loads(xpal.documents.DutySlip.objects.with_id(docid).to_json())]})
            else:
                return jsonify({"resp":[]})
        elif assignment_id:
            if xpal.documents.DutySlip.objects(assignment=xpal.documents.Assignment.objects.with_id(assignment_id)):
                return jsonify({"resp": [json.loads(xpal.documents.DutySlip.objects(assignment=xpal.documents.Assignment.objects.with_id(assignment_id)).to_json())]})
            else:
                
                return jsonify({"resp":[]})
        elif driver_id:
            if xpal.documents.DutySlip.objects(driver=driver_id):
                return jsonify({"resp": [json.loads(xpal.documents.DutySlip.objects(driver=driver_id).to_json())]})
            else:
                return jsonify({"resp":[]})
        else:
            return jsonify({"resp": json.loads(xpal.documents.DutySlip.objects.to_json())})
    
    def post(self,command=None):
        app.logger.info("{}".format(request.get_json()))
        respdict=request.get_json()
        if command=="updatestatus":
			#TODO xpal.update_dutyslip_status(dsid), move to put and take dsid from by_id - needs fix in UI as well #82
			dutyslip=xpal.documents.DutySlip.objects.with_id(respdict['dsid'])
			dutyslip.status=respdict['status']
			dutyslip.save()
			return jsonify({"resp": "Status updated.","status":"success"})	
    
    
    def put(self,docid):
		
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		if "_id" in respdict.keys():
			del respdict['_id']
		if 'created_time' in respdict.keys():
			respdict['created_time']=datetime.datetime.fromtimestamp(respdict['created_time']/1000)
		if 'open_time' in respdict.keys():
			respdict['open_time']=datetime.datetime.fromtimestamp(respdict['open_time']/1000)
		if 'close_time' in respdict.keys():
			respdict['close_time']=datetime.datetime.fromtimestamp(respdict['close_time']/1000)
		#TODO: dutyslip=xpal.update_dutyslip(docid,respdict) #82
		dutyslip=xpal.documents.DutySlip.objects.with_id(docid)
		app.logger.info(dutyslip.to_json())
		if dutyslip==None:
			return jsonify({"status":"error","resp":"No dutyslip found"})
		dutyslip.update(**respdict)
		dutyslip.save()
		dutyslip.reload()
		return jsonify({"status":"success","resp":[dutyslip]})
    

    def delete(self,docid):
		#TODO: xpal.delete_dutyslip(docid) for #82
		if len(xpal.documents.DutySlip.objects.with_id(docid))>0:
			xpal.documents.DutySlip.objects.with_id(docid).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})
api.add_resource(DutySlipResource,"/dutyslip",endpoint="dutyslip")
api.add_resource(DutySlipResource,"/dutyslip/by_id/<string:docid>",endpoint="dutyslip_docid")
api.add_resource(DutySlipResource,"/dutyslip/by_assignment_id/<string:assignment_id>",endpoint="dutyslip_assid")
api.add_resource(DutySlipResource,"/dutyslip/by_driver_id/<string:driver_id>",endpoint="dutyslip_driverid")
api.add_resource(DutySlipResource,"/dutyslip/<string:command>",endpoint="dutyslip_command")

class CustomerResource(Resource):
    def get(self,tgid=None,mobile_num=None,docid=None,cust_id=None):
        if docid:
            queryset=xpal.documents.Customer.objects.with_id(docid)
        elif tgid:
            queryset=xpal.documents.Customer.objects(tgid=tgid)
        elif mobile_num:
			queryset=xpal.documents.Customer.objects(mobile_num=mobile_num)
        elif cust_id:
            queryset=xpal.documents.Customer.objects(cust_id=cust_id)
        else:
            queryset=xpal.documents.Customer.objects
        return jsonify({"resp":json.loads(queryset.to_json()),"status":"success"}) 
    def post(self):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		if "_id" in respdict.keys():
			del respdict['_id']
		customer=xpal.documents.Customer.objects(cust_id=respdict['cust_id'])
		if len(customer)>0:
			customer=customer[0]
			return jsonify({"status":"error","resp":"Customer with that ID Exists"})
		else:
			customer=xpal.documents.Customer.from_json(json.dumps(respdict))
		customer.save()
		return jsonify({"status":"success","resp":[customer]})
    def put(self,cust_id):
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		customer=xpal.documents.Customer.objects(cust_id=cust_id)
		if len(customer)==0:
			return jsonify({"status":"error","resp":"No customer found"})
		else:
			customer=customer[0]
		if "_id" in respdict.keys():
			del respdict['_id']
		if "cust_id" in respdict.keys():
			if respdict['cust_id']!=cust_id:
				return jsonify({"status":"error","resp":"Customer ID mismatch"})
			del respdict['cust_id']
		customer.update(**respdict)
		customer.save()
		customer.reload()
		return jsonify({"status":"success","resp":[customer]})
    def delete(self,docid):
		if len(xpal.documents.Customer.objects.with_id(docid))>0:
			xpal.documents.Customer.objects.with_id(docid).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})
api.add_resource(CustomerResource,"/customer",endpoint="customer")
api.add_resource(CustomerResource,"/customer/by_tgid/<int:tgid>",endpoint="cust_tgid")
api.add_resource(CustomerResource,"/customer/by_mobile/<string:mobile_num>",endpoint="cust_mobile")
api.add_resource(CustomerResource,"/customer/by_id/<string:docid>",endpoint="customer_docid")
api.add_resource(CustomerResource,"/customer/by_cust_id/<string:cust_id>",endpoint="cust_id")

class ProductResource(Resource):
    def get(self,docid=None,product_id=None):
        if docid:
            if xpal.documents.Product.objects.with_id(docid):
                return jsonify({"resp": [json.loads(xpal.documents.Product.objects.with_id(docid).to_json())]})
            else:
                return jsonify({"resp":[]})
        if product_id:
			if xpal.documents.Product.objects(product_id=product_id):
				return jsonify({"resp": [json.loads(xpal.documents.Product.objects(product_id=product_id).to_json())]})
			else:
				return jsonify({"resp":[]})
        else:
            return jsonify({"resp": json.loads(xpal.documents.Product.objects.to_json())})
    def post(self,command=None):	
		app.logger.info("{}".format(request.get_json()))
		respdict=request.get_json()
		if command=="import":
			productlist=import_gadv(respdict)
			return jsonify({"resp":productlist})
		return jsonify({"resp":[]})
    def put(self,docid=None):
        return jsonify({"resp":[]})
    
    def delete(self,docid):
		if len(xpal.documents.Product.objects.with_id(docid))>0:
			xpal.documents.Product.objects.with_id(docid).delete()
			return jsonify({"resp":[True]})
		else:
			return jsonify({"resp":[False]})
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


