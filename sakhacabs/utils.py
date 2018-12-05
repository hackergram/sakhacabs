#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 10:43:19 2018

@author: arjun
"""

import random,datetime,re
charstring="ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789"
UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
nospec=re.compile(r"[^A-Za-z0-9 '-]+")

def ran_gen(size, chars=charstring): 
    return ''.join(random.choice(chars) for x in range(size))


def new_booking_id():
    booking_id=datetime.datetime.now().strftime("%y%m%d")+ran_gen(4)
    return booking_id

def get_utc_ts(ts):
    adjts = ts + UTC_OFFSET_TIMEDELTA
    return adjts

def get_local_ts(ts):
    adjts = ts - UTC_OFFSET_TIMEDELTA
    return adjts

def get_ts_string(x):
	return datetime.datetime.fromtimestamp((x['$date']+1)/1000).strftime("%Y-%m-%d %H:%M:%S")

def get_ts(x):
	return datetime.datetime.fromtimestamp((x['$date']+1)/1000)
