# -*- coding: utf-8 -*-
from datetime import datetime

from couchdbkit.ext.django.schema import Document, StringProperty, DateTimeProperty, IntegerProperty,DictProperty,BooleanProperty


class Booking(Document):
    author = StringProperty()
    title = StringProperty()
    content = StringProperty()
    date = DateTimeProperty(default=datetime.utcnow)

class User(Document):
    role = StringProperty()
    telegram_id=IntegerProperty()
    meta = DictProperty()
class LocationUpdate(Document):
    driver_id=StringProperty()
    timestamp=DateTimeProperty()
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