# THIS FILE IS SAFE TO EDIT. It will not be overwritten when rerunning go-raml.
from flask import request, jsonify
from ..models import FarmerRegistration
from ..grid_stats import get_farmer_up_period_since_days

def ListFarmersHandler():
    farmers = FarmerRegistration.list()
    output = []
    for farmer in farmers.all():
        f = farmer.to_mongo().to_dict()
        f['iyo_organization'] = f.pop('_id')
        f['last_month_uptime_in_hours'] = get_farmer_up_period_since_days(farmer.iyo_organization)
        output.append(f)
    return jsonify(output)
