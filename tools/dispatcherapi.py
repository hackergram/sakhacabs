#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:54:42 2018

@author: arjun
"""
from driversakhabotmongo import *
from flask import Flask, jsonify
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_mongorest import MongoRest
from flask_mongorest.views import ResourceView
from flask_mongorest.resources import Resource
from flask_mongorest import operators as ops
from flask_mongorest import methods

app = Flask(__name__)
app.config.update(
    MONGODB_HOST = 'localhost',
    MONGODB_PORT = '27017',
    MONGODB_DB = 'sakhacabs',
)
CORS(app)
db = MongoEngine(app)
api = MongoRest(app)

class UserResource(Resource):
    document = User
    filters = {
        'telegram_id': [ops.Exact],
        'mobile_num': [ops.Exact],
    }
    
@api.register(name='user', url='/user/')
class UserView(ResourceView):
    resource = UserResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

'''
@app.route("/user/all")
def api_get_users():
    return User.objects.to_json()

@app.route("/user/by_tgid/<tgid>")
def api_get_user_by_tgid(tgid):
    user=get_user_by_tgid(tgid)
    return jsonify(json_loads(user.to_json()))

@app.route("/user/by_id/<idstring>")
def api_user_by_id(idstring):
    user=get_user_by_id(idstring)
    if user:
        return jsonify({"resp":json.loads(user.tojson())})
    else:
        return jsonify({"resp":None})



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

@app.route("/vehicle/by_id/<idstring>")
def api_vehicle_by_id(idstring):    
    vehicle=get_vehicle_by_id(idstring)
    if vehicle:
        return jsonify({"resp":json.loads(vehicle.to_json())})
    else:
        return jsonify({"resp":None})

@app.route("/locupdate/all")
def api_get_locupdates():
    return jsonify({"resp":json.loads(LocationUpdate.objects.to_json())})

@app.route("/locupdate/by_driver/<tgid>")
def api_get_locupdates_for_driver(tgid):
    return None
    
'''





