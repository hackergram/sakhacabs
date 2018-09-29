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
from flask_restful import Api, Resource
import json
#from flask.ext.potion.contrib.mongoengine.manager import MongoEngineManager

app = Flask(__name__)
app.config.update(
    MONGODB_HOST = 'localhost',
    MONGODB_PORT = '27017',
    MONGODB_DB = 'sakhacabs',
)
CORS(app)
me = MongoEngine(app)

api = Api(app)

    
class UserResource(Resource):
    def get(self,role=None,telegram_id=None,mobile_num=None):
        if role:
            return jsonify({"resp": json.loads(User.objects(role=role).to_json())})
        elif telegram_id:
            return jsonify({"resp": json.loads(User.objects(telegram_id=telegram_id).to_json())})
        elif mobile_num:
            return jsonify({"resp": json.loads(User.objects(telegram_id=telegram_id).to_json())})
        else:
            return jsonify({"resp": json.loads(User.objects.to_json())})
api.add_resource(UserResource,"/user",endpoint="users")
api.add_resource(UserResource,"/user/role/<string:role>",endpoint="role")
api.add_resource(UserResource,"/user/by_tgid/<int:telegram_id>",endpoint="telegram_id")
api.add_resource(UserResource,"/user/by_tgid/<string:mobile_num>",endpoint="telegram_id")
