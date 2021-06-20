=====
Django REST URLToken Authentication
=====

A Django REST app to extend the Django REST Framework with 
simple url parameter token authentication.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "django_rest_urltoken_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_rest_urltoken_auth',
    ]

2. Run ``python manage.py migrate`` to create the token models.
