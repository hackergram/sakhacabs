#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 15:52:12 2018

@author: arjun
"""

for user in driversakhabot.users:
    print user
    tgid=user['id']
    del user['id']
    newuser=User(telegram_id=tgid,role='driver',metadata=user)
    print newuser.metadata
    
    

    
    newuser.save()
sakhacabsgd=sakhacabsxpal.get_googledriver()
carsdf=datasheet.worksheet_by_title("cars").get_as_df()
datasheet=sakhacabsgd.open_by_key("1QDzE009LaHhNbcF-xy5Fo1Kjj2Lj_u7iayITphcH1T4")
carsdf=datasheet.worksheet_by_title("cars").get_as_df()
carlist=json.loads(carsdf.to_json(orient="records"))
for car in carlist:
    vnum=str(car['vehicle_num'])
    del car['vehicle_num']
    v=Vehicle(vehicle_num=vnum,vehicle_meta=car)
    print v.to_json()
    v.save()
