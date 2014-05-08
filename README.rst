===================================
 NAV Power Stats
===================================

Install
-------

``pip install hg+ssh://hg@bitbucket.org/bredal/nav-contrib-powerstats``

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

- Reload Apache
