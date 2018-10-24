#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 21:52:07 2018

@author: arjun
"""

from mongoengine import Document, fields, DynamicDocument
import datetime
import bson,json
from flask_mongoengine import QuerySet
class CustomQuerySet(QuerySet):
         def to_json(self):
            return "[%s]" % (",".join([doc.to_json() for doc in self]))


class Driver(DynamicDocument):
    driver_id=fields.StringField(unique=True,required=True)
    mobile_num=fields.StringField()
    tgid=fields.IntField()
    def __repr__(self):
		return "Driver (%r)" %(self.driver_id)
class Customer(DynamicDocument):
    cust_id=fields.StringField(unique=True,required=True)
    cust_type=fields.StringField()
    mobile_num=fields.StringField()
    tgid=fields.IntField()
    
class Vehicle(DynamicDocument):
    vehicle_id=fields.StringField(unique=True,required=True) 
    driver_id=fields.StringField()
    def __repr__(self):
		return "Vehicle (%r)" %(self.vehicle_id)
class Booking(DynamicDocument):
    booking_id=fields.StringField(required=True)
    passenger_detail=fields.StringField()
    passenger_mobile=fields.StringField()
    created_timestamp=fields.DateTimeField(default=datetime.datetime.utcnow)    
    pickup_timestamp=fields.DateTimeField()
    pickup_location=fields.StringField()
    drop_location=fields.StringField()
    num_passengers=fields.IntField()
    product_id = fields.StringField()
    cust_id=fields.StringField()
    booking_channel=fields.StringField()
    def __repr__(self):
		return "Booking (%r)" %(self.booking_id)
class Product(DynamicDocument):
    product_id=fields.StringField(unique=True,required=True)
    
class LocationUpdate(Document):
    driver_id=fields.StringField(required=True)
    timestamp=fields.DateTimeField(required=True)
    location=fields.StringField()
    checkin=fields.BooleanField()
    vehicle_id=fields.StringField()
    handoff=fields.StringField()
    
class Assignment(Document):
    created_timestamp=fields.DateTimeField(default=datetime.datetime.utcnow)    
    reporting_timestamp=fields.DateTimeField()
    reporting_location=fields.StringField()
    drop_location=fields.StringField()
    bookings=fields.SortedListField(fields.ReferenceField(Booking))
    meta = {'queryset_class':CustomQuerySet}    
    def to_json(self):
        data=self.to_mongo()
        data['bookings']=[json.loads(booking.to_json()) for booking in self.bookings]
        return bson.json_util.dumps(data)
    

class DutySlip(Document):
    driver=fields.StringField(required=True)
    created_time=fields.DateTimeField(default=datetime.datetime.utcnow)
    vehicle=fields.StringField()
    dutyslip_id=fields.StringField()
    open_time=fields.DateTimeField()
    close_time=fields.DateTimeField()
    open_kms=fields.IntField()
    close_kms=fields.IntField()
    assignment=fields.ReferenceField(Assignment)
    
