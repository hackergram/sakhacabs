#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 21:52:07 2018

@author: arjun
"""

from mongoengine import Document, fields, DynamicDocument
import datetime
class User(DynamicDocument):
    role = fields.StringField()
    telegram_id=fields.IntField(unique=True)
    mobile_num=fields.StringField(unique=True)

class Driver(DynamicDocument):
    driver_id=fields.StringField(unique=True,required=True)
    mobile=fields.StringField()
    tgid=fields.IntField()
    
class Customer(DynamicDocument):
    cust_id=fields.StringField(unique=True,required=True)
    cust_type=fields.StringField()
    mobile_num=fields.StringField()
    tgid=fields.IntField()
    
class Vehicle(DynamicDocument):
    vehicle_id=fields.IntField(umique=True,required=True) 
    driver=fields.ReferenceField(Driver)
    
class Booking(DynamicDocument):
    booking_id=fields.StringField(required=True)
    passenger_detail=fields.StringField()
    passenger_mobile=fields.StringField()
    created_timestamp=fields.DateTimeField(default=datetime.datetime.utcnow())    
    pickup_timestamp=fields.DateTimeField()
    pickup_location=fields.StringField()
    drop_location=fields.StringField()
    num_passengers=fields.IntField()
    product_id = fields.StringField()
    cust_id=fields.StringField()
    booking_channel=fields.StringField()

class Product(DynamicDocument):
    product_id=fields.StringField(unique=True,required=True)
    
class LocationUpdate(Document):
    driver=fields.ReferenceField(Driver,required=True)
    timestamp=fields.DateTimeField(required=True)
    location=fields.StringField()
    checkin=fields.BooleanField()
    vehicle=fields.ReferenceField(Vehicle)
    handoff=fields.ReferenceField(User)
    
class DutySlip(Document):
    driver=fields.ReferenceField(Driver)
    created_time=fields.DateTimeField(default=datetime.datetime.utcnow())
    vehicle=fields.ReferenceField(Vehicle)
    dutyslip_id=fields.StringField()
    open_time=fields.DateTimeField()
    close_time=fields.DateTimeField()
    open_kms=fields.IntField()
    close_kms=fields.IntField()
    
class Trip(Document):
    created_timestamp=fields.DateTimeField(default=datetime.datetime.utcnow())    
    frm=fields.StringField()
    to=fields.StringField()    
    pickup_time=fields.DateTimeField()
    bookings=fields.ListField(fields.ReferenceField(Booking))
    dutyslips=fields.ListField(fields.ReferenceField(DutySlip))
    