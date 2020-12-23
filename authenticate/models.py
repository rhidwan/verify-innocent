from django.db import models

# Create your models here.
class Authentication(models.Model):
    unique_str = models.CharField(max_length=60, unique=True, null=False)
    authenticated = models.BooleanField(default=False)
    validated_at = models.DateTimeField(null=True, blank=True)
    inserted_at = models.DateTimeField(auto_now_add=True)
    hit_count = models.IntegerField(default=0)
    ip_address = models.GenericIPAddressField(null=True)

    def __str__(self):
        return self.unique_str

class BlacklistIP(models.Model):
    ip_address = models.GenericIPAddressField(null=False)
    hit_count = models.IntegerField(default=1)
    blocked = models.BooleanField(default=0)

    def __str__(self):
        return self.ip_address