#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 21:52:07 2018

@author: arjun
"""

from mongoengine import Document, EmbeddedDocument, fields, DynamicDocument

class User(DynamicDocument):
    role = fields.StringField()
    telegram_id=fields.IntField(unique=True)
    mobile_num=fields.StringField(unique=True)
    
class Vehicle(DynamicDocument):
    vehicle_num=fields.StringField() 
    driver=fields.ReferenceField(User)
class Booking(DynamicDocument):
    booking_id=fields.StringField(unique=True)
    passenger_name=fields.StringField()
    passenger_phone=fields.StringField()
    pickup_timestamp=fields.DateTimeField()
    pickup_location=fields.StringField()
    drop_location=fields.StringField()
    num_passengers=fields.IntField()
    product_code = fields.StringField()
    cust_id=fields.StringField()

class Product(DynamicDocument):
    product_code=fields.StringField(unique=True,required=True)
    product_price=fields.StringField()   


class LocationUpdate(Document):
    driver=fields.ReferenceField(User)
    timestamp=fields.DateTimeField()
    location=fields.StringField()
    checkin=fields.BooleanField()
    vehicle=fields.ReferenceField(Vehicle)
    handoff=fields.ReferenceField(User)
    


class DutySlip(Document):
    driver=fields.ReferenceField(User)
    created_time=fields.DateTimeField()
    vehicle=fields.ReferenceField(Vehicle)
    dutyslip_id=fields.StringField()
    open_time=fields.DateTimeField()
    close_time=fields.DateTimeField()
    open_kms=fields.IntField()
    close_kms=fields.IntField()
    verified_by=fields.ReferenceField(User)
class Trip(Document):
    trip_from=fields.StringField()
    trip_to=fields.StringField()    
    trip_pickup_time=fields.DateTimeField()
    trip_bookings=fields.ListField(fields.ReferenceField(Booking))
    trip_dutyslips=fields.ListField(fields.ReferenceField(DutySlip))
    
    
'''
class Customer(Document):
    cust_id=fields.StringField()
    cust_type=fields.StringField()
    cust_mobile=fields.StringField()
    cust_telegramid=fields.IntField()
    cust_meta=fields.DynamicField()
'''
 
    