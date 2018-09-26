#!/u*-
"""
Created on Sat Sep  8 21:52:07 2018

@author: arjun
"""

import sys,os,json
from uuid import uuid4
import datetime
sys.path.append("/opt/xetrapal")
from sakhacabsdatamodelmongo import User,LocationUpdate,DutySlip,Vehicle
import xetrapal
#from couchdbkit import *
from mongoengine import *
from pymongo import *
import mongoengine
import telegram
from telegram.ext import ConversationHandler, MessageHandler, RegexHandler, CommandHandler, Filters
mongoengine.connect('sakhacabs', alias='default')

#server=Server()
#db=server['sakhacabs']
#client=MongoClient()
#db=client.get_database("sakhacabs")

#User.set_db(db)
#LocationUpdate.set_db(db)
#DutySlip.set_db(db)
#Vehicle.set_db(db)
#DB Functions
def new_user(telegram_id,role,logger=xetrapal.astra.baselogger,**kwargs):    
    meta={}
    for key in kwargs.keys():
        meta[key]=kwargs[key]
    user=User(telegram_id=telegram_id,meta=meta,role=role)
    logger.info(u"New {} created".format(user.role))
    
    return user


def new_vehicle(vehicle_num,logger=xetrapal.astra.baselogger,**kwargs):
    vehicle_meta={}
    for key in kwargs.keys():
        vehicle_meta[key]=kwargs[key]
    vehicle=Vehicle(vehicle_num=vehicle_num,meta=vehicle_meta)
    logger.info(u"New vehicle with number {} and id {} created".format(vehicle.vehicle_num,vehicle._id))
    return vehicle



def new_dutyslip(driver,vehicle,logger=xetrapal.astra.baselogger,**kwargs): 
    created_time=datetime.datetime.utcnow()
    dutyslip=DutySlip(dutyslip_id=str(uuid4()),created_time=created_time,driver_id=driver._id,vehicle_id=vehicle._id)
    logger.info(u"New dutyslip with id {} created".format(dutyslip.dutyslip_id))
    return dutyslip


#Fix to check if vehicle is already  taken. 
def new_locationupdate(driver,location,timestamp,checkin=True,vehicle=None,handoff=None,logger=xetrapal.astra.baselogger,**kwargs): 
    driver_id=driver.id
    if handoff != None:
        handoff_id=handoff.id
    else:
        handoff_id=None
    if vehicle != None:
        vehicle_id=vehicle.id
    else:
        vehicle_id=None
    if checkin==True:
        driver.checkedin=True
        # If the driver is checking in with a vehicle
        if vehicle!=None:
            # Associate driver with vehicle
            driver.vehicle_id=vehicle_id
            # Associate vehicle with driver
            vehicle.driver_id=driver_id
            vehicle.save()
        
    if checkin==False:
        if driver.vehicle_id!=None:
            # If the driver has a vehicle associated, 
            # get the vehicle object 
            # and remove the driver association from the vehicle object
            # save the vehicle object
            driver_vehicle=Vehicle(get_
                                   object_for_id(driver.vehicle_id))
            driver_vehicle.driver_id=None
            driver_vehicle.save()
            # If the driver has a vehicle associated, 
            # remove the vehicle association from the driver object
            driver.vehicle_id=None
        driver.checkedin=False
        
    
    driver.save()
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    adjtimestamp = timestamp + UTC_OFFSET_TIMEDELTA
    # Get new location update and save it
    locationupdate=LocationUpdate(driver_id=driver.id,timestamp=adjtimestamp,location=location,checkin=checkin,handoff=handoff_id,vehicle_id=vehicle_id)
    locationupdate.save()
    
    # Tell the user what happened
    if checkin==True:
        logger.info(u"New checkin from driver with id {} at {} from {}".format(locationupdate.driver_id,locationupdate.timestamp,locationupdate.location))
    else:
        logger.info(u"Checkout from driver with id {} at {} from {}".format(locationupdate.driver_id,locationupdate.timestamp,locationupdate.location))
    
    return locationupdate

def get_driver_by_tgid(tgid):
    t=User.objects(role="driver",telegram_id=tgid)
    xetrapal.astra.baselogger.info(len(t))
    if len(t)>0:
        #return[User(x['value']) for x in t][0]
        return t[0]
    else:
        return None
def get_customer_by_tgid(tgid):
    #t=db.view("user/cust_by_telegram",keys=[tgid]).all()
    t=User.objects(role="customer",telegram_id=tgid)
    if len(t)>0:
        return t[0]
    else:
        return None
'''
def get_property_for_id(docid,prop):
    t=db.view("all/by_id",keys=[docid]).all()[0]['value'][prop]
    return t
'''
def get_vehicle_by_vnum(vnum):
    #t=db.view("vehicle/all_by_vnum",keys=[vnum]).all()
    t=Vehicle.objects(vehicle_num=vnum)
    
    if len(t)>0:
        #return [Vehicle(x['value']) for x in t][0]
        return t[0]
    else:
        return None
def get_user_for_id(oid):
    return User.objects.with_id(oid)

def get_vehicle_for_id(oid):
    return Vehicle.objects.with_id(oid)

