from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


class URLToken(models.Model):

    name = models.CharField(
        max_length=255, help_text="Name for identifying token"
    )
    token = models.CharField(max_length=128, blank=True, default="")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "URL Token"
        verbose_name_plural = "URL Tokens"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()

        return super(URLToken, self).save(*args, **kwargs)

    def generate_token(self):
        # Generate string with length 64
        token = get_random_string(64)

        # Force uniqueness
        while URLToken.objects.filter(token=token).exists():
            token = get_random_string(64)

        return token