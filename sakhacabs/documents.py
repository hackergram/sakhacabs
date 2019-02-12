#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 21:52:07 2018

@author: arjun
"""

from mongoengine import Document, fields, DynamicDocument
import datetime
import bson
import json
from flask_mongoengine import QuerySet
from sakhacabs import utils


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
                attrs.append('\n    {} = {},'.format(
                    name, value.strftime("%Y-%m-%d %H:%M:%S")))
            else:
                attrs.append('\n    {} = {!r},'.format(name, value))
        return '<{}: {}\n>'.format(type(self).__name__, ''.join(attrs))


class CustomQuerySet(QuerySet):
    def to_json(self):
        return "[%s]" % (",".join([doc.to_json() for doc in self]))


class Driver(PPrintMixin, DynamicDocument):
    driver_id = fields.StringField(unique=True, required=True)
    mobile_num = fields.StringField(unique=True, required=True)
    tgid = fields.IntField()

    def __repr__(self):
        return "Driver (%r)" % (self.driver_id)


class Customer(PPrintMixin, DynamicDocument):
    cust_id = fields.StringField(unique=True, required=True)
    cust_type = fields.StringField()
    mobile_num = fields.StringField(required=True)
    tgid = fields.IntField()
    cust_billing = fields.StringField(default="N/A")


class Vehicle(PPrintMixin, DynamicDocument):
    vehicle_id = fields.StringField(unique=True, required=True)
    driver_id = fields.StringField()
    vehicle_cat = fields.StringField()
    vehicle_name = fields.StringField()

    def __repr__(self):
        return "Vehicle (%r)" % (self.vehicle_id)


class Booking(PPrintMixin, DynamicDocument):
    booking_id = fields.StringField(required=True)
    passenger_detail = fields.StringField()
    passenger_mobile = fields.StringField()
    created_timestamp = fields.DateTimeField(default=datetime.datetime.utcnow)
    pickup_timestamp = fields.DateTimeField(required=True)
    pickup_location = fields.StringField(required=True)
    drop_location = fields.StringField()
    num_passengers = fields.IntField()
    product_id = fields.StringField(required=True)
    cust_id = fields.StringField(required=True)
    booking_channel = fields.StringField(required=True)
    status = fields.StringField(default="new")
    remarks = fields.StringField()
    assignment = fields.StringField(default=None)
    cust_meta = fields.DictField(unique=True)
    notification_prefs = fields.DictField(default=utils.defaultnotificationprefs)

    def __repr__(self):
        if self.pickup_timestamp:
            ts = utils.get_local_ts(self.pickup_timestamp).strftime("%Y-%m-%d %H:%M")
        else:
            ts = "Not Set"
        return "\nBooking ID #{}\nPickup Time: {}\nPickup Location: {}\nCust ID: {}\nPassenger Details: {}\n".format(self.booking_id, ts, self.pickup_location, self.cust_id, self.passenger_detail)


class Product(PPrintMixin, DynamicDocument):
    product_id = fields.StringField(unique=True, required=True)
    product_desc = fields.StringField(required=True, default="No description provided")
    included_hrs = fields.FloatField(required=True, default=0.0)  # CHANGELOG - Will invalidate existing product data
    included_kms = fields.FloatField(required=True, default=0.0)  # CHANGELOG - Will invalidate existing product data
    extra_hrs_rate = fields.FloatField(required=True, default=0.0)  # CHANGELOG - Will invalidate existing product data
    extra_kms_rate = fields.FloatField(required=True, default=0.0)  # CHANGELOG - Will invalidate existing product data
    price = fields.FloatField(required=True, default=0.0)


class LocationUpdate(PPrintMixin, Document):
    driver_id = fields.StringField(required=True)
    timestamp = fields.DateTimeField(required=True)
    location = fields.StringField()
    checkin = fields.BooleanField(required=True, default=True)
    vehicle_id = fields.StringField()
    handoff = fields.StringField()

    def __repr__(self):
        retval = ""
        if self.checkin:
            retval = retval + "\nCheck In\n"
        else:
            retval = retval + "\nCheck Out\n"
        retval = retval + "Timestamp: " + \
            utils.get_local_ts(self.timestamp).strftime(
                "%Y-%m-%d %H:%M:%S") + "\n"
        if self.location:
            retval = retval + "Location: " + self.location + "\n"
        if self.vehicle_id:
            retval = retval + "Vehicle: " + str(self.vehicle_id) + "\n"
        if self.handoff:
            retval = retval + "Handoff: " + self.handoff + "\n"

        return retval


class Assignment(PPrintMixin, Document):
    cust_id = fields.StringField()
    created_timestamp = fields.DateTimeField(default=datetime.datetime.utcnow)
    reporting_timestamp = fields.DateTimeField()
    reporting_location = fields.StringField()
    drop_location = fields.StringField()
    bookings = fields.SortedListField(fields.ReferenceField(Booking))
    status = fields.StringField(default="new")
    meta = {'queryset_class': CustomQuerySet}

    def to_json(self):
        data = self.to_mongo()
        data['bookings'] = [json.loads(booking.to_json())
                            for booking in self.bookings]
        return bson.json_util.dumps(data)


class DutySlip(PPrintMixin, Document):
    driver = fields.StringField(required=True)
    created_time = fields.DateTimeField(default=datetime.datetime.utcnow)
    vehicle = fields.StringField(default=None)
    dutyslip_id = fields.StringField(default=None)
    open_time = fields.DateTimeField(default=None)
    close_time = fields.DateTimeField(default=None)
    open_kms = fields.IntField(default=0)
    close_kms = fields.IntField(default=0)
    parking_charges = fields.FloatField(default=0.0)
    toll_charges = fields.FloatField(default=0.0)
    assignment = fields.ReferenceField(Assignment)
    amount = fields.IntField(default=0)
    status = fields.StringField(default="new")
    payment_mode = fields.StringField(default=None)
    remarks = fields.StringField(default=None)
    notification_prefs = fields.DictField(default=utils.defaultnotificationprefs)

    def __repr__(self):
        if self.open_time:
            ot = utils.get_local_ts(self.open_time).strftime("%Y-%m-%d %H:%M")
        else:
            ot = "Not Set"
        if self.close_time:
            ct = utils.get_local_ts(self.close_time).strftime("%Y-%m-%d %H:%M")
        else:
            ct = "Not Set"
        if ot != "Not Set" and ct != "Not Set":
            td = round(
                float((self.close_time - self.open_time).total_seconds() / 3600), 1)
        else:
            td = 0.0
        return "DutySlip #{}\nOpen Time: {}\nClose Time: {}\nTotal Hours: {}\nOpen KMs: {}\nClose KMs: {}\nTotal KMs: {}\nParking Charges: {}\nToll Charges: {}\nAmount: {}\nRemarks: {}".format(self.dutyslip_id, ot, ct, td, self.open_kms, self.close_kms, self.close_kms - self.open_kms, self.parking_charges, self.toll_charges, self.amount, self.remarks)


class Invoice(PPrintMixin, DynamicDocument):
    invoice_id = fields.StringField(unique=True, required=True)
    cust_id = fields.StringField(required=True)
    invoice_date = fields.DateTimeField()
    invoicelines = fields.ListField(fields.DictField())
    taxes = fields.ListField(fields.DictField())
    status = fields.StringField(default="new")
    url = fields.StringField()
