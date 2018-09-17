#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import sys,datetime
sys.path.append("/opt/xetrapal")
import xetrapal
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)


sys.path.append("/opt/sakhacabs/lib")
from sakhacabsfunctions import *
#from driversakhabot import *

check_in_text=u'\U0001f44d Check In'
check_out_text=u'\U0001f44b Check Out'
open_duty_slip_text=u'\U000025b6 Open Duty Slip'
add_handoff_text=u'\U0001F91D Handoff'
add_vehicle_text=u'\U0001F695 Vehicle'
send_location_text=u'\U0001F4CD Send Location'
submit_text=u'\U00002714 Submit'
cancel_text=u'\U0000274C Cancel'
driver_base_keyboard = [[check_in_text, check_out_text ],[open_duty_slip_text]]
location_update_keyboard = [[add_handoff_text, add_vehicle_text ],[send_location_text],[submit_text,cancel_text]]    
location_keyboard=[[{'text':send_location_text,'request_location':True}]]
#yes_no_keyboard = [[telegram.InlineKeyboardButton("Yes", callback_data='Yes'),telegram.InlineKeyboardButton("No", callback_data='No')]]



sakhacabsxpal=xetrapal.Xetrapal(configfile="/home/arjun/sakhacabs/sakhacabsxpal.conf")
driverbotconfig=xetrapal.karma.load_config(configfile="/home/arjun/sakhacabs/driversakhabot.conf")
driversakhabot=xetrapal.telegramastras.XetrapalTelegramBot(config=driverbotconfig,logger=sakhacabsxpal.logger)

logger=driversakhabot.logger
MENU_CHOICE, TYPING_REPLY, TYPING_CHOICE,LOCATION_CHOICE = range(4)




def facts_to_str(user_data):
    facts = list()
    logger.info("Converting facts to string")
    for key, value in user_data.items():
        facts.append(u'{} - {}'.format(key, value))
    logger.info("Converted facts to string")
    return "\n".join(facts).join(['\n', '\n'])

def main_menu(bot, update):
    user_data={}
    user_data['driver']=get_driver_by_tgid(update.message.from_user.id)
    logger.info(u"{}".format(user_data))
    if user_data['driver']==None:
        update.message.reply_text("Sorry this service is for Sakha Cabs Drivers Only!")
        return ConversationHandler.END
    logger.info("Main Menu presented to driver {}".format(user_data['driver'].meta['first_name']))
    markup = ReplyKeyboardMarkup(driver_base_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Hi! Welcome to the Sakha Driver Assistant."
        "What would you like to do?",
        reply_markup=markup)
    
    return MENU_CHOICE

def open_duty_slip(bot, update, user_data):
    text=update.message.text
    logger.info("u{}".format(text))

def location_update_menu(bot, update, user_data):
    user_data['driver']=get_driver_by_tgid(update.message.from_user.id)
    user_data['vehicle']=None
    user_data['handoff']=None
    user_data['location']=None
    logger.info(u"{}".format(user_data))
    #user_data={}
    if user_data['driver']==None:
        update.message.reply_text("Sorry this service is for Sakha Cabs Drivers Only!")
        return ConversationHandler.END

    text = update.message.text
    user_data['choice'] = text
    if text==check_in_text:
        user_data['checkin']=True
    else:
        user_data['checkin']=False
    logger.info(u"{}".format(user_data))
    markup=ReplyKeyboardMarkup(location_update_keyboard,one_time_keyboard=True)
    if user_data['checkin']==True:
        update.message.reply_text(check_in_text,reply_markup=markup)
    else:
        update.message.reply_text(check_out_text,reply_markup=markup)
    
    return LOCATION_CHOICE


def handoff_vehicle(bot, update,user_data):
    text = update.message.text
    user_data['choice'] = text
    logger.info(u"{}".format(user_data))
    update.message.reply_text(u'{} Details?'.format(text))
    return TYPING_CHOICE


def get_location(bot, update,user_data):
    text = update.message.text
    user_data['choice'] = text
    logger.info(u"{}".format(user_data))
    markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)
    update.message.reply_text(u'{}'.format(text),reply_markup=markup)
    return TYPING_CHOICE


def cancel_location_update(bot, update, user_data):
    logger.info(u"{}".format(user_data))
    markup = ReplyKeyboardMarkup(driver_base_keyboard, one_time_keyboard=True)
    
    #del user_data['choice']

    update.message.reply_text(u'Cancelled!', reply_markup=markup)
    for key in user_data.keys():
        del user_data[key]
    return MENU_CHOICE

def submit_location_update(bot, update, user_data):
    
    logger.info(u"{}".format(user_data))
    logger.info(user_data['driver'])
    markup = ReplyKeyboardMarkup(driver_base_keyboard, one_time_keyboard=True)
    
    #del user_data['choice']
    
    try:
        location=user_data['location']
        handoff=user_data['handoff']
        logger.info(u"{}".format(user_data))
        location_update=new_locationupdate(user_data['driver'],location,update.message.date,user_data['checkin'],vehicle=user_data['vehicle'],handoff=handoff)
        location_update.save()
        update.message.reply_text(u"Saved!"
                                  u"{}"
                                  u"What would you like to do".format(facts_to_str(user_data)), reply_markup=markup)
    except Exception as e:
        logger.error("Errored "+str(e))
        update.message.reply_text(u"Could Not Submit, Try again"
                                  u"{}"
                                  u"What would you like to do".format(facts_to_str(user_data)), reply_markup=markup)
    for key in user_data.keys():
        del user_data[key]
    return MENU_CHOICE



def received_location_information(bot, update, user_data):
    if update.message.text:
        text = update.message.text
    
    category = user_data['choice']
    if category==add_handoff_text:
        if update.message.contact:
            contact=update.message.contact
            user_data["handoff"] = contact
        else:
            user_data["handoff"]=None
    if category==add_vehicle_text:
        if update.message.text:
            text = update.message.text
            vehicle=get_vehicle_by_vnum(text)
            user_data["vehicle"] = vehicle
        else:
            user_data["vehicle"]=None
    if category==send_location_text:
        if update.message.location:
            location = update.message.location
            user_data["location"] = location
        else:
            user_data["location"] = None
    logger.info(u"{}".format(user_data))
    markup = ReplyKeyboardMarkup(location_update_keyboard, one_time_keyboard=True)
    
    del user_data['choice']

    update.message.reply_text(u"Neat! Just so you know, this is what you already told me:"
                              u"{}"
                              u"You can tell me more, or change your opinion on something.".format(
                                  facts_to_str(user_data)), reply_markup=markup)

    return LOCATION_CHOICE


def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def setup():
    # Create the Updater and pass it your bot's token.
    updater=driversakhabot.updater
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', main_menu)],

        states={
            MENU_CHOICE: [RegexHandler('^('+check_in_text+'|'+check_out_text+')$',
                                    location_update_menu,
                                    pass_user_data=True),
                       RegexHandler('^('+open_duty_slip_text+')$',
                                    open_duty_slip,
                                    pass_user_data=True),
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           received_location_information,
                                           pass_user_data=True),
                            MessageHandler(Filters.location,
                                           received_location_information,
                                           pass_user_data=True),
                            MessageHandler(Filters.contact,
                                           received_location_information,
                                           pass_user_data=True),
                            ],
                                           

            LOCATION_CHOICE: [RegexHandler('^('+add_handoff_text+'|'+add_vehicle_text+')$',
                                    handoff_vehicle,
                                    pass_user_data=True),
                              RegexHandler('^('+send_location_text+')$',
                                    get_location,
                                    pass_user_data=True),             
                              RegexHandler('^('+submit_text+')$',
                                    submit_location_update,
                                    pass_user_data=True),
                              RegexHandler('^('+cancel_text+')$',
                                    cancel_location_update,
                                    pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    #updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    #updater.idle()

def single_update():
    p=driversakhabot.get_latest_updates()
    for update in p:
        driversakhabot.updater.dispatcher.process_update(update)
    return p


#if __name__ == '__main__':
setup()
    