from django.contrib.auth.models import User
from django_rest_urltoken_auth.models import URLToken
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import permissions


READONLY_METHODS = ["GET", "OPTIONS", "HEAD"]

class IsURLTokenAuthenticated(permissions.BasePermission):
    """
    Allows access only for valid URLTokens given in token 
    url parameter
    """

    def has_permission(self, request, view):
      
        if not "token" in request.GET:
            return False

        token = self.get_token_parameter(request)

        # Return immediately if empty string
        if not token:
            return False

        # Return if request method isn't allowed when using
        # URL token authentication
        if not self.is_method_allowed(request):
            return

        try:
            valid_token = URLToken.objects.get(token=token)
        except URLToken.DoesNotExist:
            return False

        # Check if token is currently active or disabled
        if not valid_token.active:
            raise exceptions.AuthenticationFailed('Token not active')

        return True

    def is_method_allowed(self, request):
        if getattr(settings, 'DRF_URLTOKEN_READ_ONLY', True):
            if request.method in READONLY_METHODS:
                return True

            return False
        return True

    def get_token_parameter(self, request):
        param = getattr(settings, 'DRF_URLTOKEN_PARAM', "token")
        return request.GET[param]


class IsURLTokenAuthenticatedOrAdmin(IsURLTokenAuthenticated):
    """
    Allows access only for valid URLTokens given in token 
    url parameter and logged in admin users
    """

    def has_permission(self, request, view):
        
        # Check if admin user
        if request.user and request.user.is_staff:
            return True

        # Check if authenticated with URL Token
        return super(IsURLTokenAuthenticated, self).has_permission(request, view)