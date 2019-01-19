#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 10:43:19 2018

@author: arjun
"""

import random
import datetime
import re
charstring = "ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789"
UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
nospec = re.compile(r"[^A-Za-z0-9\n @.'\-,\/\(\):'#&]+")
notnum = re.compile(r"[^0-9]+")
validstatuses = ['new', 'assigned', 'open', 'closed', 'cancelled', 'verified']
defaultnotificationprefs = {'new': [], 'assigned': [], 'open': [], 'closed': [], 'cancelled': []}


def validate_dict(dictionary, required_keys=[], string_keys=[], mobile_nums=[], emails=[], numbers=[], dates=[]):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid dictionary"
    for key in required_keys:
        if key not in dictionary.keys():
            validation['message'] = "{} - missing required field".format(key)
            validation['status'] = False
        elif dictionary[key] is None or dictionary[key] == "":
            validation['message'] = "{} - can't be None or blank".format(key)
            validation['status'] = False
    for key in string_keys:
        if key in dictionary.keys():
            if nospec.search(str(dictionary[key])):
                validation['message'] = "{} - has special character {}".format(
                    key, nospec.search(str(dictionary[key])))
                validation['status'] = False
    for key in mobile_nums:
        if key in dictionary.keys():
            if dictionary[key] == "":
                validation['message'] = "Empty mobile number"
                validation['status'] = False
            if len(dictionary[key]) > 12:
                validation['message'] = "{} too long a mobile number".format(dictionary[key])
                validation['status'] = False
            if notnum.search(dictionary[key]):
                validation['message'] = "{} non numeric in mobile number".format(dictionary[key])
                validation['status'] = False
    for key in numbers:  # CHANGELOG #11 - AV - For #273
        try:
            if key in dictionary.keys():
                value = float(dictionary[key])
        except Exception as e:
            validation['message'] = str(e)
            validation['status'] = False
    for key in dates:  # CHANGELOG #11 - AV - For #273
        try:
            if key in dictionary.keys():
                value = datetime.datetime.strptime(dictionary[key], "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            validation['message'] = str(e)
            validation['status'] = False
    return validation


def ran_gen(size, chars=charstring):
    return ''.join(random.choice(chars) for x in range(size))


def new_invoice_id():
    booking_id = datetime.datetime.now().strftime("%Y%m%d") + "-" + ran_gen(4)
    return booking_id


def new_booking_id():
    booking_id = datetime.datetime.now().strftime("%y%m%d") + ran_gen(4)
    return booking_id


def get_utc_ts(ts):
    adjts = ts + UTC_OFFSET_TIMEDELTA
    return adjts


def get_local_ts(ts):
    adjts = ts - UTC_OFFSET_TIMEDELTA
    return adjts


def get_ts_string(x):
    return datetime.datetime.fromtimestamp((x['$date'] + 1) / 1000).strftime("%Y-%m-%d %H:%M:%S")


def get_ts(x):
    return datetime.datetime.fromtimestamp((x['$date'] + 1) / 1000)
