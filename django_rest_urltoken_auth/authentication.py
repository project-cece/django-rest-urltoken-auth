from django.contrib.auth.models import User
from django_rest_urltoken_auth.models import URLToken
from rest_framework import authentication
from rest_framework import exceptions

class URLTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
       
        if not "token" in request.GET:
        	return None

        token = request.GET["token"]

        # Return immediately if empty string
        if not token:
            return None

        try:
            valid_token = URLToken.objects.get(token=token)
        except URLToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        # Check if token is currently active or disabled
        if not valid_token.active:
        	raise exceptions.AuthenticationFailed('Inactive token')

        return (valid_token, None)