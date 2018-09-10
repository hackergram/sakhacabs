#!/usr/bin/env python2
# -*- coding: utf-8 -*-
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
driver_base_keyboard = [[u'\U0001f44d Check In', u'\U0001f44b Check Out'],[u'\U000025b6 Open Duty Slip']]
    
location_keyboard=[[{'text':u'OK','request_location':True}]]
server=Server()
db=server['sakhacabs']

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
    logger.info(u"New vehicle with number {} and id {} created".format(vehicle.vehicle_num))
    return vehicle



def new_dutyslip(driver,vehicle,logger=xetrapal.astra.baselogger,**kwargs): 
    created_time=datetime.datetime.utcnow()
    dutyslip=DutySlip(dutyslip_id=str(uuid4()),created_time=created_time,driver_id=driver._id,vehicle_id=vehicle._id)
    logger.info(u"New dutyslip with id {} created".format(dutyslip.dutyslip_id))
    return dutyslip

def new_locationupdate(driver,location,timestamp,checkin=True,logger=xetrapal.astra.baselogger,**kwargs): 
    locationupdate=LocationUpdate(driver_id=driver._id,timestamp=timestamp,location=location,checkin=checkin)
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


def drivermessagehandler(bot,update,logger=xetrapal.astra.baselogger):
    try: 
        logger.info(u"{} handling  message  {} from user {}".format(bot.name,update.message.text,update.message.from_user.id))
        if update.message.text==u'\U0001f44d Check In':
            bot.logger.info("Sending Checkin button")
            update.message.reply_text(text="CheckIn",reply_markup=telegram.ReplyKeyboardMarkup(location_keyboard))
        if update.message.text==u'\U0001f44b Check Out':
            bot.logger.info("Sending CheckOut button")
            update.message.reply_text(text="CheckOut",reply_markup=telegram.ReplyKeyboardMarkup(location_keyboard))
        if not update.message.text:
            bot.logger.info("Hmm...no text, could this be a location???")
            if update.message.location:    
                bot.logger.info("Yup, location it is!")
                driver=get_driver_by_tgid(update.message.from_user['id'])
                location=update.message.location.to_json()
                timestamp=update.message.date
                reply_markup = telegram.ReplyKeyboardRemove()     
                if update.message.reply_to_message.text=="CheckIn":
                    locupdate=new_locationupdate(driver,location,timestamp,logger=bot.logger)
                    update.message.reply_text(text="Check in from location {} at time {} successfull".format(location,timestamp.strftime("%Y-%m-%d %H:%M:%S")),reply_markup=reply_markup)
                    
                if update.message.reply_to_message.text=="CheckOut":
                    locupdate=new_locationupdate(driver,location,timestamp,checkin=False,logger=bot.logger)
                    update.message.reply_text(text="Check out from location {} at time {} successfull".format(location,timestamp.strftime("%Y-%m-%d %H:%M:%S")),reply_markup=reply_markup)
                locupdate.save()
                send_keyboard(bot,driver_base_keyboard,update.message.chat.id)
                
                
                
            
            
    except Exception as e:
        logger.info("Choked! "+repr(e))

def send_keyboard(bot,custom_keyboard,user_id):
    reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.updater.bot.send_message(user_id,"What would you like to do?",reply_markup=reply_markup)    