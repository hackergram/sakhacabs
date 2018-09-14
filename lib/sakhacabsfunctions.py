#!/u*-
"""
Created on Sat Sep  8 21:52:07 2018

@author: arjun
"""

import sys,os,json
from uuid import uuid4
import datetime
sys.path.append("/opt/xetrapal")
from sakhacabsdatamodel import User,LocationUpdate,DutySlip,Vehicle
import xetrapal
from couchdbkit import *
import telegram
from telegram.ext import ConversationHandler, MessageHandler, RegexHandler, CommandHandler, Filters

server=Server()
db=server['sakhacabs']

User.set_db(db)
LocationUpdate.set_db(db)
DutySlip.set_db(db)
Vehicle.set_db(db)
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

def new_locationupdate(driver,location,timestamp,checkin=True,vehicle=None,handoff=None,logger=xetrapal.astra.baselogger,**kwargs): 
    
    if vehicle!=None:
        driver_id=driver._id
        vehicle_id=vehicle._id
        if checkin==True:
            driver.vehicle_id=vehicle_id
            vehicle.driver_id=driver_id
        if checkin==False:
            driver.vehicle_id=None
            vehicle.driver_id=None
        
        vehicle.save()
        driver.save()
    else:
        vehicle_id=None
    locationupdate=LocationUpdate(driver_id=driver._id,timestamp=timestamp,location=location,checkin=checkin,handoff=handoff,vehicle_id=vehicle_id)
    if checkin==True:
        logger.info(u"New checkin from driver with id {} at {} from {}".format(locationupdate.driver_id,locationupdate.timestamp,locationupdate.location))
    else:
        logger.info(u"Checkout from driver with id {} at {} from {}".format(locationupdate.driver_id,locationupdate.timestamp,locationupdate.location))
    
    return locationupdate

def get_driver_by_tgid(tgid):
    t=db.view("user/driver_by_telegram",keys=[tgid]).all()
    if len(t)>0:
        return[User(x['value']) for x in t][0]
    else:
        return None
def get_customer_by_tgid(tgid):
    t=db.view("user/cust_by_telegram",keys=[tgid]).all()
    if len(t)>0:
        return [User(x['value']) for x in t][0]
    else:
        return None

def get_property_for_id(docid,prop):
    t=db.view("all/by_id",keys=[docid]).all()[0]['value'][prop]
    return t

def get_vehicle_by_vnum(vnum):
    t=db.view("vehicle/all_by_vnum",keys=[vnum]).all()
    if len(t)>0:
        return [Vehicle(x['value']) for x in t][0]
    else:
        return None




