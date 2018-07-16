from js9 import j
influxcl = j.clients.influxdb.get('capacity')


def get_farmer_up_period_since_days(iyo, days):
    q = get_farmer_up_in_last(iyo, days)
    res = list(q['capacitybeats'])
    if not res or "count" not in res[0]:
        return 0

    count = res[0]['count'] # every 5 seconds 
    return count/(12*60)
    


def get_farmer_up_in_last(iyo_org, days=30):
    q = influxcl.query("""select count("up") from capacitybeats where "farmer_id" = '{}' and time > now()- {}d """.format(iyo_org, days, database='capacity'))
    return  q