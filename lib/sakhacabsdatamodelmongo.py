#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 21:52:07 2018

@author: arjun
"""

from mongoengine import Document, EmbeddedDocument, fields




class User(Document):
    role = fields.StringField()
    telegram_id=fields.IntField()
    metadata = fields.DynamicField()
class LocationUpdate(Document):
    driver_id=fields.DynamicField()
    timestamp=fields.DateTimeField()
    location=fields.StringField()
    checkin=fields.BooleanField()
    vehicle_id=fields.DynamicField()
    handoff=fields.DynamicField()
class DutySlip(Document):
    driver_id=fields.StringField()
    created_time=fields.DateTimeField()
    vehicle_id=fields.StringField()
    dutyslip_id=fields.StringField()
    open_time=fields.DateTimeField()
    close_time=fields.DateTimeField()
    open_kms=fields.IntField()
    close_kms=fields.IntField()
    verified_by=fields.DictField()
class Vehicle(Document):
    vehicle_num=fields.StringField()
    vehicle_meta = fields.DynamicField()


'''
class User(jsonobject.JsonObject):
    role = jsonobject.fields.StringField()
    telegram_id=jsonobject.fields.IntField()
    meta = jsonobject.fields.DictField()
class LocationUpdate(jsonobject.JsonObject):
    driver_id=jsonobject.fields.StringField()
    timestamp=jsonobject.fields.DateTimeField()
    location=jsonobject.fields.StringField()
    checkin=jsonobject.BooleanProperty()
    vehicle_id=jsonobject.fields.StringField()
    handoff=jsonobject.fields.StringField()
class DutySlip(jsonobject.JsonObject):
    driver_id=jsonobject.fields.StringField()
    created_time=jsonobject.fields.DateTimeField()
    vehicle_id=jsonobject.fields.StringField()
    dutyslip_id=jsonobject.fields.StringField()
    open_time=jsonobject.fields.DateTimeField()
    close_time=jsonobject.fields.DateTimeField()
    open_kms=jsonobject.fields.IntField()
    close_kms=jsonobject.fields.IntField()
    verified_by=jsonobject.fields.DictField()
class Vehicle(jsonobject.JsonObject):
    vehicle_num=jsonobject.fields.StringField()
    vehicle_meta = jsonobject.fields.DictField()
'''

    