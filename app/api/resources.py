"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import request
from flask_restplus import Resource
from flask import Flask, request, jsonify
import io
from flask import Response
from .security import require_auth
from . import api_rest
from .business_logic import room_creator, enter_room, toggle_polling, check_participants

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
