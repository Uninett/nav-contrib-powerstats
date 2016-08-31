"""Separate util module for easier testing"""

import re

def get_rack_info(sysname):
    """Finds rack number and position from sysname of a PDU"""
    shortname = get_rack_definition(sysname)
    regex = re.compile(r'^r(?P<rack_number>\d+)(?P<position>\w)$')
    match = regex.search(shortname)
    return int(match.group('rack_number')), match.group('position')


def get_rack_definition(sysname):
    """Finds the rack defining part of the sysname

    pdu-r2a.uninett.no -> r2a
    """
    return re.sub(r'pdu-.*-?(r\d+\w)\..*', r'\1', sysname)
