#!/u*-
"""
Created on Sat Sep  8 21:52:07 2018

@author: arjun
"""


import sys,datetime,json

sys.path.append("/opt/xetrapal")
import xetrapal
sakhacabsxpal=xetrapal.Xetrapal(configfile="/home/arjun/sakhacabs/sakhacabsxpal.conf")
sakhacabsgd=sakhacabsxpal.get_googledriver()
datasheet=sakhacabsgd.open_by_key(sakhacabsxpal.config.get("SakhaCabs","datasheetkey"))
bookingsheet=datasheet.worksheet_by_title("bookings")
custsheet=datasheet.worksheet_by_title("customers")
carsheet=datasheet.worksheet_by_title("cars")
driversheet=datasheet.worksheet_by_title("drivers")
prodsheet=datasheet.worksheet_by_title("product")
#Setting up mongoengine connections
sakhacabsxpal.logger.info("Setting up MongoEngine")
import mongoengine
mongoengine.connect('sakhacabs', alias='default')

import pandas

from sakhacabs import documents,utils

def sync_remote():
    custlist=custsheet.get_as_df().to_dict(orient="records")
    driverlist=driversheet.get_as_df().to_dict(orient="records")
    carlist=carsheet.get_as_df().to_dict(orient="records")
    bookinglist=bookingsheet.get_as_df().to_dict(orient="records")
    productlist=prodsheet.get_as_df().to_dict(orient="records")
    for driver in driverlist:
        if len(documents.Driver.objects(driver_id=driver['driver_id']))==0:
            d=documents.Driver(driver_id=driver['driver_id'],mobile_num=str(driver['mobile_num']),first_name=driver['first_name'],last_name=driver['last_name'])
            d.save()
    driverdf=pandas.DataFrame(json.loads(documents.Driver.objects.to_json()))
    driverdf['_id']=driverdf['_id'].apply(lambda x: x['$oid'])
    driversheet.set_dataframe(driverdf,(1,1))
    
    for customer in custlist:
        if len(documents.Customer.objects(cust_id=customer['cust_id']))==0:
            c=documents.Customer(cust_id=customer['cust_id'],mobile_num=customer['mobile_num'],cust_type=customer['cust_type'],blacklisted=customer['blacklisted'],email=customer['email'],cust_name=customer['cust_name'])
            c.save()
    customerdf=pandas.DataFrame(json.loads(documents.Customer.objects.to_json()))
    customerdf['_id']=customerdf['_id'].apply(lambda x: x['$oid'])
    custsheet.set_dataframe(customerdf,(1,1))
    
    for car in carlist:
        if len(documents.Vehicle.objects(vehicle_id=car['vehicle_id']))==0:
            v=documents.Vehicle(vehicle_id=car['vehicle_id'],model=car['model'],make=car['make'],reg_num=car['reg_num'])
            v.save()
    cardf=pandas.DataFrame(json.loads(documents.Vehicle.objects.to_json()))
    cardf['_id']=cardf['_id'].apply(lambda x: x['$oid'])
    if 'driver' in cardf.columns:
        cardf['driver']=cardf['driver'].apply(lambda x: x['$oid'])
    carsheet.set_dataframe(cardf,(1,1))
    
    
    for product in productlist:
        if len(documents.Product.objects(product_id=product['product_id']))==0:
            p=documents.Product(product_id=product['product_id'],name=product['name'],price=product['price'],desc=product['desc'])
            p.save()
    productdf=pandas.DataFrame(json.loads(documents.Product.objects.to_json()))
    productdf['_id']=productdf['_id'].apply(lambda x: x['$oid'])
    prodsheet.set_dataframe(productdf,(1,1))
    
    
    for booking in bookinglist:
        if len(documents.Product.objects(product_id=product['product_id']))==0:
            p=documents.Product(product_id=product['product_id'],name=product['name'],price=product['price'],desc=product['desc'])
            p.save()
    productdf=pandas.DataFrame(json.loads(documents.Product.objects.to_json()))
    productdf['_id']=productdf['_id'].apply(lambda x: x['$oid'])
    prodsheet.set_dataframe(productdf,(1,1))
    
    bookingdf=bookingsheet.get_as_df()
    bookingdf.created_timestamp=bookingdf.created_timestamp.apply(pandas.to_datetime).apply(utils.get_utc_ts)
    bookingdf.pickup_timestamp=bookingdf.pickup_timestamp.apply(pandas.to_datetime).apply(utils.get_utc_ts)
    bookinglist=bookingdf.to_dict(orient="records")
    delkeys=["passenger_detail", "created_timestamp", "pickup_timestamp", "pickup_location", "drop_location", "product_id", "cust_id", "booking_channel","booking_id","_id","cust_meta"]
    for booking in bookinglist:
        
        if booking["booking_id"]=="":
            while True:
                booking_id=utils.new_booking_id()
                if len(documents.Booking.objects(booking_id=booking_id,cust_id=booking['cust_id']))==0:
                    break
            b=documents.Booking(booking_id=booking_id,created_timestamp=booking['created_timestamp'],passenger_detail=booking['passenger_detail'],
                pickup_timestamp=booking['pickup_timestamp'],pickup_location=booking['pickup_location'],
                drop_location=booking['drop_location'],product_id=booking['product_id'],cust_id=booking['cust_id'],
                booking_channel=booking['booking_channel'])
            print booking['cust_meta']
            
            b.cust_meta=json.loads(booking['cust_meta'])
            newdelkeys=[]
            for key,value in booking.iteritems():
                if value=="":
                    newdelkeys.append(key)
            
            #print delkeys
            for key in delkeys:
                booking.pop(key,None)
            for key in newdelkeys:
                booking.pop(key,None)
                    
            
            print b.to_json()
            b.save()
    newbookingsdf=pandas.DataFrame(json.loads(documents.Booking.objects.to_json()))
    newbookingsdf.created_timestamp= newbookingsdf.created_timestamp.apply(lambda x: datetime.datetime.fromtimestamp(x['$date']/1000).strftime("%Y-%m-%d %H:%M:%S"))
    newbookingsdf.pickup_timestamp= newbookingsdf.pickup_timestamp.apply(lambda x: datetime.datetime.fromtimestamp(x['$date']/1000).strftime("%Y-%m-%d %H:%M:%S"))
    newbookingsdf['_id']=newbookingsdf['_id'].apply(lambda x: x['$oid'])
    newbookingsdf.cust_meta=newbookingsdf.cust_meta.astype(str)
    bookingsheet.set_dataframe(newbookingsdf,(1,1))

    
#Fix to check if vehicle is already  taken. 
def new_locationupdate(driver,timestamp,checkin=True,location=None,vehicle=None,handoff=None,logger=xetrapal.astra.baselogger,**kwargs): 
    vehicle_id=None
    if checkin==True:
        driver.checkedin=True
        if vehicle!=None:
            vehicle.driver=driver
            vehicle.save()
            vehicle_id=vehicle.vehicle_id
    
    if checkin==False:
        driver.checkedin=False
        if len(documents.Vehicle.objects(driver=driver))>0:
            v=documents.Vehicle.objects(driver=driver)
            for vh in v:
                del vh.driver
                vh.save()
    
    driver.save()
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    adjtimestamp = timestamp + UTC_OFFSET_TIMEDELTA
    # Get new location update and save it
    locationupdate=documents.LocationUpdate(driver_id=driver.driver_id,timestamp=adjtimestamp,location=location,checkin=checkin,handoff=handoff,vehicle_id=vehicle_id)
    
    # Tell the user what happened
    if checkin==True:
        logger.info(u"New checkin from driver with id {} at {} from {}".format(locationupdate.driver_id,locationupdate.timestamp,locationupdate.location))
    else:
        logger.info(u"Checkout from driver with id {} at {} from {}".format(locationupdate.driver_id,locationupdate.timestamp,locationupdate.location))
    locationupdate.save()
    
    return locationupdate


def get_driver_by_mobile(mobile_num):
    t=documents.Driver.objects(mobile_num=mobile_num)
    xetrapal.astra.baselogger.info("Found {} drivers with Mobile Num {}".format(len(t),mobile_num))
    if len(t)>0:
        #return[User(x['value']) for x in t][0]
        return t[0]
    else:
        return None



def get_driver_by_tgid(tgid):
    t=documents.Driver.objects(tgid=tgid)
    xetrapal.astra.baselogger.info("Found {} drivers with Telegram ID {}".format(len(t),tgid))
    if len(t)>0:
        #return[User(x['value']) for x in t][0]
        return t[0]
    else:
        return None


def get_vehicle_by_vid(vid):
    #t=db.view("vehicle/all_by_vnum",keys=[vnum]).all()
    t=documents.Vehicle.objects(vehicle_id=vid)
    
    if len(t)>0:
        #return [Vehicle(x['value']) for x in t][0]
        return t[0]
    else:
        return None


'''

def get_driver_by_driver_id(mobile_num):
    t=documents.Driver.objects(mobile_num=mobile_num)
    xetrapal.astra.baselogger.info("Found {} drivers with Mobile Num {}".format(len(t),mobile_num))
    if len(t)>0:
        #return[User(x['value']) for x in t][0]
        return t[0]
    else:
        return None



'''