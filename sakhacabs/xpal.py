# -*- coding: utf-8 -*-
#

"""
Created on Sat Sep  8 21:52:07 2018

@author: arjun
"""

import sys
import datetime
import json
import mongoengine
sys.path.append("/opt/xetrapal")
import xetrapal
import pandas
from sakhacabs import documents, utils
from copy import deepcopy

sakhacabsxpal = xetrapal.Xetrapal(
    configfile="/opt/sakhacabs-appdata/sakhacabsxpal.conf")
sakhacabsgd = sakhacabsxpal.get_googledriver()
sms = sakhacabsxpal.get_sms_astra()

# Setting up mongoengine connections
sakhacabsxpal.logger.info("Setting up MongoEngine")
mongoengine.connect('sakhacabs', alias='default')


# Remote sync functionality

def validate_vehicle_dict(vehicledict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid vehicle"
    required_keys = []
    if new is True:
        required_keys = ["vehicle_id"]
    string_keys = ["vehicle_id"]
    validation = utils.validate_dict(
        vehicledict, required_keys=required_keys, string_keys=string_keys)
    if validation['status'] is True:
        sakhacabsxpal.logger.info("vehicledict: " + validation['message'])
    else:
        sakhacabsxpal.logger.error("vehicledict: " + validation['message'])
    return validation


def validate_invoice_dict(invoicedict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid vehicle"
    required_keys = []
    if new is True:
        required_keys = ["invoicelines", "cust_id", "invoice_date"]
    validation = utils.validate_dict(invoicedict, required_keys=required_keys)
    if validation['status'] is True:
        sakhacabsxpal.logger.info("invoicedict: " + validation['message'])
    else:
        sakhacabsxpal.logger.error("invoicedict: " + validation['message'])
    return validation


def validate_locupdate_dict(locupdatedict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid location update"
    required_keys = []
    if new is True:
        required_keys = ["driver_id", "timestamp"]
    string_keys = ["driver_id"]
    validation = utils.validate_dict(
        locupdatedict, required_keys=required_keys, string_keys=string_keys)
    if validation['status'] is True:
        sakhacabsxpal.logger.info("locupdatedict: " + validation['message'])
    else:
        sakhacabsxpal.logger.error("locupdatedict: " + validation['message'])
    return validation


def validate_customer_dict(customerdict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid customer"
    required_keys = []
    if new is True:
        required_keys = ["cust_id", "mobile_num"]
    string_keys = ["cust_id"]
    mobile_nums = ["mobile_num"]
    validation = utils.validate_dict(
        customerdict, required_keys=required_keys, string_keys=string_keys, mobile_nums=mobile_nums)
    if validation['status'] is True:
        sakhacabsxpal.logger.info("customerdict: " + validation['message'])
    else:
        sakhacabsxpal.logger.error("customerdict: " + validation['message'])
    return validation


def validate_product_dict(productdict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid product"
    required_keys = []
    if new is True:
        required_keys = ["product_id"]
    string_keys = ["product_id"]
    numbers = ["included_hrs", "included_kms", "extra_hrs_rate", "extra_kms_rate"]  # CHANGELOG #11 - AV - For #261
    validation = utils.validate_dict(productdict, required_keys=required_keys, string_keys=string_keys, numbers=numbers)
    if validation['status'] is True:
        sakhacabsxpal.logger.info("productdict: " + validation['message'])
    else:
        sakhacabsxpal.logger.error("productdict: " + validation['message'])
    return validation


def validate_driver_dict(driverdict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid driver"
    required_keys = []
    if new is True:
        required_keys = ["driver_id", "mobile_num"]
    string_keys = ["first_name", "last_name",
                   "mobile_num", "name", "driver_id"]
    mobile_nums = ["mobile_num"]
    validation = utils.validate_dict(
        driverdict, required_keys=required_keys, string_keys=string_keys, mobile_nums=mobile_nums)
    if validation['status'] is True:
        sakhacabsxpal.logger.info("driverdict: " + validation['message'])
    else:
        sakhacabsxpal.logger.error("driverdict: " + validation['message'])
    return validation


def validate_dutyslip_dict(dutyslipdict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid dutyslip"
    required_keys = []
    if new is True:
        required_keys = ["driver", "assignment"]
    string_keys = ["driver", "vehicle", "remarks"]
    dates = ['open_time', 'close_time']
    numbers = ['open_kms', 'close_kms', 'parking_charges', 'toll_charges', 'amount']
    validation = utils.validate_dict(
        dutyslipdict, required_keys=required_keys, string_keys=string_keys, dates=dates, numbers=numbers)

    try:
        if datetime.datetime.strptime(dutyslipdict['open_time'], "%Y-%m-%d %H:%M:%S") > datetime.datetime.strptime(dutyslipdict['close_time'], "%Y-%m-%d %H:%M:%S"):
            validation['status'] = False
            validation['message'] = "Open time cant be after close time"
    except Exception as e:
        validation['status'] = False
        validation['message'] = "ERROR IN TIME VALIDATION " + str(e)

    try:
        if float(dutyslipdict['open_kms']) > float(dutyslipdict['close_kms']):
            validation['status'] = False
            validation['message'] = "Open kms cant be more than close kms"
    except Exception as e:
        validation['status'] = False
        validation['message'] = "ERROR IN DIST VALIDATION " + str(e)
    try:
        if "vehicle" in dutyslipdict.keys() and dutyslipdict['vehicle'] != "":
            if len(documents.Vehicle.objects(vehicle_id=dutyslipdict['vehicle'])) == 0:
                validation['status'] = False
                validation['message'] = "Unknown vehicle id"
    except Exception as e:
        validation['status'] = False
        validation['message'] = "ERROR IN VEHICLE VALIDATION " + str(e)
    if validation['status'] is True:
        sakhacabsxpal.logger.info("dutyslipdict: " + validation['message'])
    else:
        sakhacabsxpal.logger.error("dutyslipdict: " + validation['message'])
    return validation


def validate_assignment_dict(assignmentdict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid assignment"

    if assignmentdict['dutyslips'] == []:
        validation['status'] = False
        validation['message'] = "At least one driver must be assigned to create an assignment."
    if assignmentdict['assignment']['bookings'] == []:
        validation['status'] = False
        validation['message'] = "At least one booking must be assigned to create an assignment."
    bookings = [documents.Booking.objects.with_id(
        x['_id']['$oid']) for x in assignmentdict['assignment']['bookings']]
    for booking in bookings:
        if booking.assignment is not None:
            validation['status'] = False
            validation['message'] = "Booking is already assigned {}! Please delete the old assignment before creating a new one.".format(
                booking.assignment)
        if booking.cust_id != assignmentdict['assignment']['cust_id']:
            validation['status'] = False
            validation['message'] = "Bookings from different customers cannot be assigned together."
    seenvehicles = []
    for dutyslip in assignmentdict['dutyslips']:
        if "vehicle" in dutyslip.keys():
            if dutyslip['vehicle'] in seenvehicles:
                validation['status'] = False
                validation['message'] = "Can't assign the same vehicle to more than one driver in the same assignment."
            seenvehicles.append(dutyslip['vehicle'])
    if validation['status'] is True:
        sakhacabsxpal.logger.info("assignmentdict: " + validation['message'])
    else:
        sakhacabsxpal.logger.error("assignmentdict: " + validation['message'])
    return validation





def new_locationupdate(driver, timestamp, checkin=True, location=None, vehicle=None, handoff=None, logger=xetrapal.astra.baselogger, **kwargs):
    """
    Creates a new location update, location updates once created are not deleted as they are equivalent to log entries.
    Returns a LocationUpdate object
    """
    vehicle_id = None
    if checkin is True:
        driver.checkedin = True
    if vehicle is not None:
        vehicle.driver_id = driver.driver_id
        vehicle.save()
        vehicle_id = vehicle.vehicle_id
    if checkin is False:
        driver.checkedin = False
        if len(documents.Vehicle.objects(driver_id=driver.driver_id)) > 0:
            v = documents.Vehicle.objects(driver_id=driver.driver_id)
            for vh in v:
                del vh.driver_id
                vh.save()
                vehicle_id = vh.vehicle_id
    driver.save()
    # UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    # timestamp + UTC_OFFSET_TIMEDELTA
    adjtimestamp = utils.get_utc_ts(timestamp)
    # Get new location update and save it
    locationupdate = documents.LocationUpdate(
        driver_id=driver.driver_id, timestamp=adjtimestamp, location=location, checkin=checkin, handoff=handoff, vehicle_id=vehicle_id)
    # Tell the user what happened
    if checkin is True:
        logger.info(u"New checkin from driver with id {} at {} from {}".format(
            locationupdate.driver_id, locationupdate.timestamp, locationupdate.location))
    else:
        logger.info(u"Checkout from driver with id {} at {} from {}".format(
            locationupdate.driver_id, locationupdate.timestamp, locationupdate.location))
    locationupdate.save()
    return locationupdate


'''
Bookings CRUD
'''


def validate_booking_dict(bookingdict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid booking"
    required_keys = []
    if new is True:
        required_keys = ["cust_id", "product_id", "passenger_detail",
                         "pickup_timestamp", "pickup_location", "booking_channel"]
    string_keys = ["cust_id", "product_id",
                   "passenger_detail", "passenger_mobile", "remarks"]
    mobile_nums = ["passenger_mobile"]
    validation = utils.validate_dict(
        bookingdict, required_keys=required_keys, string_keys=string_keys, mobile_nums=mobile_nums)
    if "cust_id" in bookingdict.keys():
        if bookingdict['cust_id'] == "retail":
            if not bookingdict['passenger_mobile'] or bookingdict['passenger_mobile'] is None:
                validation['message'] = "Passenger Mobile Must be provided for retail bookings"
                validation['status'] = False
    if validation['status'] is True:
        sakhacabsxpal.logger.info("bookingdict: " + validation['message'])
    else:
        sakhacabsxpal.logger.error("bookingdict: " + validation['message'])
    return validation


def new_booking(respdict):
    bookingdict = {}
    sakhacabsxpal.logger.info(
        "Creating new booking from dictionary\n{}".format(respdict))
    for key in respdict.keys():
        if key in ["cust_id", "product_id", "passenger_detail", "passenger_mobile", "pickup_timestamp", "pickup_location", "drop_location", "booking_channel", "num_passengers", "notification_prefs", "remarks"]:  # CHANGELOG #11 - AV - Remarks given at booking time should now be reflected in the booking
            bookingdict[key] = respdict[key]
            respdict.pop(key)
    if "_id" in respdict.keys():
        respdict.pop("_id")
    if "created_timestamp" in respdict.keys():
        respdict.pop("created_timestamp")
    if "passenger_mobile" not in bookingdict.keys() or bookingdict['passenger_mobile'] is None:
        mobile_num = documents.Customer.objects(
            cust_id=bookingdict['cust_id'])[0].mobile_num
        bookingdict['passenger_mobile'] = mobile_num
    try:
        b = documents.Booking(booking_id=utils.new_booking_id(), **bookingdict)
        for key in respdict.keys():
            key2 = key.replace(".", "").replace("$", "")
            if key2 != key:
                respdict[key2] = respdict[key]
                respdict.pop(key)
        sakhacabsxpal.logger.info("Saving cust-meta as: {}".format(respdict))
        b.cust_meta = respdict
        b.save()
        b.reload()
        notification = "Sakha Cabs Booking {} created \n {}".format(b.booking_id, repr(b))

        if b.notification_prefs["new"] != []:
            recipients = []
            for num in b.notification_prefs["new"]:
                recipients.append({"type": "mobile", "value": num})
            sms.send_sms({"message": notification, "recipients": recipients})
        sakhacabsxpal.logger.info("{}".format(notification))
        respdict['booking_id'] = b.booking_id
        return [b]
    except Exception as e:
        respdict['booking_id'] = None
        return "error: {} {}".format(type(e), str(e))


def update_booking_status(booking_id, status):
    if status not in utils.validstatuses:
        sakhacabsxpal.logger.error("Invalid status")
        return False
    booking = documents.Booking.objects(booking_id=booking_id)
    if len(booking) == 0:
        return "No booking by that id"
    else:
        booking = booking[0]
    try:
        if status in ['cancelled', 'new']:
            if booking.assignment is not None:
                sakhacabsxpal.logger.info(
                    "Booking is assigned, checking assignment status")
                assignment = documents.Assignment.objects.with_id(booking.assignment)
                sakhacabsxpal.logger.info("Removing booking {} from assignment {}".format(
                    booking.booking_id, booking.assignment))
                assignment.bookings.remove(booking)
                assignment.save()
                assignment.reload()
                if assignment.bookings == []:
                    update_assignment_status(assignment.id, "cancelled")
                else:
                    sakhacabsxpal.logger.info("Updating assignment reporting time to first booking!")
                    assignment.reporting_location = assignment.bookings[0].pickup_location
                    assignment.reporting_timestamp = assignment.bookings[0].pickup_timestamp
                    assignment.save()
                booking.assignment = None
        booking.status = status
        booking.save()
        if booking.notification_prefs[status] != []:
            recipients = []
            notification = "Sakha Cabs Booking {} status change to {}".format(booking.booking_id, booking.status)
            for num in booking.notification_prefs[status]:
                recipients.append({"type": "mobile", "value": num})
            if status == "assigned":
                assignment = documents.Assignment.objects.with_id(booking.assignment)
                notification = notification + "\n Pickup Time: " + assignment.reporting_timestamp.strftime("%Y-%m-%d %H:%M") + "\n Pickup Location: " + assignment.reporting_location + "\n Drivers Assigned \n"
                dutyslips = documents.DutySlip.objects(assignment=assignment)
                for dutyslip in dutyslips:
                    driver = documents.Driver.objects(driver_id=dutyslip.driver)[0]
                    notification = notification + "\n {} {} {}".format(driver.driver_id, driver.mobile_num, dutyslip.vehicle)
            sms.send_sms({"message": notification, "recipients": recipients})
        return True
    except Exception as e:
        sakhacabsxpal.logger.error("Error occurred updating booking status {}".format(str(e)))
        return False


def update_booking(booking_id, respdict):
    booking = documents.Booking.objects(booking_id=booking_id)
    if len(booking) == 0:
        return "No booking by that id"
    else:
        booking = booking[0]
        sakhacabsxpal.logger.info(
            "Trying to update booking with id {}".format(booking.booking_id))
        if "_id" in respdict.keys():
            respdict.pop("_id")
        if "created_timestamp" in respdict.keys():
            respdict.pop("created_timestamp")
        if "status" in respdict.keys():
            sakhacabsxpal.logger.info("Updated status should be {}".format(respdict['status']))
            if respdict['status'] != booking.status:
                sakhacabsxpal.logger.info("original status is {}".format(booking.status))
                if not update_booking_status(booking.booking_id, respdict['status']):
                    sakhacabsxpal.loggger.error("Updating booking status failed")
                    return "Updating booking status failed"
        try:
            booking.update(**respdict)
            booking.save()
            booking.reload()
            if booking.assignment is not None:
                assignment = documents.Assignment.objects.with_id(
                    booking.assignment)
                if "pickup_timestamp" in respdict.keys():
                    assignment.reporting_timestamp = booking.pickup_timestamp
                if "pickup_location" in respdict.keys():
                    assignment.reporting_location = booking.pickup_location
                assignment.save()

            return [booking]
        except Exception as e:
            return "{} {}".format(type(e), str(e))


def delete_booking(booking_id):
    if len(documents.Booking.objects(booking_id=booking_id)) > 0:
        try:
            update_booking_status(booking_id, "cancelled")
            booking = documents.Booking.objects(booking_id=booking_id)[0]
            booking.delete()
            return []
        except Exception as e:
            return "{} {}".format(type(e), str(e))
    else:
        return "No booking by that id"


'''
Assignment CRUD
'''

def save_assignment(assignmentdict, assignment_id=None):
    '''Creates a new assignment/Updates an existing assignment with the provided bookings and duty slips
    Input: A dictionary of the format {"assignment": Assignment object,dutyslips: List of driver/vehicle pairs}
    Returns: An assignment object
    '''
    bookings = [documents.Booking.objects.with_id(
        x['_id']['$oid']) for x in assignmentdict['assignment']['bookings']]
    if assignment_id is None:
        assignment = documents.Assignment(bookings=bookings)
        assignment.status = "new"
        sakhacabsxpal.logger.info("Created new assignment at {}".format(
            assignment.created_timestamp.strftime("%Y-%m-%d %H:%M:%S")))
    else:
        sakhacabsxpal.logger.info(
            "Saving existing assignment {}".format(assignment_id))
        assignment = documents.Assignment.objects.with_id(assignment_id)
        assignment.bookings = bookings
    assignment.bookings = sorted(
        assignment.bookings, key=lambda k: k.pickup_timestamp)
    assignment.reporting_timestamp = assignment.bookings[0].pickup_timestamp
    assignment.reporting_location = assignment.bookings[0].pickup_location
    if assignment.bookings[0].drop_location:
        assignment.drop_location = assignment.bookings[0].drop_location
    assignment.cust_id = assignment.bookings[0].cust_id
    assignment.save()
    existingdutyslips = documents.DutySlip.objects(assignment=assignment)
    sakhacabsxpal.logger.info(
        "Existing duty slips {}".format(existingdutyslips.to_json()))
    existingdutyslips = list(existingdutyslips)
    sakhacabsxpal.logger.info(
        "Submitted duty slips {}".format(assignmentdict['dutyslips']))
    sakhacabsxpal.logger.info("Ignoring unchanged dutyslips")
    for dutyslip in existingdutyslips:
        sakhacabsxpal.logger.info("{}".format(dutyslip.to_json()))
        match = False
        for dutyslipdict in assignmentdict['dutyslips']:
            # sakhacabsxpal.logger.info("{}".format(dutyslipdict))
            if dutyslip.driver == dutyslipdict['driver'] and dutyslip.vehicle == dutyslipdict['vehicle']:
                sakhacabsxpal.logger.info("Unchanged {}".format(dutyslipdict))
                # assignmentdict['dutyslips'].remove(dutyslipdict)
                # existingdutyslips.remove(dutyslip)
                match = True
        if match is False:
            sakhacabsxpal.logger.info(
                "Removing unmatched dutyslip {}".format(dutyslip.to_json()))
            dutyslip.delete()
    sakhacabsxpal.logger.info("Adding the new dutyslips")
    for dutyslipdict in assignmentdict['dutyslips']:
        if "vehicle" not in dutyslipdict.keys():
            dutyslipdict['vehicle'] = None
        d = documents.DutySlip.objects(
            driver=dutyslipdict['driver'], vehicle=dutyslipdict['vehicle'], assignment=assignment)
        if len(d) == 0:
            d = documents.DutySlip(
                driver=dutyslipdict['driver'], vehicle=dutyslipdict['vehicle'], assignment=assignment, status="new")
            sakhacabsxpal.logger.info(
                "Created duty slip {}".format(d.to_json()))
        else:
            d = d[0]
            sakhacabsxpal.logger.info(
                "Duty slip exists {}".format(d.to_json()))
        d.save()
    for booking in assignment.bookings:
        booking.assignment = str(assignment.id)
        booking.save()
        update_booking_status(booking.booking_id, "assigned")
        booking.save()
    sakhacabsxpal.logger.info(
        "Saved assignment {}".format(assignment.to_json()))
    return [assignment]


def search_assignments(cust_id=None, date_frm=None, date_to=None, status=None):
    assignments = documents.Assignment.objects
    if cust_id is not None:
        assignments = assignments.filter(cust_id=cust_id)
    if date_frm is not None:
        assignments = assignments.filter(reporting_timestamp__gt=date_frm)
    if date_to is not None:
        assignments = assignments.filter(reporting_timestamp__lt=date_to)
    if status is not None:
        assignments = assignments.filter(status=status)

    return assignments


def update_assignment_status(assignmentid, status):
    if status not in utils.validstatuses or status in ["new", "assigned"]:
        sakhacabsxpal.logger.error("Invalid status")
        return False
    assignment = documents.Assignment.objects.with_id(assignmentid)
    if assignment:
        dutyslips = documents.DutySlip.objects(assignment=assignment)
        try:
            if status == "cancelled":
                sakhacabsxpal.logger.info("Removing Assignment reference from  Bookings {}".format(assignment.bookings))
                for booking in assignment.bookings:
                    update_booking_status(booking.booking_id, "new")
                for ds in dutyslips:
                    if ds.status != "cancelled":
                        update_dutyslip_status(ds.id, "cancelled")
            if status in ["open", "closed"]:
                for booking in assignment.bookings:
                    update_booking_status(booking.booking_id, status)

            if status == "verified":
                for booking in assignment.bookings:
                    update_booking_status(booking.booking_id, status)
                for ds in dutyslips:
                    if ds.status != "cancelled":
                        update_dutyslip_status(ds.id, status)
            assignment.status = status
            assignment.save()
            sakhacabsxpal.logger.info("Successfully updated assignment status")
            return True
        except Exception as e:
                sakhacabsxpal.logger.error({}.format(str(e)))
                return False

    else:
        sakhacabsxpal.logger.error("Assignment with that ID does not exist")
        return False


def delete_assignment(assignmentid):
    if len(documents.Assignment.objects.with_id(assignmentid)) > 0:
        update_assignment_status(assignmentid, "cancelled")
        assignment = documents.Assignment.objects.with_id(assignmentid)
        documents.DutySlip.objects(assignment=assignment).delete()
        assignment.delete()
        return []
    else:
        return "Assignment with that ID does not exist"


'''
Duty Slip CRUD
'''


def get_duties_for_driver(driver_id):
    d = documents.DutySlip.objects(driver=driver_id, status__ne="verified")
    if len(d) > 0:
        return d


def update_dutyslip_status(dsid, status):
    dutyslip = documents.DutySlip.objects.with_id(dsid)
    if dutyslip is None:
        sakhacabsxpal.logger.error("No dutyslip with that id found")
        return False
    if status not in utils.validstatuses or status in ['assigned']:
        sakhacabsxpal.logger.error("Invalid status")
        return False
    try:

        dutyslip.status = status
        dutyslip.save()
        if status == "open":
            update_assignment_status(dutyslip.assignment.id, "open")
        if status == "cancelled":
            otherds = documents.DutySlip.objects(assignment=dutyslip.assignment, status__ne="cancelled")
            if len(otherds) == 0:
                update_assignment_status(dutyslip.assignment.id, "cancelled")
        return True
    except Exception as e:
        sakhacabsxpal.logger.error("{}".format(str(e)))
        return False


def update_dutyslip(dsid, respdict):
    dutyslip = documents.DutySlip.objects.with_id(dsid)
    if dutyslip is None:
        return "No dutyslip with that id found"
    try:
        if "status" in respdict.keys():
            if respdict['status'] != dutyslip.status:
                update_dutyslip_status(dutyslip.id, respdict['status'])
        dutyslip.update(**respdict)
        dutyslip.save()
        dutyslip.reload()
        return [dutyslip]
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def delete_dutyslip(dsid):
    if len(documents.DutySlip.objects.with_id(dsid)) > 0:
        update_dutyslip_status(dsid, "cancelled")
        ds = documents.DutySlip.objects.with_id(dsid)
        ds.delete()
    else:
        return "No Dutyslip by that ID"


'''
Driver CRUD functionality
'''


def get_driver_by_mobile(mobile_num):
    t = documents.Driver.objects(mobile_num=mobile_num)
    xetrapal.astra.baselogger.info(
        "Found {} drivers with Mobile Num {}".format(len(t), mobile_num))
    if len(t) > 0:
        # return[User(x['value']) for x in t][0]
        return t[0]
    else:
        return None


def get_driver_by_tgid(tgid):
    t = documents.Driver.objects(tgid=tgid)
    xetrapal.astra.baselogger.info(
        "Found {} drivers with Telegram ID {}".format(len(t), tgid))
    if len(t) > 0:
        # return[User(x['value']) for x in t][0]
        return t[0]
    else:
        return None


def create_driver(respdict):
    driver = documents.Driver.objects(driver_id=respdict['driver_id'])
    if len(driver) > 0:
        return "Driver with that ID Exists"
    if len(respdict['driver_id']) < 5:
        return "id should be minmum of 5 charecters"
    if "_id" in respdict.keys():
        respdict.pop('_id')
    try:
        driver = documents.Driver(**respdict)
        driver.save()
        return [driver]
    except Exception as e:
        return "{} {}".format(repr(e), str(e))


def update_driver(driver_id, respdict):
    driver = documents.Driver.objects(driver_id=driver_id)
    if len(driver) == 0:
        return "No driver by ID {}".format(driver_id)
    else:
        driver = driver[0]
    if "_id" in respdict.keys():
        respdict.pop('_id')
    if "driver_id" in respdict.keys():
        if respdict['driver_id'] != driver_id:
            return "Driver ID mismatch {} {}".format(driver_id, respdict['driver_id'])
        respdict.pop('driver_id')
    try:
        driver.update(**respdict)
        driver.save()
        driver.reload()
        return [driver]
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def delete_driver(driver_id):
    if len(documents.Driver.objects(driver_id=driver_id)) > 0:
        try:
            driver = documents.Driver.objects(driver_id=driver_id)[0]
            driver.delete()
            return []
        except Exception as e:
            return "{} {}".format(type(e), str(e))
    else:
        return "No driver by that id"


'''
Vehicle CRUD functionality
'''


def get_vehicle_by_vid(vid):
    t = documents.Vehicle.objects(vehicle_id=vid)
    if len(t) > 0:
        return t[0]
    else:
        return None


def create_vehicle(respdict):
    vehicle = documents.Vehicle.objects(vehicle_id=respdict['vehicle_id'])
    if len(vehicle) > 0:
        return "Vehicle with that ID Exists"
    if len(respdict['vehicle_id'])<5:
        return "id should be minmum of 5 charecters"
    if "_id" in respdict.keys():
        respdict.pop('_id')
    try:
        vehicle = documents.Vehicle(**respdict)
        vehicle.save()
        return [vehicle]
    except Exception as e:
        return "{} {}".format(repr(e), str(e))


def update_vehicle(vehicle_id, respdict):
    vehicle = documents.Vehicle.objects(vehicle_id=vehicle_id)
    if len(vehicle) == 0:
        return "No Vehicle by ID {}".format(vehicle_id)
    else:
        vehicle = vehicle[0]
    if "_id" in respdict.keys():
        respdict.pop('_id')
    if "vehicle_id" in respdict.keys():
        if respdict['vehicle_id'] != vehicle_id:
            return "vehicle ID mismatch {} {}".format(vehicle_id, respdict['vehicle_id'])
        respdict.pop('vehicle_id')
    try:
        vehicle.update(**respdict)
        vehicle.save()
        vehicle.reload()
        return [vehicle]
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def delete_vehicle(vehicle_id):
    if len(documents.Vehicle.objects(vehicle_id=vehicle_id)) > 0:
        try:
            vehicle = documents.Vehicle.objects(vehicle_id=vehicle_id)[0]
            vehicle.delete()
            return []
        except Exception as e:
            return "{} {}".format(type(e), str(e))
    else:
        return "No vehicle by that id"


'''
Customer
'''


def create_customer(respdict):
    customer = documents.Customer.objects(cust_id=respdict['cust_id'])
    if len(customer) > 0:
        return "Customer with that ID Exists"
    if len(respdict['cust_id']) < 5:
        return "id should be minmum of 5 charecters"
    if "_id" in respdict.keys():
        respdict.pop('_id')
    try:
        customer = documents.Customer(**respdict)
        customer.save()
        return [customer]
    except Exception as e:
        return "{} {}".format(repr(e), str(e))


def update_customer(cust_id, respdict):
    customer = documents.Customer.objects(cust_id=cust_id)
    if len(customer) == 0:
        return "No Customer by ID {}".format(cust_id)
    else:
        customer = customer[0]
    if "_id" in respdict.keys():
        respdict.pop('_id')
    if "cust_id" in respdict.keys():
        if respdict['cust_id'] != cust_id:
            return "customer ID mismatch {} {}".format(cust_id, respdict['cust_id'])
        respdict.pop('cust_id')
    try:
        customer.update(**respdict)
        customer.save()
        customer.reload()
        return [customer]
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def delete_customer(cust_id):
    if len(documents.Customer.objects(cust_id=cust_id)) > 0:
        try:
            customer = documents.Customer.objects(cust_id=cust_id)[0]
            customer.delete()
            return []
        except Exception as e:
            return "{} {}".format(type(e), str(e))
    else:
        return "No customer by that id"


'''
Product
'''


def create_product(respdict):
    product = documents.Product.objects(product_id=respdict['product_id'])
    if len(product) > 0:
        return "Product with that ID Exists"
    if "_id" in respdict.keys():
        respdict.pop('_id')
    if len(respdict['product_id'])<5:
        return "id should be minmum of 5 charecters"
    try:
        product = documents.Product(**respdict)
        product.save()
        return [product]
    except Exception as e:
        return "{} {}".format(repr(e), str(e))


def update_product(product_id, respdict):
    product = documents.Product.objects(product_id=product_id)
    if len(product) == 0:
        return "No Product by ID {}".format(product_id)
    else:
        product = product[0]
    if "_id" in respdict.keys():
        respdict.pop('_id')
    if "product_id" in respdict.keys():
        if respdict['product_id'] != product_id:
            return "product ID mismatch {} {}".format(product_id, respdict['product_id'])
        respdict.pop('product_id')
    try:
        product.update(**respdict)
        product.save()
        product.reload()
        return [product]
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def delete_product(product_id):
    if len(documents.Product.objects(product_id=product_id)) > 0:
        try:
            product = documents.Product.objects(product_id=product_id)[0]
            product.delete()
            return []
        except Exception as e:
            return "{} {}".format(type(e), str(e))
    else:
        return "No product by that id"


'''
Invoices
'''


def generate_invoice(to_settle):
    sakhacabsxpal.logger.info(
        "Generating invoice for assignments {}".format(to_settle))
    invoice_lines = []

    try:
        for ass in to_settle:
            covered_hrs = 0
            covered_kms = 0

            for booking in ass.bookings:
                invoiceline = {}
                invoiceline['date'] = utils.get_local_ts(
                    booking.pickup_timestamp).strftime("%Y-%m-%d")
                invoiceline['particulars'] = booking.booking_id + \
                    " " + booking.passenger_detail
                invoiceline['product'] = booking.product_id
                invoiceline['qty'] = 1
                invoiceline['rate'] = documents.Product.objects(
                    product_id=booking.product_id)[0].price
                invoiceline['amount'] = invoiceline['qty'] * \
                    invoiceline['rate']
                invoice_lines.append(invoiceline)
                covered_hrs += documents.Product.objects(
                    product_id=booking.product_id)[0].included_hrs  # CHANGELOG #11 - AV - Should fix the invoicing calculation based on product details
                covered_kms += documents.Product.objects(
                    product_id=booking.product_id)[0].included_kms  # CHANGELOG #11 - AV - Should fix the invoicing calculation based on product details
            consumed_hrs = 0
            consumed_kms = 0
            for ds in documents.DutySlip.objects(assignment=ass):
                print repr(ds)
                kms = ds.close_kms - ds.open_kms
                consumed_kms += kms
                hrs = ds.close_time - ds.open_time
                consumed_hrs += int(hrs.total_seconds() / 3600)
                if ds.parking_charges is not None:
                    invoiceline = {}
                    invoiceline['date'] = utils.get_local_ts(
                        ass.reporting_timestamp).strftime("%Y-%m-%d")
                    invoiceline['particulars'] = "Parking Charges"
                    invoiceline['product'] = "PARKINGCHRGS"
                    invoiceline['rate'] = int(ds.parking_charges)
                    invoiceline['qty'] = 1
                    invoiceline['amount'] = invoiceline['qty'] * \
                        invoiceline['rate']
                    if invoiceline['amount'] != 0:
                        invoice_lines.append(invoiceline)
                if ds.toll_charges is not None:
                    invoiceline = {}
                    invoiceline['date'] = utils.get_local_ts(
                        ass.reporting_timestamp).strftime("%Y-%m-%d")
                    invoiceline['particulars'] = "Toll Charges"
                    invoiceline['product'] = "TOLLCHRGS"
                    invoiceline['rate'] = int(ds.toll_charges)
                    invoiceline['qty'] = 1
                    invoiceline['amount'] = invoiceline['qty'] * \
                        invoiceline['rate']
                    if invoiceline['amount'] != 0:
                        invoice_lines.append(invoiceline)
            sakhacabsxpal.logger.info("Consumed KMs {} Consumed Hrs {} Included Hrs {} Included Kms {}".format(consumed_kms, consumed_hrs, covered_kms, covered_hrs))
            if consumed_kms > covered_kms:
                extrakms = consumed_kms - covered_kms
                invoiceline = {}
                invoiceline['date'] = utils.get_local_ts(
                    ass.reporting_timestamp).strftime("%Y-%m-%d")
                invoiceline['particulars'] = "Extra Kms " + str(ds.dutyslip_id)
                invoiceline['product'] = "EXTRAKMS"
                invoiceline['rate'] = max([documents.Product.objects(product_id=booking.product_id)[0].extra_kms_rate for booking in ass.bookings])  # CHANGELOG #11 - AV - Should fix the invoicing calculation based on product details
                sakhacabsxpal.logger.info("Setting rate for extra kms as {}".format(invoiceline['rate']))
                invoiceline['qty'] = extrakms
                invoiceline['amount'] = invoiceline['qty'] * \
                    invoiceline['rate']
                if invoiceline['amount'] != 0:
                    invoice_lines.append(invoiceline)
            if consumed_hrs > covered_hrs:
                extrahrs = consumed_hrs - covered_hrs
                invoiceline = {}
                invoiceline['date'] = utils.get_local_ts(
                    ass.reporting_timestamp).strftime("%Y-%m-%d")
                invoiceline['particulars'] = "Extra Hours " + \
                    str(ds.dutyslip_id)
                invoiceline['product'] = "EXTRAHRS"
                invoiceline['rate'] = max([documents.Product.objects(product_id=booking.product_id)[0].extra_hrs_rate for booking in ass.bookings])  # CHANGELOG #11 - AV - Should fix the invoicing calculation based on product details
                invoiceline['qty'] = extrahrs
                invoiceline['amount'] = invoiceline['qty'] * \
                    invoiceline['rate']
                if invoiceline['amount'] != 0:
                    invoice_lines.append(invoiceline)
    except Exception as e:
        sakhacabsxpal.logger.error("{} {}".format(type(e), str(e)))
    invoice = {}
    invoice['invoicelines'] = invoice_lines
    if len(to_settle) > 0:
        invoice['cust_id'] = to_settle[0].cust_id
    invoice['taxes'] = []
    return invoice


def get_invoice_total(invoice_id):
    if len(documents.Invoice.objects(invoice_id=invoice_id)) > 0:
        try:
            invoice = documents.Invoice.objects(invoice_id=invoice_id)[0]
            resp = {}
            resp['total'] = 0.0
            resp['grand_total'] = 0.0
            resp['tax'] = 0.0
            for line in invoice.invoicelines:
                resp['total'] += line['amount']
            resp['grand_total'] = resp['total']
            for tax in invoice.taxes:
                resp['tax'] += tax['rate'] * resp['total']
            resp['grand_total'] += resp['tax']
            return resp
        except Exception as e:
            return "{}''' {}".format(type(e), str(e))
    else:
        return "No such invoice"


def create_invoice(invoicedict):
    try:
        invoice = documents.Invoice(
            invoice_id=utils.new_invoice_id(), **invoicedict)
        invoice.save()
        invoice.total = get_invoice_total(invoice.invoice_id)
        return[invoice]
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def update_invoice(invoice_id, invoicedict):
    try:
        if "_id" in invoicedict:
            invoicedict.pop("_id")
        invoice = documents.Invoice.objects(invoice_id=invoice_id)[0]
        invoice.update(**invoicedict)
        invoice.save()
        invoice.total = get_invoice_total(invoice.invoice_id)
        return[invoice]
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def delete_invoice(invoice_id):
    if len(documents.Invoice.objects(invoice_id=invoice_id)) == 0:
        return "No Invoice by that ID"
    else:
        try:
            invoice = documents.Invoice.objects(invoice_id=invoice_id)
            invoice.delete()
            return []
        except Exception as e:
            return "{} {}".format(type(e), str(e))


def export_invoice(invoice_id):
    invoice = documents.Invoice.objects(invoice_id=invoice_id)
    if invoice == []:
        return "No such invoice"
    else:
        invoice = invoice[0]
    cur = sakhacabsgd.create(invoice.invoice_id)
    template = sakhacabsgd.open("InvoiceTemplate")
    t = template.worksheet_by_title("Invoice")
    cur.add_worksheet("Invoice", src_worksheet=t)
    invoicesheet = cur.worksheet_by_title("Invoice")
    cur.del_worksheet(cur.worksheet_by_title("Sheet1"))

    n = 15
    for line in invoice.invoicelines:
        print n, line
        invoicesheet.insert_rows(n - 1, 1)
        invoicesheet.update_row(n, ["", line['date'], line['particulars'],
                                    line['product'], line['qty'], line['rate'], "=F" + str(n) + "*E" + str(n)])
        n += 1
    totalcell = "G" + str(n + 2)
    print totalcell
    n = n + 4
    for line in invoice.taxes:
        invoicesheet.insert_rows(n - 1, 1)
        invoicesheet.update_row(n, ["", "", "", "", "", line['name'] + "(" + str(
            line['rate'] * 100) + "%)", "=" + totalcell + "*" + str(line['rate'])])
    n += 1
    custbil = invoicesheet.cell("B8")
    cust = documents.Customer.objects(cust_id=invoice.cust_id)[0]
    custbil.value = cust.cust_billing
    datecel = invoicesheet.cell("B5")
    datecel.value = "Submitted on " + invoice.invoice_date.strftime("%Y-%m-%d")
    idcel = invoicesheet.cell("F8")
    idcel.value = invoice.invoice_id
    duedatecel = invoicesheet.cell("F11")
    duedatecel.value = invoice.invoice_date.strftime("%Y-%d-%m")
    return cur.url


'''
Exporting everything
'''

def export_drivers():
    drivers = documents.Driver.objects.to_json()
    drivers = json.loads(drivers)
    for driver in drivers:
        del driver['_id']
    driverdf = pandas.DataFrame(drivers)
    driverdf.to_csv("./dispatcher/reports/drivers.csv")
    return "reports/drivers.csv"


def export_locupdates():
    locupdates = documents.LocationUpdate.objects.to_json()
    locupdates = json.loads(locupdates)
    for locupdate in locupdates:
        del locupdate['_id']
    locupdatedf = pandas.DataFrame(locupdates)
    locupdatedf.timestamp = locupdatedf.timestamp.apply(lambda x: datetime.datetime.fromtimestamp(
        (x['$date'] + 1) / 1000).strftime("%Y-%m-%d %H:%M:%S"))
    locupdatedf.to_csv("./dispatcher/reports/locupdates.csv")
    return "reports/locupdates.csv"


def export_vehicles():
    vehicles = documents.Vehicle.objects.to_json()
    vehicles = json.loads(vehicles)
    for vehicle in vehicles:
        del vehicle['_id']
    vehicledf = pandas.DataFrame(vehicles)
    vehicledf.to_csv("./dispatcher/reports/vehicles.csv")
    return "reports/vehicles.csv"


def export_bookings():
    bookings = documents.Booking.objects.to_json()
    bookings = json.loads(bookings)
    for booking in bookings:
        del booking['_id']
    bookingdf = pandas.DataFrame(bookings)
    bookingdf.created_timestamp = bookingdf.created_timestamp.apply(
        lambda x: datetime.datetime.fromtimestamp((x['$date'] + 1) / 1000).strftime("%Y-%m-%d %H:%M:%S"))
    bookingdf.pickup_timestamp = bookingdf.pickup_timestamp.apply(
        lambda x: datetime.datetime.fromtimestamp((x['$date'] + 1) / 1000).strftime("%Y-%m-%d %H:%M:%S"))
    bookingdf.to_csv("./dispatcher/reports/bookings.csv", encoding="utf-8")
    return "reports/bookings.csv"


'''
Bulk Imports of everything
'''


def import_bookings(bookinglist):
    sakhacabsxpal.logger.info("Booking list: {}".format(bookinglist))
    try:
        for booking in bookinglist:
            try:
                if validate_booking_dict(booking)['status'] is True:
                    b = new_booking(deepcopy(booking))

                    if type(b) == list:
                        b = b[0]
                        b.pickup_timestamp = utils.get_utc_ts(
                            b.pickup_timestamp)
                        b.save()
                        b.reload()
                        booking['status'] = b.booking_id
                    else:
                        booking['status'] = b
                else:
                    booking['status'] = "error: " + validate_booking_dict(booking)['message']
            except Exception as e:
                booking['status'] = "error: {} {}".format(type(e), str(e))
        return bookinglist
    except Exception as e:
        return "error: {} {}".format(type(e), str(e))


def import_drivers(driverlist):
    try:
        for driver in driverlist:
            try:
                if validate_driver_dict(driver)['status'] is True:
                    d = create_driver(driver)
                    if type(d) == list:
                        d = d[0]
                        d.save()
                        d.reload()
                        driver['status'] = d.driver_id
                    else:
                        driver['status'] = d
                else:
                    driver['status'] = validate_driver_dict(driver)['message']
            except Exception as e:
                driver['status'] = "{} {}".format(type(e), str(e))
        return driverlist
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def import_customers(customerlist):
    try:
        for customer in customerlist:
            try:
                if validate_customer_dict(customer)['status'] is True:
                    d = create_customer(customer)
                    if type(d) == list:
                        d = d[0]
                        d.save()
                        d.reload()
                        customer['status'] = d.cust_id
                    else:
                        customer['status'] = d
                else:
                    customer['status'] = validate_customer_dict(customer)[
                        'message']
            except Exception as e:
                customer['cust_id'] = "{} {}".format(type(e), str(e))
        return customerlist
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def import_products(productlist):
    try:
        for product in productlist:
            try:
                if validate_product_dict(product)['status'] is True:
                    d = create_product(product)
                    if type(d) == list:
                        d = d[0]
                        d.save()
                        d.reload()
                        product['status'] = d.product_id
                    else:
                        product['status'] = d
                else:
                    product['status'] = validate_product_dict(product)[
                        'message']
            except Exception as e:
                product['status'] = "{} {}".format(type(e), str(e))
        return productlist
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def import_vehicles(vehiclelist):
    try:
        for vehicle in vehiclelist:
            try:
                if validate_vehicle_dict(vehicle)['status'] is True:
                    d = create_vehicle(vehicle)
                    if type(d) == list:
                        d = d[0]
                        d.save()
                        d.reload()
                        vehicle['status'] = d.vehicle_id
                    else:
                        vehicle['status'] = d
                else:
                    vehicle['status'] = validate_vehicle_dict(vehicle)[
                        'message']
            except Exception as e:
                vehicle['status'] = "{} {}".format(type(e), str(e))
        return vehiclelist
    except Exception as e:
        return "{} {}".format(type(e), str(e))
