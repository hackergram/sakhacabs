#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 11:33:20 2018

@author: lilhack110
"""

import pygsheets
gd=pygsheets.authorize("/home/lilhack110/authdir/sheets.googleapis.com-python.json")
sakha=gd.open_by_key("1a5U8WAN6PclcGCGMyhKENDVkZ3LegNkyjEZTWPBI5NQ")
sakha_ws=sakha.worksheet_by_title("Sheet1")
sakhadf=sakha_ws.get_as_df()
sakhadf.columns

#sakhadf.drop(sakhadf.ix[:,'Duty Cancelled':'No o f Ride'].head(0).columns, axis=1)
#sakha_cabs_df_drop=sakhadf.drop(sakhadf.ix[:,'Duty Cancelled':'No o f Ride'].head(0).columns, axis=1)
#gd.list_ssheets()
sakha=gd.open_by_key("1QDzE009LaHhNbcF-xy5Fo1Kjj2Lj_u7iayITphcH1T4")
sakha_ws=sakha.worksheet_by_title("2018")
sakhadf=sakha_ws.get_as_df()
#sakha_cabs_df_drop=sakhadf.drop(sakhadf.ix[:,'Duty Cancelled':'No o f Ride'].head(0).columns, axis=1)
#sakha_cabs_df_drop.columns
#sakhacdf = sakha_cabs_df_drop.fillna(method='ffill')
#sakhacdf
#sakhacdf.head()
import pymongo
client= pymongo.MongoClient("mongodb://localhost:27017/")
sakha1=client.sakha
roster1=sakha1.mis_roster_pwc1
#client.list_database_names
print(client.list_database_names())

roster1.insert_many(sakhadf.to_dict('records'))