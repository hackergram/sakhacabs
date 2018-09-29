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
from flask_potion import Api, ModelResource, fields
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

    
class UserResource(ModelResource):
    class Meta:
        name = 'user'
        model = User

    class Schema:
        telegram_id = fields.Integer()
api.add_resource(UserResource)

