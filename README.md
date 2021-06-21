## Django REST URL Token Authentication

Simple extension for Django REST Framework to allow for simple url token authentication. Adds
an authentication option for passing a token key as an url parameter: `?token=sometoken` and
allows for managing tokens through the admin (similar to Tastypie).

This could be useful for example when needing to share some data through a simple API with an 
external group where you don't want to make a user account for the group on your application.

By default, the token only gives READ ONLY permission to requests, but this can be adjusted to
allow url token authentication for all requests.

### Installation


1. Add "django_rest_urltoken_auth" to your INSTALLED_APPS setting like this::
	
	```
    INSTALLED_APPS = [
        ...
        'django_rest_urltoken_auth',
    ]
    ```

2. Run ``python manage.py migrate`` to create the apps models.

### Quick start

- Create URL API tokens in the admin: `/admin/django_rest_urltoken_auth/urltokens/`

- Set permission of the DRF view/viewset to IsURLTokenAuthenticated

```
from django_rest_urltoken_auth.permissions import IsURLTokenAuthenticated

...
# viewsets.py

class ExampleViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsURLTokenAuthenticated,)
    queryset = Example.objects.all()
```

This view can now be accessed by adding `?token=<url_token>` to the request url.

### Optional configuration

- By default the url parameter used for the authentication token is `token`. This can be 
adapted by overriding the setting `DRF_URLTOKEN_PARAM`. For example:

```
# settings.py

DRF_URLTOKEN_PARAM = "secret"
```

would lead to authentication the API using `?secret=<url_token>` as url parameter.

- If you want to allow url token authentication on all requests methods 
(not just read only methods `GET`, `HEAD`, `OPTIONS`), then add to your settings:
`DRF_URLTOKEN_READ_ONLY=False`


### Running tests

For running the tests using pytest:

```
pip install pytest
```
 
```
pytest --pyargs django_rest_urltoken_auth.tests
```


