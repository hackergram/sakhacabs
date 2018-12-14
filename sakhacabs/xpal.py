# -*- coding: utf-8 -*-
#
"""
Created on Sat Sep  8 21:52:07 2018

@author: arjun
"""

import sys,datetime,json,re
import mongoengine
sys.path.append("/opt/xetrapal")
import xetrapal
import pandas
from sakhacabs import documents,utils

sakhacabsxpal=xetrapal.Xetrapal(configfile="/opt/sakhacabs-appdata/sakhacabsxpal.conf")
sakhacabsgd=sakhacabsxpal.get_googledriver()
try:
	datasheet=sakhacabsgd.open_by_key(sakhacabsxpal.config.get("SakhaCabs","datasheetkey"))
	bookingsheet=datasheet.worksheet_by_title("bookings")
	custsheet=datasheet.worksheet_by_title("customers")
	carsheet=datasheet.worksheet_by_title("cars")
	driversheet=datasheet.worksheet_by_title("drivers")
	prodsheet=datasheet.worksheet_by_title("product")
except Exception as e:
	sakhacabsxpal.logger.error("Error connecting to Google Drive, check connectivity - {} {}".format(repr(e),str(e)))

#Setting up mongoengine connections
sakhacabsxpal.logger.info("Setting up MongoEngine")
mongoengine.connect('sakhacabs', alias='default')


#Remote sync functionality

def validate_vehicle_dict(vehicledict,new=True):
	validation={}
	validation['status']=True
	validation['message']="Valid vehicle"
	required_keys=[]
	if new==True:
		required_keys=["vehicle_id"]
	string_keys=["vehicle_id"]
	validation=utils.validate_dict(vehicledict,required_keys=required_keys,string_keys=string_keys)
	if validation['status']==True:
		sakhacabsxpal.logger.info("vehicledict: "+validation['message'])
	else:
		sakhacabsxpal.logger.error("vehicledict: "+validation['message'])
	return validation


def validate_locupdate_dict(locupdatedict,new=True):
	validation={}
	validation['status']=True
	validation['message']="Valid location update"
	required_keys=[]
	if new==True:
		required_keys=["driver_id","timestamp"]
	string_keys=["driver_id"]
	validation=utils.validate_dict(locupdatedict,required_keys=required_keys,string_keys=string_keys)
	if validation['status']==True:
		sakhacabsxpal.logger.info("locupdatedict: "+validation['message'])
	else:
		sakhacabsxpal.logger.error("locupdatedict: "+validation['message'])
	return validation

def validate_customer_dict(customerdict,new=True):
	validation={}
	validation['status']=True
	validation['message']="Valid customer"
	required_keys=[]
	if new==True:
		required_keys=["cust_id"]
	string_keys=["cust_id"]
	validation=utils.validate_dict(customerdict,required_keys=required_keys,string_keys=string_keys)
	if validation['status']==True:
		sakhacabsxpal.logger.info("customerdict: "+validation['message'])
	else:
		sakhacabsxpal.logger.error("customerdict: "+validation['message'])
	return validation

def validate_product_dict(productdict,new=True):
	validation={}
	validation['status']=True
	validation['message']="Valid product"
	required_keys=[]
	if new==True:
		required_keys=["product_id"]
	string_keys=["product_id"]
	validation=utils.validate_dict(productdict,required_keys=required_keys,string_keys=string_keys)
	if validation['status']==True:
		sakhacabsxpal.logger.info("productdict: "+validation['message'])
	else:
		sakhacabsxpal.logger.error("productdict: "+validation['message'])
	return validation

def validate_driver_dict(driverdict,new=True):
	validation={}
	validation['status']=True
	validation['message']="Valid driver"
	required_keys=[]
	if new==True:
		required_keys=["driver_id","moble_num"]
	string_keys=["first_name","last_name","mobile_num","name","driver_id"]
	mobile_nums=["mobile_num"]
	validation=utils.validate_dict(driverdict,required_keys=required_keys,string_keys=string_keys,mobile_nums=mobile_nums)
	if validation['status']==True:
		sakhacabsxpal.logger.info("driverdict: "+validation['message'])
	else:
		sakhacabsxpal.logger.error("driverdict: "+validation['message'])
	return validation

def validate_dutyslip_dict(dutyslipdict,new=True):
	validation={}
	validation['status']=True
	validation['message']="Valid dutyslip"
	required_keys=[]
	if new==True:
		required_keys=["driver","assignment"]
	string_keys=["driver","vehicle","remarks"]
	validation=utils.validate_dict(dutyslipdict,required_keys=required_keys,string_keys=string_keys)
	if validation['status']==True:
		sakhacabsxpal.logger.info("dutyslipdict: "+validation['message'])
	else:
		sakhacabsxpal.logger.error("dutyslipdict: "+validation['message'])
	return validation

def validate_assignment_dict(assignmentdict,new=True):
	validation={}
	validation['status']=True
	validation['message']="Valid assignment"
	
	if assignmentdict['dutyslips']==[]:
		validation['status']=False
		validation['message']="At least one driver must be assigned to create an assignment."
        if assignmentdict['assignment']['bookings']==[]:
			validation['status']=False
			validation['message']= "At least one booking must be assigned to create an assignment."
        bookings=[documents.Booking.objects.with_id(x['_id']['$oid']) for x in assignmentdict['assignment']['bookings']]
        for booking in bookings:
			if hasattr(booking,"assignment"):
				validation['status']=False
				validation['message']= "Booking is already assigned! Please delete the old assignment before creating a new one."
			if booking.cust_id!=assignmentdict['assignment']['cust_id']:
				validation['status']=False
				validation['message']="Bookings from different customers cannot be assigned together."
        seenvehicles=[]
        for dutyslip in assignmentdict['dutyslips']:
			if "vehicle" in dutyslip.keys():
				if dutyslip['vehicle'] in seenvehicles:
					validation['status']=False
					validation['message']="Can't assign the same vehicle to more than one driver in the same assignment."
				seenvehicles.append(dutyslip['vehicle'])
	if validation['status']==True:
		sakhacabsxpal.logger.info("assignmentdict: "+validation['message'])
	else:
		sakhacabsxpal.logger.error("assignmentdict: "+validation['message'])
	return validation
	
def sync_remote():
    custlist=custsheet.get_as_df().to_dict(orient="records")
    driverlist=driversheet.get_as_df().to_dict(orient="records")
    carlist=carsheet.get_as_df().to_dict(orient="records")
    bookinglist=bookingsheet.get_as_df().to_dict(orient="records")
    productlist=prodsheet.get_as_df().to_dict(orient="records")
    for driver in driverlist:
        if len(documents.Driver.objects(driver_id=driver['driver_id']))==0:
            d=documents.Driver(driver_id=driver['driver_id'],mobile_num=str(driver['mobile_num']),first_name=driver['first_name'],last_name=driver['last_name'])
            d.save()
    driverdf=pandas.DataFrame(json.loads(documents.Driver.objects.to_json()))
    driverdf['_id']=driverdf['_id'].apply(lambda x: x['$oid'])
    driversheet.set_dataframe(driverdf,(1,1))
    
    for customer in custlist:
        if len(documents.Customer.objects(cust_id=customer['cust_id']))==0:
            c=documents.Customer(cust_id=customer['cust_id'],mobile_num=customer['mobile_num'],cust_type=customer['cust_type'],blacklisted=customer['blacklisted'],email=customer['email'],cust_name=customer['cust_name'])
            c.save()
    customerdf=pandas.DataFrame(json.loads(documents.Customer.objects.to_json()))
    customerdf['_id']=customerdf['_id'].apply(lambda x: x['$oid'])
    custsheet.set_dataframe(customerdf,(1,1))
    
    for car in carlist:
        if len(documents.Vehicle.objects(vehicle_id=car['vehicle_id']))==0:
            v=documents.Vehicle(vehicle_id=car['vehicle_id'],model=car['model'],make=car['make'],reg_num=car['reg_num'])
            v.save()
    cardf=pandas.DataFrame(json.loads(documents.Vehicle.objects.to_json()))
    cardf['_id']=cardf['_id'].apply(lambda x: x['$oid'])
    if 'driver' in cardf.columns:
        cardf['driver']=cardf['driver'].apply(lambda x: x['$oid'])
    carsheet.set_dataframe(cardf,(1,1))
    
    
    for product in productlist:
        if len(documents.Product.objects(product_id=product['product_id']))==0:
            p=documents.Product(product_id=product['product_id'],name=product['name'],price=product['price'],desc=product['desc'])
            p.save()
    productdf=pandas.DataFrame(json.loads(documents.Product.objects.to_json()))
    productdf['_id']=productdf['_id'].apply(lambda x: x['$oid'])
    prodsheet.set_dataframe(productdf,(1,1))
    
    
    for booking in bookinglist:
        if len(documents.Product.objects(product_id=product['product_id']))==0:
            p=documents.Product(product_id=product['product_id'],name=product['name'],price=product['price'],desc=product['desc'])
            p.save()
    productdf=pandas.DataFrame(json.loads(documents.Product.objects.to_json()))
    productdf['_id']=productdf['_id'].apply(lambda x: x['$oid'])
    prodsheet.set_dataframe(productdf,(1,1))

'''
LocationUpdate CRUD functionality
Fix to check if vehicle is already  taken.
'''

def new_locationupdate(driver,timestamp,checkin=True,location=None,vehicle=None,handoff=None,logger=xetrapal.astra.baselogger,**kwargs): 
	"""
	Creates a new location update, location updates once created are not deleted as they are equivalent to log entries. 
	Returns a LocationUpdate object
	"""
	vehicle_id=None
	if checkin==True:
		driver.checkedin=True
        if vehicle!=None:
            vehicle.driver_id=driver.driver_id
            vehicle.save()
            vehicle_id=vehicle.vehicle_id
	if checkin==False:
		driver.checkedin=False
		if len(documents.Vehicle.objects(driver_id=driver.driver_id))>0:
			v=documents.Vehicle.objects(driver_id=driver.driver_id)
			for vh in v:
				del vh.driver_id
				vh.save()
				vehicle_id=vh.vehicle_id
	driver.save()
	#UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
	adjtimestamp = utils.get_utc_ts(timestamp)#timestamp + UTC_OFFSET_TIMEDELTA
	# Get new location update and save it
	locationupdate=documents.LocationUpdate(driver_id=driver.driver_id,timestamp=adjtimestamp,location=location,checkin=checkin,handoff=handoff,vehicle_id=vehicle_id)
	# Tell the user what happened
	if checkin==True:
		logger.info(u"New checkin from driver with id {} at {} from {}".format(locationupdate.driver_id,locationupdate.timestamp,locationupdate.location))
	else:
		logger.info(u"Checkout from driver with id {} at {} from {}".format(locationupdate.driver_id,locationupdate.timestamp,locationupdate.location))
	locationupdate.save()
	return locationupdate



'''
Bookings, Assignments and DutySlips
Assignments are collections of one or more bookings grouped together for assignment of vehicles/drivers
DutySlips record assignment execution. DutySlips are issued by the dispatcher and can be created and deleted but not updated.
A DutySlip can not be deleted once the open time has been set by the driver, i.e. after execution on an assignment has begun.
'''
'''
Bookings CRUD
'''
def validate_booking_dict(bookingdict,new=True):
	validation={}
	validation['status']=True
	validation['message']="Valid booking"
	required_keys=[]
	if new==True:
		required_keys=["cust_id","product_id","passenger_detail","passenger_mobile","pickup_timestamp","pickup_location","booking_channel"]
	string_keys=["cust_id","product_id","passenger_detail","passenger_mobile","remarks"]
	mobile_nums=["passenger_mobile"]
	validation=utils.validate_dict(bookingdict,required_keys=required_keys,string_keys=string_keys,mobile_nums=mobile_nums)			
	if validation['status']==True:
		sakhacabsxpal.logger.info("bookingdict: "+validation['message'])
	else:
		sakhacabsxpal.logger.error("bookingdict: "+validation['message'])
	return validation

def new_booking(respdict):
	bookingdict={}
	sakhacabsxpal.logger.info("Creating new booking")
	sakhacabsxpal.logger.info("{}".format(respdict))
	for key in respdict.keys():
		if key in ["cust_id","product_id","passenger_detail","passenger_mobile","pickup_timestamp","pickup_location","drop_location","booking_channel","num_passengers"]:
			bookingdict[key]=respdict[key]
			respdict.pop(key)
	if "_id" in respdict.keys():
		respdict.pop("_id")
	if "created_timestamp" in respdict.keys():
		respdict.pop("created_timestamp")
	
	sakhacabsxpal.logger.info("{}".format(respdict))
	dupbookings=documents.Booking.objects(cust_meta=respdict)
	if len(dupbookings)>0:
		sakhacabsxpal.logger.info("Duplicate booking {}".format(dupbookings))
		return "Duplicate of {}".format(dupbookings[0].booking_id)
	else:
		try:
			b=documents.Booking(booking_id=utils.new_booking_id(),**bookingdict)
			b.cust_meta=respdict
			b.save()
			b.reload()
			sakhacabsxpal.logger.info("{}".format(b))
			return [b]
		except Exception as e:
			return "{} {}".format(type(e),str(e))


def update_booking(booking_id,respdict):
	booking=documents.Booking.objects(booking_id=booking_id)
	if len(booking)==0:
		return "No booking by that id"
	else:
		booking=booking[0]
		sakhacabsxpal.logger.info("Trying to update booking with id {}".format(booking.booking_id))
		if "_id" in respdict.keys():
			respdict.pop("_id")
		if "created_timestamp" in respdict.keys():
			respdict.pop("created_timestamp")
		try:
			booking.update(**respdict)
			booking.reload()
			if booking.assignment!=None:
				assignment=documents.Assignment.objects.with_id(booking.assignment)
				if "pickup_timestamp" in respdict.keys():
					assignment.reporting_timestamp=booking.pickup_timestamp
				if "pickup_location" in respdict.keys():
					assignment.reporting_location=booking.pickup_location
				assignment.save()
					
			return [booking]
		except Exception as e:
			return "{} {}".format(type(e),str(e))


def delete_booking(booking_id):
	if len(documents.Booking.objects(booking_id=booking_id))>0:
		try:
			booking=documents.Booking.objects(booking_id=booking_id)[0]
			assignment=booking.assignment
			booking.delete()
			if assignment!=None:
				if len(documents.Booking.objects(assignment=assignment))==0:
					sakhacabsxpal.logger.info("No more bookings in assignment. Deleting!")
					documents.Assignment.objects.with_id(assignment).delete()	
				else:
					sakhacabsxpal.logger.info("Updating assignment reporting time to first booking!")
					assignmentobj=documents.Assignment.objects.with_id(assignment)
					assignmentobj.reporting_location=assignmentobj.bookings[0].pickup_location
					assignmentobj.reporting_timestamp=assignmentobj.bookings[0].pickup_timestamp
					assignmentobj.save()
			return []
		except Exception as e:
			return "{} {}".format(type(e),str(e))
	else:
		return "No booking by that id"

			
'''
Assignment CRUD
'''
def save_assignment(assignmentdict,assignment_id=None):
    '''
    Creates a new assignment/Updates an existing assignment with the provided bookings and duty slips
    Input: A dictionary of the format {"assignment": Assignment object,dutyslips: List of driver/vehicle pairs}
    Returns: An assignment object
    '''
    #bookings=[documents.Booking.from_json(json.dumps(x)) for x in assignmentdict['assignment']['bookings']]
    bookings=[documents.Booking.objects.with_id(x['_id']['$oid']) for x in assignmentdict['assignment']['bookings']]
    if assignment_id==None:
		assignment=documents.Assignment(bookings=bookings)
		assignment.status="new"
		sakhacabsxpal.logger.info("Created new assignment at {}".format(assignment.created_timestamp.strftime("%Y-%m-%d %H:%M:%S")))
    else:
		sakhacabsxpal.logger.info("Saving existing assignment {}".format(assignment_id))
		assignment=documents.Assignment.objects.with_id(assignment_id)
		assignment.bookings=bookings
    assignment.bookings=sorted(assignment.bookings, key=lambda k: k.pickup_timestamp)
    assignment.reporting_timestamp=assignment.bookings[0].pickup_timestamp
    assignment.reporting_location=assignment.bookings[0].pickup_location
    if assignment.bookings[0].drop_location:
		assignment.drop_location=assignment.bookings[0].drop_location
    assignment.cust_id=assignment.bookings[0].cust_id	
    assignment.save()
    existingdutyslips=documents.DutySlip.objects(assignment=assignment)
    sakhacabsxpal.logger.info("Existing duty slips {}".format(existingdutyslips.to_json()))
    existingdutyslips=list(existingdutyslips)
    sakhacabsxpal.logger.info("Submitted duty slips {}".format(assignmentdict['dutyslips']))
    sakhacabsxpal.logger.info("Ignoring unchanged dutyslips")
    for dutyslip in existingdutyslips:
		sakhacabsxpal.logger.info("{}".format(dutyslip.to_json()))
		match=False
		for dutyslipdict in assignmentdict['dutyslips']:
			#sakhacabsxpal.logger.info("{}".format(dutyslipdict))
			if dutyslip.driver==dutyslipdict['driver'] and dutyslip.vehicle==dutyslipdict['vehicle']:
				sakhacabsxpal.logger.info("Unchanged {}".format(dutyslipdict))
				#assignmentdict['dutyslips'].remove(dutyslipdict)
				#existingdutyslips.remove(dutyslip)
				match=True
		if match==False:
			sakhacabsxpal.logger.info("Removing unmatched dutyslip {}".format(dutyslip.to_json()))
			dutyslip.delete()
    sakhacabsxpal.logger.info("Adding the new dutyslips")
    for dutyslipdict in assignmentdict['dutyslips']:
		if "vehicle" not in dutyslipdict.keys():
			dutyslipdict['vehicle']=None
		d=documents.DutySlip.objects(driver=dutyslipdict['driver'],vehicle=dutyslipdict['vehicle'],assignment=assignment)
		if len(d)==0:
			d=documents.DutySlip(driver=dutyslipdict['driver'],vehicle=dutyslipdict['vehicle'],assignment=assignment,status="new")
			sakhacabsxpal.logger.info("Created duty slip {}".format(d.to_json()))
		else:
			d=d[0]
			sakhacabsxpal.logger.info("Duty slip exists {}".format(d.to_json()))
		d.save()
    for booking in assignment.bookings:
		booking.assignment=str(assignment.id)
		booking.save()
    sakhacabsxpal.logger.info("Saved assignment {}".format(assignment.to_json()))
    return [assignment]

def search_assignments(cust_id=None,date_frm=None,date_to=None):
	assignments=documents.Assignment.objects
	if cust_id!=None:
		assignments=assignments.filter(cust_id=cust_id)
	if date_frm!=None:
		assignments=assignments.filter(reporting_timestamp__gt=date_frm)
	if date_to!=None:
		assignments=assignments.filter(reporting_timestamp__lt=date_to)
	return assignments

def delete_assignment(assignmentid):
	if len(xpal.documents.Assignment.objects.with_id(assignment))>0:
			dutyslips=xpal.documents.DutySlip.objects(assignment=xpal.documents.Assignment.objects.with_id(assignmentid))
			app.logger.info("Deleting DutySlips {}".format(dutyslips.to_json()))
			dutyslips.delete()
			bookings=xpal.documents.Booking.objects(assignment=assignmentid)
			app.logger.info("Removing Assignment reference from  Bookings {}".format(bookings.to_json()))
			
			for booking in bookings:
				del(booking.assignment)
				booking.save()
			xpal.documents.Assignment.objects.with_id(assignment).delete()
			return []
	else:
		return "Assignment with that ID does not exist"

'''
Duty Slip CRUD
'''
def get_duties_for_driver(driver_id):
	d=documents.DutySlip.objects(driver=driver_id,status__ne="verified")
	if len(d)>0:
		return d

def update_dutyslip(dsid,respdict):
	dutyslip=xpal.documents.DutySlip.objects.with_id(docid)
	if dutyslip==None:
		return "No dutyslip with that id found"
	try:
		dutyslip.update(**respdict)
		dutyslip.save()
		dutyslip.reload()
		return [dutyslip]
	except Exception as e:
		return "{} {}".format(type(e),str(e))

def delete_dutyslip(dsid):
	if len(documents.DutySlip.objects.with_id(dsid))>0:
		ds=documents.DutySlip.objects.with_id(dsid)
		assignment=ds.assignment
		ds.delete()
		if len(documents.DutySlip.objects(assignment=assignment))==0:
			documents.Assignment.objecs.with_id(assignment).delete()
		return []
	else:
		return "No Dutyslip by that ID"
			
'''
Driver CRUD functionality
'''
def get_driver_by_mobile(mobile_num):
    t=documents.Driver.objects(mobile_num=mobile_num)
    xetrapal.astra.baselogger.info("Found {} drivers with Mobile Num {}".format(len(t),mobile_num))
    if len(t)>0:
        #return[User(x['value']) for x in t][0]
        return t[0]
    else:
        return None

def get_driver_by_tgid(tgid):
    t=documents.Driver.objects(tgid=tgid)
    xetrapal.astra.baselogger.info("Found {} drivers with Telegram ID {}".format(len(t),tgid))
    if len(t)>0:
        #return[User(x['value']) for x in t][0]
        return t[0]
    else:
        return None
def create_driver(respdict):
	driver=xpal.documents.Driver.objects(driver_id=respdict['driver_id'])
	if len(driver)>0:
		return "Driver with that ID Exists"
	if "_id" in respdict.keys():
		respdict.pop('_id')			
	try:
		driver=xpal.documents.Driver(**respdict)
		driver.save()
		return [driver]
	except Exception as e:
		return "{} {}".format(repr(e),str(e))
	
def update_driver(driver_id,respdict):
	driver=documents.Driver.objects(driver_id=driver_id)
	if len(driver)==0:
		return "No driver by ID {}".format(driver_id)
	else:
		driver=driver[0]
	if "_id" in respdict.keys():
		respdict.pop('_id')
	if "driver_id" in respdict.keys():
		if respdict['driver_id']!=driver_id:
			return "Driver ID mismatch {} {}".format(driver_id,respdict['driver_id'])
		respdict.pop('driver_id')
	try:
		driver.update(**respdict)
		driver.save()
		driver.reload()
		return [driver]
	except Exception as e:
		return "{} {}".format(type(e),str(e))


def delete_driver(driver_id):
	if len(documents.Driver.objects(driver_id=driver_id))>0:
		try:
			driver=documents.Driver.objects(driver_id=driver_id)[0]
			driver.delete()
			return []
		except Exception as e:
			return "{} {}".format(type(e),str(e))
	else:
		return "No driver by that id"

'''
Vehicle CRUD functionality
'''

def get_vehicle_by_vid(vid):
    #t=db.view("vehicle/all_by_vnum",keys=[vnum]).all()
    t=documents.Vehicle.objects(vehicle_id=vid)
    
    if len(t)>0:
        #return [Vehicle(x['value']) for x in t][0]
        return t[0]
    else:
        return None


def create_vehicle(respdict):
	vehicle=xpal.documents.Vehicle.objects(vehicle_id=respdict['vehicle_id'])
	if len(vehicle)>0:
		return "Vehicle with that ID Exists"
	if "_id" in respdict.keys():
		respdict.pop('_id')			
	try:
		vehicle=xpal.documents.Vehicle(**respdict)
		vehicle.save()
		return [vehicle]
	except Exception as e:
		return "{} {}".format(repr(e),str(e))
	
def update_vehicle(vehicle_id,respdict):
	vehicle=documents.Vehicle.objects(vehicle_id=vehicle_id)
	if len(vehicle)==0:
		return "No Vehicle by ID {}".format(vehicle_id)
	else:
		vehicle=vehicle[0]
	if "_id" in respdict.keys():
		respdict.pop('_id')
	if "vehicle_id" in respdict.keys():
		if respdict['vehicle_id']!=vehicle_id:
			return "vehicle ID mismatch {} {}".format(vehicle_id,respdict['vehicle_id'])
		respdict.pop('vehicle_id')
	try:
		vehicle.update(**respdict)
		vehicle.save()
		vehicle.reload()
		return [vehicle]
	except Exception as e:
		return "{} {}".format(type(e),str(e))


def delete_vehicle(vehicle_id):
	if len(documents.Vehicle.objects(vehicle_id=vehicle_id))>0:
		try:
			vehicle=documents.Vehicle.objects(vehicle_id=vehicle_id)[0]
			vehicle.delete()
			return []
		except Exception as e:
			return "{} {}".format(type(e),str(e))
	else:
		return "No vehicle by that id"




'''
Customer
'''

def create_customer(respdict):
	customer=xpal.documents.Customer.objects(cust_id=respdict['cust_id'])
	if len(customer)>0:
		return "Customer with that ID Exists"
	if "_id" in respdict.keys():
		respdict.pop('_id')			
	try:
		customer=xpal.documents.Customer(**respdict)
		customer.save()
		return [customer]
	except Exception as e:
		return "{} {}".format(repr(e),str(e))
	
def update_customer(cust_id,respdict):
	customer=documents.Customer.objects(cust_id=cust_id)
	if len(customer)==0:
		return "No Customer by ID {}".format(cust_id)
	else:
		customer=customer[0]
	if "_id" in respdict.keys():
		respdict.pop('_id')
	if "cust_id" in respdict.keys():
		if respdict['cust_id']!=cust_id:
			return "customer ID mismatch {} {}".format(cust_id,respdict['cust_id'])
		respdict.pop('cust_id')
	try:
		customer.update(**respdict)
		customer.save()
		customer.reload()
		return [customer]
	except Exception as e:
		return "{} {}".format(type(e),str(e))


def delete_customer(cust_id):
	if len(documents.Customer.objects(cust_id=cust_id))>0:
		try:
			customer=documents.Customer.objects(cust_id=cust_id)[0]
			customer.delete()
			return []
		except Exception as e:
			return "{} {}".format(type(e),str(e))
	else:
		return "No customer by that id"




'''
Product
'''

def create_product(respdict):
	product=xpal.documents.Product.objects(product_id=respdict['product_id'])
	if len(product)>0:
		return "Product with that ID Exists"
	if "_id" in respdict.keys():
		respdict.pop('_id')			
	try:
		product=xpal.documents.Product(**respdict)
		product.save()
		return [product]
	except Exception as e:
		return "{} {}".format(repr(e),str(e))
	
def update_product(product_id,respdict):
	product=documents.Product.objects(product_id=product_id)
	if len(product)==0:
		return "No Product by ID {}".format(product_id)
	else:
		product=product[0]
	if "_id" in respdict.keys():
		respdict.pop('_id')
	if "product_id" in respdict.keys():
		if respdict['product_id']!=product_id:
			return "product ID mismatch {} {}".format(product_id,respdict['product_id'])
		respdict.pop('product_id')
	try:
		product.update(**respdict)
		product.save()
		product.reload()
		return [product]
	except Exception as e:
		return "{} {}".format(type(e),str(e))


def delete_product(product_id):
	if len(documents.Product.objects(product_id=product_id))>0:
		try:
			product=documents.Product.objects(product_id=product_id)[0]
			product.delete()
			return []
		except Exception as e:
			return "{} {}".format(type(e),str(e))
	else:
		return "No product by that id"




'''
Invoices
'''
def get_invoice(to_settle):
	invoice_lines=[]
	for ass in to_settle:
		covered_hrs=0;
		covered_kms=0;
		for booking in ass.bookings:
			invoiceline={}
			invoiceline['date']=utils.get_local_ts(booking.pickup_timestamp).strftime("%Y-%m-%d")
			invoiceline['particulars']=booking.booking_id+" "+booking.passenger_detail
			invoiceline['product']=booking.product_id
			invoiceline['qty']=1
			invoiceline['rate']=documents.Product.objects(product_id=booking.product_id)[0].price
			invoiceline['amount']=invoiceline['qty']*invoiceline['rate']
			invoice_lines.append(invoiceline)
			covered_hrs+=documents.Product.objects(product_id=booking.product_id)[0].hrs
			covered_kms+=documents.Product.objects(product_id=booking.product_id)[0].kms
		consumed_hrs=0;
		consumed_kms=0;
		for ds in documents.DutySlip.objects(assignment=ass):
			print repr(ds)
			kms=ds.close_kms-ds.open_kms
			consumed_kms+=kms
			hrs=ds.close_time-ds.open_time
			consumed_hrs+=int(hrs.total_seconds()/3600)
			if ds.parking_charges!=None:
				invoiceline={}                                               
				invoiceline['date']=utils.get_local_ts(ass.reporting_timestamp).strftime("%Y-%m-%d")
				invoiceline['particulars']="Parking Charges"
				invoiceline['product']="PARKINGCHRGS"
				invoiceline['rate']=int(ds.parking_charges)
				invoiceline['qty']=1
				invoiceline['amount']=invoiceline['qty']*invoiceline['rate']
				if invoiceline['amount']!=0:
					invoice_lines.append(invoiceline)
			if ds.toll_charges!=None:
				invoiceline={}                                               
				invoiceline['date']=utils.get_local_ts(ass.reporting_timestamp).strftime("%Y-%m-%d")
				invoiceline['particulars']="Toll Charges"
				invoiceline['product']="TOLLCHRGS"
				invoiceline['rate']=int(ds.toll_charges)
				invoiceline['qty']=1
				invoiceline['amount']=invoiceline['qty']*invoiceline['rate']
				if invoiceline['amount']!=0:
					invoice_lines.append(invoiceline)
		if consumed_kms>covered_kms:
			extrakms=consumed_kms-covered_kms
			invoiceline={}                   
			invoiceline['date']=utils.get_local_ts(ass.reporting_timestamp).strftime("%Y-%m-%d")
			invoiceline['particulars']="Extra Kms "+str(ds.dutyslip_id)
			invoiceline['product']="EXTRAKMS"                               
			invoiceline['rate']=20                                         
			invoiceline['qty']=extrahrs                                     
			invoiceline['amount']=invoiceline['qty']*invoiceline['rate']    
			if invoiceline['amount']!=0:
				invoice_lines.append(invoiceline)
		if consumed_hrs>covered_hrs:
			extrahrs=consumed_hrs-covered_hrs
			invoiceline={}
			invoiceline['date']=utils.get_local_ts(ass.reporting_timestamp).strftime("%Y-%m-%d")
			invoiceline['particulars']="Extra Hours "+str(ds.dutyslip_id)
			invoiceline['product']="EXTRAHRS"
			invoiceline['rate']=100
			invoiceline['qty']=extrahrs
			invoiceline['amount']=invoiceline['qty']*invoiceline['rate']
			if invoiceline['amount']!=0:
				invoice_lines.append(invoiceline)
	invoice={}
	invoice['invoicelines']=invoice_lines
	invoice['cust_id']=to_settle[0].cust_id
	total=0
	for line in invoice_lines:
		total+=line['amount']
	invoice['total']=total
	return invoice





'''
Exporting everything
'''

def export_drivers():
	drivers=documents.Driver.objects.to_json()
	drivers=json.loads(drivers)
	for driver in drivers:
		del driver['_id']
	driverdf=pandas.DataFrame(drivers)
	driverdf.to_csv("./dispatcher/reports/drivers.csv")
	return "reports/drivers.csv"
	
def export_locupdates():
	locupdates=documents.LocationUpdate.objects.to_json()
	locupdates=json.loads(locupdates)
	for locupdate in locupdates:
		del locupdate['_id']
	locupdatedf=pandas.DataFrame(locupdates)
	locupdatedf.timestamp=locupdatedf.timestamp.apply(lambda x: datetime.datetime.fromtimestamp((x['$date']+1)/1000).strftime("%Y-%m-%d %H:%M:%S"))
	locupdatedf.to_csv("./dispatcher/reports/locupdates.csv")
	return "reports/locupdates.csv"
	
def export_vehicles():
	vehicles=documents.Vehicle.objects.to_json()
	vehicles=json.loads(vehicles)
	for vehicle in vehicles:
		del vehicle['_id']
	vehicledf=pandas.DataFrame(vehicles)
	vehicledf.to_csv("./dispatcher/reports/vehicles.csv")
	return "reports/vehicles.csv"

def export_bookings():
	bookings=documents.Booking.objects.to_json()
	bookings=json.loads(bookings)
	for booking in bookings:
		del booking['_id']
	bookingdf=pandas.DataFrame(bookings)
	bookingdf.created_timestamp=bookingdf.created_timestamp.apply(lambda x: datetime.datetime.fromtimestamp((x['$date']+1)/1000).strftime("%Y-%m-%d %H:%M:%S"))
	bookingdf.pickup_timestamp=bookingdf.pickup_timestamp.apply(lambda x: datetime.datetime.fromtimestamp((x['$date']+1)/1000).strftime("%Y-%m-%d %H:%M:%S"))
	bookingdf.to_csv("./dispatcher/reports/bookings.csv", encoding="utf-8")
	return "reports/bookings.csv"



'''
Bulk Imports of everything
'''
#def import_gadv():
def import_gadv(bookinglist):
	for booking in bookinglist:
		dupbookings=documents.Booking.objects(cust_meta=booking)
		#if 'booking_id' in booking.keys() and booking['booking_id']!="" and len(documents.Booking.objects(booking_id=booking['booking_id']))>0:
		if len(dupbookings)>0:
			sakhacabsxpal.logger.info("Duplicate booking {}".format(dupbookings))
			booking['booking_id']=dupbookings[0].booking_id
			#b=documents.Booking.objects(booking_id=booking['booking_id'])[0]
			#b.cust_meta=booking
		else:
			sakhacabsxpal.logger.info("New Booking") #TODO - Merge with single booking workflow #83
			b.passenger_detail=str(b.cust_meta['Booking ID'])+"\n"+b.cust_meta['Trip Code']+"\n"+b.cust_meta['Passengers']
			b.pickup_location="Intl Airport, Flight #"+str(b.cust_meta['Pick-Up'])
			b.drop_location=b.cust_meta['Drop-Off']
			b.num_passengers=len(b.cust_meta['Passengers'].split(","))
			b.booking_channel="bulk"
			if b.cust_meta['Flight Time'] == "None":
				b.cust_meta['Flight Time']="00:00:00"
			b.pickup_timestamp=utils.get_utc_ts(datetime.datetime.strptime(b.cust_meta['Date']+" "+b.cust_meta['Flight Time'],"%Y-%m-%d %H:%M:%S"))
			if b.cust_meta['Transfer Name']=="Airport to Hotel Transfer":
				b.product_id="GADVARPTPKUP"
			
			b.save()
			booking['booking_id']=b.booking_id
			    
	return bookinglist

def import_bookings(bookinglist):
	try:
		for booking in bookinglist:
				try:
					b=new_booking(booking)
					if type(b)==list:
						booking['booking_id']=b[0].booking_id
					else:
						booking['booking_id']=b
				except Exception as e:
					booking['booking_id']="{} {}".format(type(e),str(e))
		return bookinglist
	except Exception as e:
			return "{} {}".format(type(e),str(e))
		
			
