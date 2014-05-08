===================================
 NAV Power Stats
===================================

Install
-------

``python setup.py install``

Watch the output to see where the templates go.

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

    # Verify this path with output from setup script
    TEMPLATE_DIRS += ('/usr/local/nav_contrib_templates/navpowerstats', )

- Reload Apache
