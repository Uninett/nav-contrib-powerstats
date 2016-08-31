"""Controller functions for power sensor rendering

pdu's are required to have a certain naming standard. They need to have the
category 'POWER' and the sysname must start with 'pdu-'
"""

from collections import defaultdict
from nav.models.manage import Room
from django.shortcuts import get_object_or_404, render
from .utils import get_rack_info


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
            'sensors': sensors
        }

    results = []
    for index in sorted(racks.keys()):
        results.append({
            'number': index,
            'pdus': racks[index]
        })

    return results


def get_metrics(upses):
    """Creates internal_name -> metric_name mapping for all sensors"""
    mapping = {}
    for ups in upses:
        metrics = {}
        for sensor in ups.sensor_set.all():
            metrics[sensor.internal_name] = sensor.get_metric_name()
        mapping[ups.sysname] = metrics
    return mapping
