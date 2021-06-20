from django.contrib import admin

from django_rest_urltoken_auth.models import URLToken

@admin.register(URLToken)
class URLTokenAdmin(admin.ModelAdmin):
	list_display = ("name", "token", "active", "created")
	list_filter = ("active",)


