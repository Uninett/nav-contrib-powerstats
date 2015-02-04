#!/usr/bin/env/python
#
# Copyright (C) 2014 UNINETT AS
#
# This file is part of Network Administration Visualized (NAV).
#
# NAV is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.  You should have received a copy of the GNU General Public
# License along with NAV. If not, see <http://www.gnu.org/licenses/>.
#
"""Module comment"""

from setuptools import setup

setup(name='NAVPowerStatistics',
      version='0.2',
      description='NAV Power Statistics for Rooms',
      author='John-Magne Bredal',
      author_email='john.m.bredal@uninett.no',
      url='https://bitbucket.org/bredal/nav-contrib-powerstats',
      packages=['navpowerstats'],
      package_data={'navpowerstats': ['templates/*.html', 'static/*.js', 'static/*.css']},
      include_package_data=True)
