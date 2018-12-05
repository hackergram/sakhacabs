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


class PPrintMixin(object):
    def __str__(self):
        return '<{}: id={!r}>'.format(type(self).__name__, self.id)

    def __repr__(self):
        attrs = []
        for name in self._fields.keys():
            value = getattr(self, name)
            if isinstance(value, (Document, DynamicDocument)):
                attrs.append('\n    {} = {!s},'.format(name, value))
            elif isinstance(value, (datetime.datetime)):
                attrs.append('\n    {} = {},'.format(name, value.strftime("%Y-%m-%d %H:%M:%S")))
            else:
                attrs.append('\n    {} = {!r},'.format(name, value))
        return '<{}: {}\n>'.format(type(self).__name__, ''.join(attrs))


class CustomQuerySet(QuerySet):
         def to_json(self):
            return "[%s]" % (",".join([doc.to_json() for doc in self]))


class Driver(PPrintMixin,DynamicDocument):
    driver_id=fields.StringField(unique=True,required=True)
    mobile_num=fields.StringField()
    tgid=fields.IntField()
    def __repr__(self):
		return "Driver (%r)" %(self.driver_id)
class Customer(PPrintMixin,DynamicDocument):
    cust_id=fields.StringField(unique=True,required=True)
    cust_type=fields.StringField()
    mobile_num=fields.StringField()
    tgid=fields.IntField()
   
    
class Vehicle(PPrintMixin,DynamicDocument):
    vehicle_id=fields.StringField(unique=True,required=True) 
    driver_id=fields.StringField()
    def __repr__(self):
		return "Vehicle (%r)" %(self.vehicle_id)
class Booking(PPrintMixin,DynamicDocument):
    booking_id=fields.StringField(required=True)
    passenger_detail=fields.StringField()
    passenger_mobile=fields.StringField()
    created_timestamp=fields.DateTimeField(default=datetime.datetime.utcnow)    
    pickup_timestamp=fields.DateTimeField(required=True)
    pickup_location=fields.StringField(required=True)
    drop_location=fields.StringField()
    num_passengers=fields.IntField()
    product_id = fields.StringField(required=True)
    cust_id=fields.StringField(required=True)
    booking_channel=fields.StringField(required=True)
    status=fields.StringField(default="new")
    
class Product(PPrintMixin,DynamicDocument):
    product_id=fields.StringField(unique=True,required=True)
    
class LocationUpdate(PPrintMixin,Document):
    driver_id=fields.StringField(required=True)
    timestamp=fields.DateTimeField(required=True)
    location=fields.StringField()
    checkin=fields.BooleanField()
    vehicle_id=fields.StringField()
    handoff=fields.StringField()
    
class Assignment(PPrintMixin,Document):
    cust_id=fields.StringField()
    created_timestamp=fields.DateTimeField(default=datetime.datetime.utcnow)    
    reporting_timestamp=fields.DateTimeField()
    reporting_location=fields.StringField()
    drop_location=fields.StringField()
    bookings=fields.SortedListField(fields.ReferenceField(Booking))
    status=fields.StringField(default="new")
    meta = {'queryset_class':CustomQuerySet}    
    def to_json(self):
        data=self.to_mongo()
        data['bookings']=[json.loads(booking.to_json()) for booking in self.bookings]
        return bson.json_util.dumps(data)
    

class DutySlip(PPrintMixin,Document):
    driver=fields.StringField(required=True)
    created_time=fields.DateTimeField(default=datetime.datetime.utcnow)
    vehicle=fields.StringField()
    dutyslip_id=fields.StringField()
    open_time=fields.DateTimeField()
    close_time=fields.DateTimeField()
    open_kms=fields.IntField()
    close_kms=fields.IntField()
    parking_charges=fields.FloatField()
    toll_charges=fields.FloatField()
    assignment=fields.ReferenceField(Assignment)
    amount=fields.IntField()
    status=fields.StringField(default="new")
    payment_mode=fields.StringField()
    
class Invoice(PPrintMixin,DynamicDocument):
	cust_id=fields.StringField()
	invoice_date=fields.DateTimeField()
	invoicelines=fields.ListField(fields.DictField())
