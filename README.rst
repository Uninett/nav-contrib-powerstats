===================================
 NAV Power Stats
===================================

Install
-------

``pip install git+https://github.com/Uninett/nav-contrib-powerstats.git``

Example config
--------------

- Go to NAV config directory
- Create directory ``python`` if it does not exist, and enter it
- Create file ``local_urls.py``::

    from django.conf.urls import url, patterns
    from navpowerstats.views import render_power_sensors
    urlpatterns = patterns(
        '',
        url(r'^ajax/open/powersensors/(?P<roomid>.+)', render_power_sensors,
            name='room-info-power'),
    )

- Create file ``local_settings.py``::

    LOCAL_SETTINGS = True
    from nav.django.settings import *
    INSTALLED_APPS += (
        'navpowerstats',
    )

- Run collectstatic::

    cd python/nav/django
    python ./manage.py collectstatic

- Reload Apache


Developement
------------

- hg clone <dir>
- cd <dir>
- python setup.py sdist
- pip install dist/NAVPowerStatistics-0.x.tar.gz
- Copy css and js files to static dir
