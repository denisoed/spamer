from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Portal(models.Model):
    name = models.CharField(verbose_name="Portal name", max_length=50)
    user = models.CharField(verbose_name="User", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Portal'
        verbose_name_plural = 'Portals'

    def __str__(self):
        return self.name
