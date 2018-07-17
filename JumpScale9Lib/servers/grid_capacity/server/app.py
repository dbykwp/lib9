import os
import sys
import datetime

from flask import Flask, jsonify
from js9 import j

from . import settings
from .flask_itsyouonline import configure
from .models import db
from .grid_stats import get_farmer_up_period_since_days, get_node_up_period_since_days

app = Flask(__name__)

app.secret_key = os.urandom(24)
configure(app, settings.IYO_CLIENTID, settings.IYO_SECRET, settings.IYO_CALLBACK, '/callback', None, True, True, 'organization')

# connect to mongodb
j.clients.mongoengine.get('capacity', interactive=False)


from flask_debugtoolbar import DebugToolbarExtension
# the toolbar is only enabled in debug mode:
app.debug = True
toolbar = DebugToolbarExtension(app)


db.init_app(app)

from .api_api import api_api
from .frontend_blueprint import frontend_bp

app.register_blueprint(api_api)
app.register_blueprint(frontend_bp)


@app.template_filter()
def uptime(seconds):
    if not seconds:
        return "not available"

    delta = datetime.timedelta(seconds=seconds)

    # manually compute hh:mm:ss
    hrs = int(delta.seconds / 3600)
    min = int((delta.seconds - (hrs * 3600)) / 60)
    sec = delta.seconds % 60

    if delta.days > 0:
        return '%d days, %02d:%02d:%02d' % (delta.days, hrs, min, sec)

    return '%02d:%02d:%02d' % (hrs, min, sec)

@app.template_filter()
def farmer_uptime_last_month_in_hours(farmer):
    return "{:.3f}".format(get_farmer_up_period_since_days(farmer.iyo_organization))
    
@app.template_filter()
def farmer_uptime_last_month_in_percent(farmer):
    return "{:.3f}".format( get_farmer_up_period_since_days(farmer.iyo_organization) * 100 / (30 * 24))


@app.template_filter()
def node_uptime_last_month_in_hours(node):
    return "{:.3f}".format(get_node_up_period_since_days(node.node_id))
    
@app.template_filter()
def node_uptime_last_month_in_percent(node):
    return "{:.3f}".format(get_node_up_period_since_days(node.node_id) * 100 / (30*24))


@app.template_filter()
def deltatime_color(time):
    """
    return a color base on the delta time between now and time

    :param time: time we when to compare
    :type time: datetime.datetime
    :return: color
    :rtype: str
    """
    if not time:
        return 'danger'

    delta = (datetime.datetime.now() - time).total_seconds()
    if delta < 7200:  # less then 2h
        return 'success'
    if 7200 < delta and delta < 10800:  # between 2h and 3h
        return 'warning'
    if delta > 10800:  # plus de 3h
        return 'danger'


@app.errorhandler(500)
def internal_error(err):
    _, _, exc_traceback = sys.exc_info()
    eco = j.core.errorhandler.parsePythonExceptionObject(err, tb=exc_traceback)
    return jsonify(code=500, message=eco.errormessage, stack_trace=eco.traceback), 500


if __name__ == "__main__":
    app.run(debug=True, port=settings.PORT, host=settings.PORT)
