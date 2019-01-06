#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 17:02:47 2018

@author: lilhack110
"""
import datetime 
from jsonobject import*
class Booking(JsonObject):
    serialno=FloatProperty()
    bookingrcvddate=DateProperty()
    bookingdate=DateProperty()
    bookingchannel=StringProperty()
    custid=StringProperty
    passengerdetail=StringProperty()
    flightnum=FloatProperty()
    pickupaddress=StringProperty()
    dropaddress=StringProperty()
    reportingtime=DateTimeProperty()
    gadv_bookingid=IntegerProperty()
    gadv_tripcode=StringProperty()
    productcode=StringProperty()
    payment=StringProperty()
    price=FloatProperty()
    cancelled=BooleanProperty(default=False)
    airportrepduty=StringProperty()
    driveronduty=ListProperty()
    vehiclenotused=ListProperty()
    vehicledetails=StringProperty()
    driver=ListProperty()

