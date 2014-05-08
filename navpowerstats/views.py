import re
from collections import defaultdict
from nav.models.manage import Room
from django.shortcuts import get_object_or_404, render


def render_power_sensors(request, roomid):
    """Gets the power devices for a room"""

    room = get_object_or_404(Room, pk=roomid)
    grouped_racks = group_by_rack(room.netbox_set.filter(
        category='POWER', sysname__startswith='pdu-'
    ).order_by('sysname'))
    ups = room.netbox_set.filter(category='POWER', sysname__startswith='ups')

    metric_mapping = get_metrics(ups)

    return render(request, 'info/room/roominfo_power.html', {
        'racks': grouped_racks,
        'ups': ups,
        'metric_mapping': metric_mapping
    })


def group_by_rack(netboxes):
    """Groups the netboxes by rack which is given in sysname"""
    racks = defaultdict(dict)

    for netbox in netboxes:
        rack_number, rack_index = get_rack_info(netbox.sysname)
        rack_type = 'ups' if rack_index == 'a' else 'by'
        sensors = netbox.sensor_set.exclude(
            internal_name__endswith=1).order_by('internal_name')

        racks[rack_number][rack_type] = {
            'netbox': netbox,
            'shortname': get_shortname(netbox.sysname),
            'sensors': sensors
        }

    results = []
    for index in sorted(racks.keys()):
        results.append({
            'number': index,
            'pdus': racks[index]
        })

    return results


def get_rack_info(sysname):
    """Finds rack number from sysname of a PDU"""
    number, index = re.search(r'pdu-r(\d+)(\w)', sysname).groups()
    return int(number), index


def get_shortname(sysname):
    """Custom formatting of shortname for a pdu given a sysname"""
    return re.sub(r'pdu-(\w+)\..*', r'\1', sysname)


def get_metrics(ups):
    """Creates internal_name -> metric_name mapping for all sensors"""
    mapping = {}
    for up in ups:
        metrics = {}
        for sensor in up.sensor_set.all():
            metrics[sensor.internal_name] = sensor.get_metric_name()
        mapping[up.sysname] = metrics
    return mapping

