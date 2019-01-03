# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
from sakhacabs.xpal import *
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from telegram import ReplyKeyboardMarkup
import xetrapal
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

import sys
import datetime
sys.path.append("/opt/xetrapal")


check_in_text = u'\U0001f44d Check In'
check_out_text = u'\U0001f44b Check Out'
open_duty_slip_text = u'\U000025b6 Open Duty Slip'
add_handoff_text = u'\U0001F91D Handoff'
add_vehicle_text = u'\U0001F695 Vehicle'
send_location_text = u'\U0001F4CD Send Location'
send_contact_text = u'\U0001F4CD Send Contact'
submit_text = u'\U00002714 Submit'
cancel_text = u'\U0000274C Cancel'
start_duty_text = u'\U0001f3c1 Start Duty'
stop_duty_text = u'\U0001f6a9 Stop Duty'
cash_text = u'\U0001f6a9 Cash'
credit_text = u'\U0001f6a9 Credit'

driver_base_keyboard = [[check_in_text, check_out_text], [open_duty_slip_text]]
location_update_keyboard = [[add_handoff_text, add_vehicle_text], [
    send_location_text], [submit_text, cancel_text]]
location_keyboard = [[{'text': send_location_text, 'request_location': True}]]
contact_keyboard = [[{'text': send_contact_text, 'request_contact': True}]]
dutyslip_start_keyboard = [[start_duty_text], [cancel_text]]
dutyslip_stop_keyboard = [[stop_duty_text], [cancel_text]]
dutyslip_submit_keyboard = [[submit_text], [cancel_text]]
payment_mode_keyboard = [[cash_text], [credit_text]]
#yes_no_keyboard = [[telegram.InlineKeyboardButton("Yes", callback_data='Yes'),telegram.InlineKeyboardButton("No", callback_data='No')]]

driverbotconfig = xetrapal.karma.load_config(
    configfile="/opt/sakhacabs-appdata/driversakhabot.conf")
driversakhabot = xetrapal.telegramastras.XetrapalTelegramBot(
    config=driverbotconfig, logger=sakhacabsxpal.logger)

logger = driversakhabot.logger
GETMOBILE, MENU_CHOICE, TYPING_REPLY, TYPING_CHOICE, LOCATION_CHOICE, DUTYSLIP_CHOICE, DUTYSLIP_MENU, DUTYSLIP_OPEN, DUTYSLIP_FORM = range(
    9)


def facts_to_str(user_data):
    facts = list()
    logger.info("Converting facts to string")
    for key, value in user_data.items():
        facts.append(u'{} - {}'.format(key, repr(value)))
    logger.info("Converted facts to string")
    return "\n".join(facts).join(['\n', '\n'])


def main_menu(bot, update):
    user_data = {}
    try:
        user_data['driver'] = get_driver_by_tgid(update.message.from_user.id)
        logger.info(u"{}".format(user_data))
        if user_data['driver'] is None:
            update.message.reply_text(
                "Sorry this service is for Sakha Cabs Drivers Only!")
            markup = ReplyKeyboardMarkup(contact_keyboard)
            update.message.reply_text(
                "If you are logging in for the first time, please share your mobile number", reply_markup=markup)
            # return ConversationHandler.END
            return GETMOBILE
        logger.info("Main Menu presented to driver {}".format(
            user_data['driver'].driver_id))
        markup = ReplyKeyboardMarkup(
            driver_base_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Hi! Welcome to the Sakha Driver Assistant."
            "What would you like to do?",
            reply_markup=markup)
        return MENU_CHOICE
    except Exception as e:
        logger.info("{} {}".format(type(e), str(e)))


def open_duty_slip(bot, update, user_data):
    try:
        logger.info("Opening Duty Slip {},{}".format(
            update.message.text.split(" ")[1], user_data))
        markup = ReplyKeyboardMarkup(
            dutyslip_start_keyboard, one_time_keyboard=True)
        dutyslip = documents.DutySlip.objects.with_id(
            update.message.text.split(" ")[1])
        user_data['current_duty_slip'] = dutyslip
        logger.info("Curr DS ={}".format(dutyslip))
        replytext = "Reporting Time: " + utils.get_local_ts(dutyslip.assignment.reporting_timestamp).strftime(
            "%Y-%m-%d %H:%M:%S") + "\n" + "Reporting Location: " + dutyslip.assignment.reporting_location + "\nBookings:"
        if hasattr(dutyslip, "vehicle"):
            replytext = "Vehicle: {}\n".format(dutyslip.vehicle) + replytext

        for booking in dutyslip.assignment.bookings:
            replytext = replytext + "\nBooking ID: " + booking.booking_id + \
                "\nPassenger Detail: " + booking.passenger_detail
            if booking.drop_location:
                replytext = replytext + "\nDrop Localtion: " + booking.drop_location  # fixes 117
        # replytext=replytext+"\n"+repr(dutyslip)
        update.message.reply_text(replytext,
                                  reply_markup=markup)
        # return MENU_CHOICE
        return DUTYSLIP_MENU
    except Exception as e:
        logger.info("{} {}".format(type(e), str(e)))
        markup = ReplyKeyboardMarkup(
            driver_base_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Could not open duty slip", reply_markup=markup)
    return MENU_CHOICE


def get_duty_slips(bot, update, user_data):
    user_data['driver'] = get_driver_by_tgid(update.message.from_user.id)
    user_data['vehicle'] = None
    user_data['handoff'] = None
    user_data['location'] = None
    # text=update.message.tex
    logger.info("Fetching Duty Slips {}".format(user_data))
    try:
        user_data['duties'] = get_duties_for_driver(
            user_data['driver'].driver_id)
        if not user_data['duties'] or user_data['duties'] == []:
            update.message.reply_text("No Assignments As of Now")
            return MENU_CHOICE
        logger.info("{}".format(user_data['duties']))
        updatekeys = []
        for duty in user_data['duties']:
            logger.info("{}".format(duty.to_json()))
            keytext = ["ID: " + unicode(duty.id) + " " + unicode(utils.get_local_ts(
                duty.assignment.reporting_timestamp).strftime("%Y-%m-%d %H:%M:%S"))]
            updatekeys.append(keytext)
            logger.info("{}".format(updatekeys))
        keytext = [cancel_text]
        updatekeys.append(keytext)
        markup = ReplyKeyboardMarkup(updatekeys)
        update.message.reply_text(
            "Select Duty Slip to open", reply_markup=markup)
        return DUTYSLIP_CHOICE
    except Exception as e:
        logger.error(str(e))
        update.message.reply_text("An error occurred")
        return MENU_CHOICE


def location_update_menu(bot, update, user_data):
    user_data['driver'] = get_driver_by_tgid(update.message.from_user.id)
    user_data['vehicle'] = None
    user_data['handoff'] = None
    user_data['location'] = None
    logger.info(u"{}".format(user_data))
    # user_data={}
    if user_data['driver'] is None:
        update.message.reply_text(
            "Sorry this service is for Sakha Cabs Drivers Only!")
        return ConversationHandler.END
    text = update.message.text
    user_data['choice'] = text
    if text == check_in_text:
        user_data['checkin'] = True
    else:
        user_data['checkin'] = False
    logger.info(u"{}".format(user_data))
    markup = ReplyKeyboardMarkup(
        location_update_keyboard, one_time_keyboard=True)
    if user_data['checkin'] == True:
        update.message.reply_text(check_in_text, reply_markup=markup)
    else:
        update.message.reply_text(check_out_text, reply_markup=markup)
    return LOCATION_CHOICE


def handoff_vehicle(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    logger.info(u"{}".format(user_data))
    update.message.reply_text(u'{} Details?'.format(text))
    return TYPING_CHOICE


def get_location(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    logger.info(u"{}".format(user_data))
    markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)
    update.message.reply_text(u'{}'.format(text), reply_markup=markup)
    return TYPING_CHOICE


def set_mobile(bot, update, user_data):
    logger.info(u"{}".format(update.message.contact))
    driver = get_driver_by_mobile(
        update.message.contact.phone_number.lstrip("+"))
    if driver:
        driver.tgid = update.message.contact.user_id
        driver.save()
        user_data['driver'] = driver
        logger.info("Main Menu presented to driver {}".format(
            user_data['driver'].driver_id))
        markup = ReplyKeyboardMarkup(
            driver_base_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            "Hi! Welcome to the Sakha Driver Assistant."
            "What would you like to do?",
            reply_markup=markup)
        return MENU_CHOICE
    else:
        update.message.reply_text("Sorry, you don't seem to be listed!")
        return ConversationHandler.END


def cancel(bot, update, user_data):
    logger.info(u"Cancelling Update {}".format(user_data))
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
        location = user_data['location']
        handoff = user_data['handoff']
        logger.info(u"{} {}".format(update.message.date, user_data))
        location_update = new_locationupdate(user_data['driver'], update.message.date,
                                             user_data['checkin'], location=location,
                                             vehicle=user_data['vehicle'], handoff=handoff)
        location_update.save()
        update.message.reply_text(u"Saved!"
                                  u"{}"
                                  u"What would you like to do".format(repr(location_update)), reply_markup=markup)
    except Exception as e:
        logger.error("Errored " + str(e))
        update.message.reply_text(u"Could Not Submit, Try again"
                                  u"{}"
                                  u"What would you like to do".format(facts_to_str(user_data)), reply_markup=markup)
    for key in user_data.keys():
        del user_data[key]
    return MENU_CHOICE


def received_dutyslip_information(bot, update, user_data):
    logger.info("Received ds info")
    logger.info("{}".format(update.message))
    if update.message:
        if update.message.text:
            if update.message.text == cash_text:
                text = "cash"
            elif update.message.text == credit_text:
                text = "credit"
            else:
                text = update.message.text
    logger.info("Received message {} and user data - {}".format(text, user_data))
    field = user_data['field']
    if field == "dutyslipnum":
        try:
            if utils.nospec.search(text):
                markup = ReplyKeyboardMarkup(driver_base_keyboard)
                update.message.reply_text(
                    "No special characters in duty slip number, please start over", reply_markup=markup)
                return MENU_CHOICE
            user_data['current_duty_slip'].dutyslip_id = text
            user_data['field'] = "openkms"
            logger.info("{}".format(user_data))
            update.message.reply_text("Open Kms?")
            return DUTYSLIP_FORM
        except Exception as e:
            logger.error(str(e))
            markup = ReplyKeyboardMarkup(driver_base_keyboard)
            update.message.reply_text(
                "An error occurred, please start over", reply_markup=markup)
            return MENU_CHOICE

    if field == "openkms":
        try:
            if utils.notnum.search(text):
                update.message.reply_text(
                    "Numbers only for open kms\nOpen Kms?")
                return DUTYSLIP_FORM
            user_data['current_duty_slip'].open_kms = float(text)
            user_data['current_duty_slip'].open_time = utils.get_utc_ts(
                update.message.date)
            # user_data['current_duty_slip'].status = "open"
            # user_data['current_duty_slip'].save()
            # user_data['current_duty_slip'].assignment.status = "open"
            # user_data['current_duty_slip'].assignment.save()
            update_dutyslip_status(user_data['current_duty_slip'].id, "open")
            for booking in user_data['current_duty_slip'].assignment.bookings:
                booking.status = "open"
                booking.save()
            user_data['field'] = "closekms"
            logger.info("{}".format(user_data))
            markup = ReplyKeyboardMarkup(
                dutyslip_stop_keyboard, one_time_keyboard=True)
            update.message.reply_text(
                "Trip in progress. Stop Trip?", reply_markup=markup)
            return DUTYSLIP_OPEN
        except Exception as e:
            logger.error(str(e))
            markup = ReplyKeyboardMarkup(driver_base_keyboard)
            update.message.reply_text(
                "An error occurred, please start over", reply_markup=markup)
            return MENU_CHOICE

    if field == "closekms":
        try:
            if utils.notnum.search(text):
                markup = ReplyKeyboardMarkup(driver_base_keyboard)
                update.message.reply_text(
                    "Numbers only for close kms\nClose Kms?")
                return DUTYSLIP_OPEN
            user_data['current_duty_slip'].close_kms = float(text)
            if user_data['current_duty_slip'].close_kms < user_data['current_duty_slip'].open_kms:
                update.message.reply_text(
                    "Close kms cant be less than open kms, please start over")
                return DUTYSLIP_OPEN
            user_data['current_duty_slip'].close_time = utils.get_utc_ts(
                update.message.date)
            user_data['field'] = "parking"
            logger.info("{}".format(user_data))
            update.message.reply_text("Parking Charges? Enter 0 if none")
            return DUTYSLIP_FORM
        except Exception as e:
            logger.error(str(e))
            markup = ReplyKeyboardMarkup(driver_base_keyboard)
            update.message.reply_text(
                "An error occurred, please start over", reply_markup=markup)
            return MENU_CHOICE

    if field == "parking":
        try:
            if utils.notnum.search(text):
                update.message.reply_text(
                    "Numbers only for parking\nParking Charges? Enter 0 if none")
                return DUTYSLIP_FORM

            user_data['current_duty_slip'].parking_charges = float(text)
            user_data['field'] = "toll"
            logger.info("{}".format(user_data))
            update.message.reply_text("Toll Charges? Enter 0 if none")
            return DUTYSLIP_FORM
        except Exception as e:
            logger.error(str(e))
            markup = ReplyKeyboardMarkup(driver_base_keyboard)
            update.message.reply_text(
                "An error occurred, please start over", reply_markup=markup)
            return MENU_CHOICE

    if field == "toll":
        try:
            if utils.notnum.search(text):
                update.message.reply_text(
                    "Numbers only for toll\nToll Charges? Enter 0 if none")
                return DUTYSLIP_FORM
            user_data['current_duty_slip'].toll_charges = float(text)
            user_data['field'] = "payment_mode"
            logger.info("{}".format(user_data))
            markup = ReplyKeyboardMarkup(
                payment_mode_keyboard, one_time_keyboard=True)
            update.message.reply_text("Payment Mode?", reply_markup=markup)
            return DUTYSLIP_FORM
        except Exception as e:
            logger.error(str(e))
            markup = ReplyKeyboardMarkup(driver_base_keyboard)
            update.message.reply_text(
                "An error occurred, please start over", reply_markup=markup)
            return MENU_CHOICE

    if field == "payment_mode":
        try:
            logger.info("Payment mode is : " + text)
            user_data['current_duty_slip'].payment_mode = text
            logger.info("{}".format(user_data))
            user_data['field'] = "amount"

            update.message.reply_text("Amount Received? Enter 0 if none")

            return DUTYSLIP_FORM
        except Exception as e:
            logger.error(str(e))
            markup = ReplyKeyboardMarkup(driver_base_keyboard)
            update.message.reply_text(
                "An error occurred, please start over", reply_markup=markup)
            return MENU_CHOICE

    if field == "amount":
        try:
            if utils.notnum.search(text):
                update.message.reply_text(
                    "Numbers only for amount\n Amount Received? Enter 0 if none")
                return DUTYSLIP_FORM
            user_data['current_duty_slip'].amount = float(text)
            user_data['field'] = "remarks"
            logger.info("{}".format(user_data))
            update.message.reply_text("Remarks?")

            return DUTYSLIP_FORM
        except Exception as e:
            logger.error(str(e))
            markup = ReplyKeyboardMarkup(driver_base_keyboard)
            update.message.reply_text(
                "An error occurred, please start over", reply_markup=markup)
            return MENU_CHOICE

    if field == "remarks":
        try:
            logger.info("Remarks : " + text)
            user_data['current_duty_slip'].remarks = text
            logger.info("{}".format(user_data))

            markup = ReplyKeyboardMarkup(dutyslip_submit_keyboard)
            # logger.info("{}".format(facts_to_str(user_data['current_duty_slip'].to_json())))
            update.message.reply_text("Trip Details - \n{}\n Submit Trip?".format(
                repr(user_data['current_duty_slip'])), reply_markup=markup)
            return DUTYSLIP_OPEN
        except Exception as e:
            logger.error(str(e))
            markup = ReplyKeyboardMarkup(driver_base_keyboard)
            update.message.reply_text(
                "An error occurred, please start over", reply_markup=markup)
            return MENU_CHOICE


def received_location_information(bot, update, user_data):
    try:
        if update.message.text:
            text = update.message.text
            logger.info("Received message {} and user data - {}".format(text,
                                                                        user_data['choice'] == add_vehicle_text))
        category = user_data['choice']
        #logger.info("Category {}".format(category))
        if category == add_handoff_text:
            if update.message.contact:
                contact = update.message.contact
                user_data["handoff"] = contact
            else:
                user_data["handoff"] = None
        if category == add_vehicle_text:
            logger.info("Adding vehicle")
            if update.message.text:
                text = update.message.text
                vehicle = get_vehicle_by_vid(text)
                try:
                    if vehicle.driver_id is None or vehicle.driver_id == user_data['driver'].id:
                        user_data["vehicle"] = vehicle
                    else:
                        update.message.reply_text(
                            "That vehicle is assigned to someone else")
                        return LOCATION_CHOICE
                except:
                    user_data["vehicle"] = vehicle
            else:
                user_data["vehicle"] = None
        if category == send_location_text:
            logger.info("Received {}".format(update.message))
            if update.message.location:
                location = update.message.location
                user_data["location"] = location.to_json()
            else:
                user_data["location"] = None
        logger.info(u"{}".format(user_data))
        markup = ReplyKeyboardMarkup(
            location_update_keyboard, one_time_keyboard=True)
        del user_data['choice']
        update.message.reply_text(u"Neat! Just so you know, this is what you already told me:"
                                  u"{}"
                                  u"You can tell me more, or change your opinion on something.".format(
                                      facts_to_str(user_data)), reply_markup=markup)

        return LOCATION_CHOICE
    except Exception as e:
        logger.error(str(e))
        markup = ReplyKeyboardMarkup(driver_base_keyboard)
        update.message.reply_text(
            "An error occurred, please start over", reply_markup=markup)
        return MENU_CHOICE


def start_duty(bot, update, user_data):
    try:
        sakhacabsxpal.logger.info("Starting Duty {}".format(
            user_data['current_duty_slip'].to_json()))
        markup = ReplyKeyboardMarkup(dutyslip_stop_keyboard)
        # update.message.reply_text("Trip in progress",
        #    reply_markup=markup)
        user_data['field'] = "dutyslipnum"
        update.message.reply_text("Duty Slip Number?")
        return DUTYSLIP_FORM
    except Exception as e:
        logger.error(str(e))
        markup = ReplyKeyboardMarkup(driver_base_keyboard)
        update.message.reply_text(
            "An error occurred, please start over", reply_markup=markup)
        return MENU_CHOICE

        # return DUTYSLIP_OPEN


def stop_duty(bot, update, user_data):
    try:
        sakhacabsxpal.logger.info("Stopping Duty {}".format(user_data['current_duty_slip'].to_json()))
        # markup = ReplyKeyboardMarkup(dutyslip_stop_keyboard)
        # update.message.reply_text("Trip in progress",
        #    reply_markup=markup)
        # user_data['field']="dutyslipnum"
        update.message.reply_text("Close Kms?")
    except Exception as e:
        logger.error(str(e))
        markup = ReplyKeyboardMarkup(driver_base_keyboard)
        update.message.reply_text(
            "An error occurred, please start over", reply_markup=markup)
        return MENU_CHOICE
        # return DUTYSLIP_OPEN
    return DUTYSLIP_FORM


def submit_duty(bot, update, user_data):
    markup = ReplyKeyboardMarkup(driver_base_keyboard)
    try:
        sakhacabsxpal.logger.info(
            "Submitting Duty {}".format(user_data['current_duty_slip']))
        # user_data['current_duty_slip'].status = "closed"
        # user_data['current_duty_slip'].save()
        update_dutyslip_status(user_datauser_data['current_duty_slip']['current_duty_slip'].id, "closed")
        update.message.reply_text("Trip Saved", reply_markup=markup)
    except Exception as e:
        logger.error(str(e))
        update.message.reply_text(
            "An error occurred, please start over", reply_markup=markup)
    return MENU_CHOICE


def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']
    update.message.reply_text("Bye!")
    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def setup():
    # Create the Updater and pass it your bot's token.
    updater = driversakhabot.updater
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', main_menu)],

        states={
            GETMOBILE: [MessageHandler(Filters.text,
                                       done,
                                       pass_user_data=True),
                        MessageHandler(Filters.contact,
                                       set_mobile,
                                       pass_user_data=True),
                        ],
            MENU_CHOICE: [RegexHandler('^(' + check_in_text + '|' + check_out_text + ')$',
                                       # open_duty_slip,
                                       location_update_menu,
                                       pass_user_data=True),
                          RegexHandler('^(' + open_duty_slip_text + ')$',
                                       get_duty_slips,
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
            DUTYSLIP_FORM: [MessageHandler(Filters.text,
                                           received_dutyslip_information,
                                           pass_user_data=True),
                            RegexHandler('^(' + cash_text + ')$',
                                         received_dutyslip_information,
                                         pass_user_data=True),
                            RegexHandler('^(' + credit_text + ')$',
                                         received_dutyslip_information,
                                         pass_user_data=True),
                            MessageHandler(Filters.location,
                                           received_dutyslip_information,
                                           pass_user_data=True),
                            ],
            DUTYSLIP_CHOICE: [RegexHandler('^(ID: [a-z,0-9,\s]+)',
                                           open_duty_slip,
                                           pass_user_data=True),
                              RegexHandler('^(' + cancel_text + ')$',
                                           cancel,
                                           pass_user_data=True),
                              ],
            DUTYSLIP_MENU: [RegexHandler('^(' + start_duty_text + ')$',
                                         start_duty,
                                         pass_user_data=True),
                            RegexHandler('^(' + cancel_text + ')$',
                                         cancel,
                                         pass_user_data=True),
                            ],
            DUTYSLIP_OPEN: [RegexHandler('^(' + stop_duty_text + ')$',
                                         stop_duty,
                                         pass_user_data=True),
                            RegexHandler('^(' + submit_text + ')$',
                                         submit_duty,
                                         pass_user_data=True),
                            RegexHandler('^(' + cancel_text + ')$',
                                         cancel,
                                         pass_user_data=True),
                            ],
            LOCATION_CHOICE: [RegexHandler('^(' + add_handoff_text + '|' + add_vehicle_text + ')$',
                                           handoff_vehicle,
                                           pass_user_data=True),
                              RegexHandler('^(' + send_location_text + ')$',
                                           get_location,
                                           pass_user_data=True),
                              RegexHandler('^(' + submit_text + ')$',
                                           submit_location_update,
                                           pass_user_data=True),
                              RegexHandler('^(' + cancel_text + ')$',
                                           cancel,
                                           pass_user_data=True),
                              ],
        },
        fallbacks=[RegexHandler('^[dD]one$', done, pass_user_data=True)]
    )
    dp.add_handler(conv_handler)
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    # updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


def single_update():
    p = driversakhabot.get_latest_updates()
    for update in p:
        driversakhabot.updater.dispatcher.process_update(update)
    return p


if __name__ == '__main__':
    setup()
    driversakhabot.updater.start_polling()
    driversakhabot.updater.idle()
