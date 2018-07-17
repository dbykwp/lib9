# THIS FILE IS SAFE TO EDIT. It will not be overwritten when rerunning go-raml.

import json as JSON
import os
from datetime import datetime

import jsonschema
from jsonschema import Draft4Validator

import jose.jwt
from flask import jsonify, request
from js9 import j

from ..models import Capacity, Farmer
from ..grid_stats import push_node_beat
from ..flask_itsyouonline import ITSYOUONLINE_KEY

dir_path = os.path.dirname(os.path.realpath(__file__))
Capacity_schema = JSON.load(open(dir_path + '/schema/Capacity_schema.json'))
Capacity_schema_resolver = jsonschema.RefResolver('file://' + dir_path + '/schema/', Capacity_schema)
Capacity_schema_validator = Draft4Validator(Capacity_schema, resolver=Capacity_schema_resolver)


def RecordCapacityBeatHandler():
    inputs = request.get_json()
    # refresh jwt is needed otherwise return original
    jwt = j.clients.itsyouonline.refresh_jwt_token(inputs.pop('farmer_id'))
    token = jose.jwt.decode(jwt, ITSYOUONLINE_KEY)
    iyo_organization = token['scope'][0].replace('user:memberof:', '')
    farmer = Farmer.objects(iyo_organization=iyo_organization).first()
    if not farmer:
        return jsonify(errors='Unauthorized farmer'), 403

    try:
        Capacity_schema_validator.validate(inputs)
    except jsonschema.ValidationError as e:
        return jsonify(errors="bad request body: {}".format(e)), 400
    
    inputs['farmer'] = iyo_organization
    inputs['updated'] = datetime.now()

    capacity = Capacity(**inputs)

    push_node_beat(farmer.iyo_organization, capacity.node_id)
    return capacity.to_json(use_db_field=False), 201, {'Content-type': 'application/json'}