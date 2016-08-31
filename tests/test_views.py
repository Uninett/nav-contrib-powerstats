"""Test package

To test: python -m pytest
"""
from navpowerstats.utils import get_rack_info, get_rack_definition

_SYSNAME1 = 'pdu-r2a.uninett.no'
_SYSNAME2 = 'pdu-something-r2a.uninett.no'

def test_get_rack_info_min():
    """Test with minimum name"""
    assert get_rack_info(_SYSNAME1) == (2, 'a')

def test_get_rack_info():
    """Test with extended name"""
    assert get_rack_info(_SYSNAME2) == (2, 'a')

def test_get_rack_definition_min():
    """Test with minimum name"""
    assert get_rack_definition(_SYSNAME1) == 'r2a'

def test_get_rack_definition():
    """Test with extended name"""
    assert get_rack_definition(_SYSNAME2) == 'r2a'
