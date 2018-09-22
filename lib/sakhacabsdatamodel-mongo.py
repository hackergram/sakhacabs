#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 21:52:07 2018

@author: arjun
"""

import jsonobject
from couchdbkit import *

class User(Document):
    role = StringProperty()
    telegram_id=IntegerProperty()
    meta = DictProperty()
class LocationUpdate(Document):
    driver_id=StringProperty()
    timestamp=DateTimeProperty(exact=True)
    location=StringProperty()
    checkin=BooleanProperty()
    vehicle_id=StringProperty()
    handoff=StringProperty()
class DutySlip(Document):
    driver_id=StringProperty()
    created_time=DateTimeProperty()
    vehicle_id=StringProperty()
    dutyslip_id=StringProperty()
    open_time=DateTimeProperty()
    close_time=DateTimeProperty()
    open_kms=IntegerProperty()
    close_kms=IntegerProperty()
    verified_by=DictProperty()
class Vehicle(Document):
    vehicle_num=StringProperty()
    vehicle_meta = DictProperty()


'''
class User(jsonobject.JsonObject):
    role = jsonobject.StringProperty()
    telegram_id=jsonobject.IntegerProperty()
    meta = jsonobject.DictProperty()
class LocationUpdate(jsonobject.JsonObject):
    driver_id=jsonobject.StringProperty()
    timestamp=jsonobject.DateTimeProperty()
    location=jsonobject.StringProperty()
    checkin=jsonobject.BooleanProperty()
    vehicle_id=jsonobject.StringProperty()
    handoff=jsonobject.StringProperty()
class DutySlip(jsonobject.JsonObject):
    driver_id=jsonobject.StringProperty()
    created_time=jsonobject.DateTimeProperty()
    vehicle_id=jsonobject.StringProperty()
    dutyslip_id=jsonobject.StringProperty()
    open_time=jsonobject.DateTimeProperty()
    close_time=jsonobject.DateTimeProperty()
    open_kms=jsonobject.IntegerProperty()
    close_kms=jsonobject.IntegerProperty()
    verified_by=jsonobject.DictProperty()
class Vehicle(jsonobject.JsonObject):
    vehicle_num=jsonobject.StringProperty()
    vehicle_meta = jsonobject.DictProperty()
'''

    