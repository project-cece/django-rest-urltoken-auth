from django.test import TestCase
from django.db import models
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.urls import include, path
from rest_framework.test import APIRequestFactory
from rest_framework import routers
from rest_framework import serializers
from rest_framework.test import APITestCase
from rest_framework.response import Response
from rest_framework import (
    HTTP_HEADER_ENCODING, authentication, generics, permissions, serializers,
    status, views
)
from rest_framework.routers import DefaultRouter

from django_rest_urltoken_auth.models import URLToken
from django_rest_urltoken_auth.permissions import IsURLTokenAuthenticated, IsURLTokenAuthenticatedOrAdmin

factory = APIRequestFactory()

# Objects to be used instead of model objects in tests
class TestObject(object):
    def __init__(self, **kwargs):
        for field in ('name', 'favorite_cake'):
            setattr(self, field, kwargs.get(field, None))

objects = {
    1: TestObject(name='Moya', favorite_cake='Apple Pie'),
    2: TestObject(name='Michelle', favorite_cake='Sticky Toffee'),
    3: TestObject(name='Mara', favorite_cake='Cinnamon Cake'),
}

class TestObjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    favorite_cake = serializers.CharField(max_length=100)

class TestObjectViewSet(viewsets.ViewSet):
    serializer_class = TestObjectSerializer
    basename = "testobject"
    permission_classes = (IsURLTokenAuthenticated,)

    def list(self, request):
        serializer = TestObjectSerializer(
            instance=objects.values(), many=True)
        return Response(serializer.data)

root_view = TestObjectViewSet.as_view({'get': 'list'})

# Tests
class URLTokenAuthTests(APITestCase):

    def setUp(self):
        super().setUp()  # in case of inheritance

        # self.normal_user = User.objects.create_user("somebody", "somebody@mail.com", "somesecret")
        # self.admin_user = User.objects.create_user("admin", "admin@mail.com", "adminsecret")
        self.valid_token = URLToken(name="Testtoken")
        self.valid_token.save()
        self.inactive_token = URLToken(name="Testtoken", active=False)
        self.inactive_token.save()

    def test_unauthicated_get_request(self):

        request = factory.get('/?token={0}'.format(self.valid_token.token), format='json')
        response = root_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(False)

    def test_authicated_get_request(self):

        request = factory.get('/?token={0}'.format(self.invalid_token.token), format='json')
        response = root_view(request)

        self.assertEqual(response.status_code, 401)
        self.assertTrue(False)