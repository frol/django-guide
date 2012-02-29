django-guide
===========

**Django guide** is Django module which is a simple wrapper around jQuery-guide module.
Django guide improve users ability individually disable guides (all visible guides
or one guide at a time).

.. contents::

Requirements
==============

- python >= 2.6 (not tested at early versions)
- pip >= 0.8 (just for installation, not tested at early versions)
- django >= 1.2 (not tested at early versions)
- jquery-guide (more details at https://github.com/frol/jquery-guide )

Installation
============

**Django guide** might be installed using pip: ::

    pip install git+git://github.com/frol/django-guide.git


Setup
=====

- Add 'misc' to INSTALLED_APPS ::

    INSTALLED_APPS += ( 'guide', )

- Setup jQuery-guide

Settings
========

In settings.py you can change following settings:

 * GUIDE_IMAGES_URL - jQuery-guide specific setting, by default is `settings.STATIC_URL + 'img/guide/'`
 * GUIDE_ARROW_IMAGE_NAME - jQuery-guide specific setting, by default is `'arrow'`
 * GUIDE_HIGHLIGHT_IMAGE_NAME - jQuery-guide specific setting, by default is `'circle'`
 * GUIDE_MIN_VIEWS_COUNT - minimum count of views guide by one user, by default is `3`
 * GUIDE_SHOW_ONLY_REGISTERED_GUIDES - if `True` than you must register needed guides in
 templates by using `add_guide` templatetag, by default is `False`.

Usage
=====

Templatetags
------------

::

    {% load guide_tags %}

    {% add_guide 'login' 'logout' ... %} {# this need for all guides you want show if GUIDE_SHOW_ONLY is True #}

    <script>
        {% render_guides %} {# generating jQuery-guide JS code #}
    </script>


Contributing
============

Development of django-guide happens at github: https://github.com/frol/django-guide

This module used in production at https://escalibro.com

License
============

Copyright (C) 2011-2012 Vladyslav Frolov & Ilya Polosukhin
This program is licensed under the MIT License (see LICENSE) 
