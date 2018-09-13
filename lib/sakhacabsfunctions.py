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
    logger.info(u"New vehicle with number {} and id {} created".format(vehicle.vehicle_num))
    return vehicle



def new_dutyslip(driver,vehicle,logger=xetrapal.astra.baselogger,**kwargs): 
    created_time=datetime.datetime.utcnow()
    dutyslip=DutySlip(dutyslip_id=str(uuid4()),created_time=created_time,driver_id=driver._id,vehicle_id=vehicle._id)
    logger.info(u"New dutyslip with id {} created".format(dutyslip.dutyslip_id))
    return dutyslip

def new_locationupdate(driver,location,timestamp,checkin=True,vehicle_id=None,handoff=None,logger=xetrapal.astra.baselogger,**kwargs): 
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



#Bot Functions

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)



GENDER, PHOTO, LOCATION, BIO = range(4)


def start(bot, update):
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return GENDER


def gender(bot, update):
    user = update.message.from_user
    bot.logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    bot.logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION


def skip_photo(bot, update):
    user = update.message.from_user
    bot.logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    bot.logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(bot, update):
    user = update.message.from_user
    bot.logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(bot, update):
    user = update.message.from_user
    bot.logger.info("Bio of %s: %s", user.first_name, update.message.text)
    bot.update.message.reply_text('Thank you! I hope we can talk again some day.')
    bot.update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    bot.logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    bot.logger.warning('Update "%s" caused error "%s"', update, error)














    '''








def send_keyboard(bot,custom_keyboard,user_id):
    reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.updater.bot.send_message(user_id,"What would you like to do?",reply_markup=reply_markup)    

def checkin(bot,update,parsed_update,logger=xetrapal.astra.baselogger):
    logger.info("Checkin")
    if parsed_update['response']==u'\U0001f44d Check In':
        bot.updater.bot.send_message(parsed_update['reply_id'],u"\U0001f44d Check In\nVehicle?",reply_markup=telegram.InlineKeyboardMarkup(yes_no_keyboard))
        
    if parsed_update['source_message']==u"\U0001f44d Check In\nVehicle?" and parsed_update['response']==u"Yes":
        bot.updater.bot.send_message(parsed_update['reply_id'],u"\U0001f44d Check In\nVehicle:Yes\nVehicle Num?",reply_markup=telegram.ForceReply())
    if parsed_update['source_message']==u"\U0001f44d Check In\nVehicle?" and parsed_update['response']==u"No":
        bot.updater.bot.send_message(parsed_update['reply_id'],u"\U0001f44d Check In\nVehicle:No\nHandoff?",reply_markup=telegram.InlineKeyboardMarkup(yes_no_keyboard))
    if parsed_update['source_message']==u"\U0001f44d Check In\nVehicle:Yes\nVehicle Num?" and parsed_update['response']!=None:
       bot.updater.bot.send_message(parsed_update['reply_id'],u"\U0001f44d Check In\nVehicle:Yes\nVehicle Num:"+parsed_update['response']+"\nHandoff?",reply_markup=telegram.InlineKeyboardMarkup(yes_no_keyboard))
  
def drivermessagehandler(bot,update,parsed_update,logger=xetrapal.astra.baselogger):
    logger.info(u"{}".format(parsed_update))
    if parsed_update['response'].startswith(u'\U0001f44d Check In') or parsed_update['source_message'].startswith(u'\U0001f44d Check In'):
        logger.info(u"Starting checkin")
        checkin(bot,update,parsed_update,logger)
                
        
        
    
    

    if update.callback_query:
        query=update.callback_query
        tg_id=update.callback_query.from_user['id']
        try: 
            driver=get_driver_by_tgid(tg_id)
            bot.logger.info("Got query data {} in response to query {}".format(query.data,query.message.text))
            #update.message.reply_text(text="Enter Vehicle Number ",reply_markup=telegram.ReplyKeyboardMarkup(location_keyboard))
        except Exception as e:
            logger.info("Choked! "+repr(e))
            
    if update.message:
        tg_id=update.message.from_user['id']
        try: 
            driver=get_driver_by_tgid(tg_id)
            logger.info(u"{} handling  message  {} from driver {}".format(bot.name,update.message.text,driver.meta['first_name']))   
            if update.message.text==u'\U0001f44d Check In':
                bot.logger.info("Sending Checkin button")
                update.message.reply_text("Starting checkin process",reply_markup = telegram.ReplyKeyboardRemove())
                keyboard = [[telegram.InlineKeyboardButton("Yes", callback_data='1'),
                     telegram.InlineKeyboardButton("No", callback_data='2')]]
                update.message.reply_text("Do you have a vehicle with you?",reply_markup=telegram.InlineKeyboardMarkup(keyboard))
                #update.message.reply_text(text="CheckIn",reply_markup=telegram.ReplyKeyboardMarkup(location_keyboard))
                
            if update.message.text==u'\U0001f44b Check Out':
                bot.logger.info("Sending CheckOut button")
                update.message.reply_text(text="CheckOut",reply_markup=telegram.ReplyKeyboardMarkup(location_keyboard))
            
            if update.message.text==u'\U000025b6 Open Duty Slip':
       
                bot.logger.info(u"Driver {} opened a duty slip".format(driver.meta['first_name']))
                
            if not update.message.text:
                bot.logger.info("Hmm...no text, could this be a location???")
                if update.message.location:    
                    bot.logger.info("Yup, location it is!")
                    location=update.message.location.to_json()
                    timestamp=update.message.date
                    reply_markup = telegram.ReplyKeyboardRemove()
                    try:
                        if update.message.reply_to_message.text.startswith("Check In"):
                            locupdate=new_locationupdate(driver,location,timestamp,logger=bot.logger)
                            locupdate.save()
                            driver.checkedin=True
                            driver.save()
                            update.message.reply_text(text="Check in from location {} at time {} successfull".format(location,timestamp.strftime("%Y-%m-%d %H:%M:%S")),reply_markup=reply_markup)
                        
                        if update.message.reply_to_message.text=="CheckOut":
                            locupdate=new_locationupdate(driver,location,timestamp,checkin=False,logger=bot.logger)
                            locupdate.save()
                            driver.checkedin=False
                            driver.save()
                            update.message.reply_text(text="Check out from location {} at time {} successfull".format(location,timestamp.strftime("%Y-%m-%d %H:%M:%S")),reply_markup=reply_markup)
                        
                    except:
                        update.message.reply_text(text="Location update from location {} at time {} failed! Please try again (mobile only)".format(location,timestamp.strftime("%Y-%m-%d %H:%M:%S")),reply_markup=reply_markup)        
                    send_keyboard(bot,driver_base_keyboard,update.message.chat.id)
        except Exception as e:
            logger.info("Choked! "+repr(e))
        '''
