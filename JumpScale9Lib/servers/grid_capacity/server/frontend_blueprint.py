# DO NOT EDIT THIS FILE. This file will be overwritten when re-running go-raml.
import os
from flask import Blueprint, send_from_directory, render_template, request, session

from .models import NodeRegistration, FarmerRegistration

frontend_bp = Blueprint('frontent', __name__)

dir_path = os.path.dirname(os.path.realpath(__file__))


@frontend_bp.route('/static/<path:path>')
def send_js(path):
    return send_from_directory(dir_path, os.path.join('static', path))


@frontend_bp.route('/', methods=['GET'])
def capacity():
    countries = NodeRegistration.all_countries()
    farmers = [f.iyo_organization for f in FarmerRegistration.list()]
    nodes = []
    form = {
        'mru': 0,
        'cru': 0,
        'sru': 0,
        'hru': 0,
        'country': '',
    }

    if len(request.args) != 0:
        mru = request.args.get('mru') or None
        if mru:
            form['mru'] = int(mru)
        cru = request.args.get('cru') or None
        if cru:
            form['cru'] = int(cru)
        sru = request.args.get('sru') or None
        if sru:
            form['sru'] = int(sru)
        hru = request.args.get('hru') or None
        if hru:
            form['hru'] = int(hru)
        form['country'] = request.args.get('country') or ''
        form['farmer'] = request.args.get('farmer') or ''

        form['page'] = int(request.args.get('page') or 1)
        form['per_page'] = int(request.args.get('pre_page') or 20)

        nodes = NodeRegistration.search(**form)

    return render_template('capacity.html', nodes=nodes, form=form, countries=countries, farmers=farmers)


@frontend_bp.route('/farmers', methods=['GET'])
def list_farmers():
    farmers = FarmerRegistration.list()
    return render_template('farmers.html', farmers=farmers)


@frontend_bp.route('/farm_registered', methods=['GET'])
def farmer_registered():
    jwt = session['iyo_jwt']
    return render_template('farm_registered.html', jwt=jwt)


@frontend_bp.route('/api', methods=['GET'])
def api_index():
    return render_template('api.html')
