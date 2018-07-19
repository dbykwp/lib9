from js9 import j
from JumpScale9Lib.servers.grid_capacity.server.models import FarmerRegistration, NodeRegistration

influxcl = j.clients.influxdb.get('capacity', interactive=False)
influxcl.create_database("capacity")

def get_hours_in_days(days=1):
    return days*24

def get_farmer_up_period_since_days(iyo, days=30):
    q = get_farmer_up_in_last(iyo, days)

    res = list(q['capacitybeats'])
    if not res or "count" not in res[0]:
        return 0
    count = res[0]['count']  # every 10 seconds
    return count/(6*60)

def get_farmer_up_in_last(iyo_org, days=30):
    q = influxcl.query(
        """select count("up") from capacitybeats where "farmer_id" = '{}' and time > now()- {}d """.format(iyo_org, days, database='capacity'))
    return q


def get_node_up_period_since_days(node_id, days=30):
    q = get_node_up_in_last(node_id, days)
    res = list(q['capacitybeats'])
    if not res or "count" not in res[0]:
        return 0
    count = res[0]['count']  # every 5 seconds
    return count/(6*60)

def get_node_up_in_last(node_id, days=30):
    q = influxcl.query(
        """select count("up") from capacitybeats where "node_id" = '{}' and time > now()- {}d """.format(node_id, days, database='capacity'))
    return q


def get_farmer_complete_capacity(iyo_org):
    nodes = NodeRegistration.search(farmer=iyo_org)
    return dict(total_cru=sum([n.cru for n in nodes if n.cru]),
                total_mru=sum([n.mru for n in nodes if n.mru]),
                total_hru=sum([n.hru for n in nodes if n.hru]),
                total_sru=sum([n.sru for n in nodes if n.sru])
            )

def push_node_heartbeat(farmer_id, node_id):

    points = [{
        "measurement": "capacitybeats",
        "tags":{"node_id": node_id, "farmer_id": farmer_id},
        "fields":{"up": 1} 
    }]
    try:
        influxcl.write_points(points, database='capacity')
    except Exception as ex:
        print(ex)
        # don't fail here.


def push_node_heartbeat_with_time(farmer_id, node_id, time_):
    points = [{
        "measurement": "capacitybeats",
        "tags":{"node_id": node_id, "farmer_id": farmer_id},
        "time":time_,       
        "fields":{
            "up": 1,
        } 

    }]
    try:
        influxcl.write_points(points, database='capacity')
    except Exception as ex:
        print(ex)
        # don't fail here.
 