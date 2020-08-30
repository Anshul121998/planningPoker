"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import request
from flask_restplus import Resource
from flask import Flask, request, jsonify
import io
import random
from flask import Response
from .security import require_auth
from . import api_rest
import uuid


class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]

@api_rest.route('/planningPoker/createRoom/<string:resource_id>')
class SecureResourceOne(SecureResource):
    def post(self, resource_id):
        return jsonify(room_creator(request.get_json()))

@api_rest.route('/planningPoker/enterRoom/<string:resource_id>')
class SecureResourceOne(SecureResource):
    def post(self, resource_id):
        return jsonify(enter_room(request.get_json()))

@api_rest.route('/planningPoker/togglePolling/<string:resource_id>')
class SecureResourceOne(SecureResource):
    def post(self, resource_id):
        return jsonify(toggle_polling(request.get_json()))

@api_rest.route('/planningPoker/checkParticipants/<string:resource_id>')
class SecureResourceOne(SecureResource):
    def post(self, resource_id):
        return jsonify(check_participants(request.get_json()))

# @api_rest.route('/secure-getValues/<string:resource_id>')
# class SecureResourceOne(SecureResource):
#     def get(self, resource_id):
#         return 1

dataStorage = {}

def room_creator(json_data):
    if json_data['uuid'] == '':
        my_uuid = str(uuid.uuid4())
        while json_data['uuid'] in dataStorage:
            my_uuid = str(uuid.uuid4())
        dataStorage[my_uuid] = {
            'polling' : False,
            'attendees' : [],
            'creator' : json_data['name'],
            'topPeople' : [],
            'datetime' : json_data['datetime'],
            'topEstimate' : '',
            'topEstimateNumber' : -1
        }
        return {
            'uuid' : my_uuid,
            'polling' : False
        }
    else:
        if json_data['uuid'] in dataStorage:
            return {
                'uuid' : json_data['uuid'],
                'polling' : dataStorage[json_data['uuid']]['polling']
            }
    return {
        'uuid' : '1',
        'polling' : False
    }

def enter_room(json_data):
    if json_data['uuid'] in dataStorage:
        exists = False
        loc = -1
        for i in range(0, len(dataStorage[json_data['uuid']]['attendees'])):
            if(dataStorage[json_data['uuid']]['attendees'][i]['name'] == json_data['name']):
                exists = True
                loc = i
                break
        if dataStorage[json_data['uuid']]['polling'] and exists:
            dataStorage[json_data['uuid']]['attendees'][loc]['estimate'] = json_data['estimate']
            store_top_estimate(json_data['uuid'], json_data['estimate'], dataStorage[json_data['uuid']]['attendees'][loc]['name'])
            return 1
        elif dataStorage[json_data['uuid']]['polling'] and not exists:
            dataStorage[json_data['uuid']]['attendees'].append({'name' : json_data['name'], 'estimate' : json_data['estimate']})
            store_top_estimate(json_data['uuid'], json_data['estimate'], json_data['name'])
            return 1
        elif not dataStorage[json_data['uuid']]['polling'] and not exists:
            dataStorage[json_data['uuid']]['attendees'].append({'name' : json_data['name'], 'estimate' : -1})
            return 0
        else:
            return 0
    else:
        return -1
    
def store_top_estimate(data_uuid, val, name):
    if val == 'Infinity':
        if 'Infinity' != dataStorage[data_uuid]['topEstimate']:
            dataStorage[data_uuid]['topEstimateNumber'] = 1000
            dataStorage[data_uuid]['topEstimate'] = val
            dataStorage[data_uuid]['topPeople'] = []
    else:
        if float(val) > dataStorage[data_uuid]['topEstimateNumber']:
            dataStorage[data_uuid]['topEstimateNumber'] = float(val)
            dataStorage[data_uuid]['topEstimate'] = val
            dataStorage[data_uuid]['topPeople'] = []
    if val == dataStorage[data_uuid]['topEstimate'] and name not in dataStorage[data_uuid]['topPeople']:
        dataStorage[data_uuid]['topPeople'].append(name)

def toggle_polling(json_data):
    if json_data['uuid'] in dataStorage:
        if json_data['polling']:
            dataStorage[json_data['uuid']]['attendees'] = []
            dataStorage[json_data['uuid']]['topEstimateNumber'] = -1
            dataStorage[json_data['uuid']]['topEstimate'] = ''
            dataStorage[json_data['uuid']]['topPeople'] = []
            dataStorage[json_data['uuid']]['polling'] = json_data['polling']
            return 1
        else:
            dataStorage[json_data['uuid']]['polling'] = False
            return dataStorage[json_data['uuid']]
    else:
        return 0

def check_participants(json_data):
    if json_data['uuid'] in dataStorage:
        user_list = []
        for i in dataStorage[json_data['uuid']]['attendees']:
            user_list.append(i['name'])
        return user_list
    else:
        return 0
