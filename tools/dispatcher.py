#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:54:42 2018

@author: arjun
"""
from driversakhabotmongo import *
from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/user/all")
def api_get_users():
    return User.objects.to_json()

@app.route("/user/by_tgid/<tgid>")
def api_get_user_by_tgid(tgid):
    user=get_user_by_tgid(tgid)
    return jsonify(json_loads(user.to_json()))
@app.route("/driver/all")
def api_get_drivers():
    return jsonify({"resp":json.loads(User.objects(role="driver").to_json())})

@app.route("/driver/by_tgid/<tgid>")
def api_get_driver_by_tgid(tgid):
    driver=get_driver_by_tgid(tgid)
    return jsonify(json_loads(driver.to_json()))
    
@app.route("/vehicle/all")
def api_get_vehicles():
    return jsonify({"resp":json.loads(Vehicle.objects.to_json())})

@app.route("/vehicle/by_vnum/<vnum>")
def api_get_vehicle_by_vnum(vnum):
    return None

@app.route("/locupdate/all")
def api_get_locupdates():
    return jsonify({"resp":json.loads(LocationUpdate.objects.to_json())})

@app.route("/locupdate/by_driver/<tgid>")
def api_get_locupdates_for_driver(tgid):
    return None
    







