from django.db import models


class Portal(models.Model):
    name = models.CharField(verbose_name="Portal name", max_length=50)
    user = models.CharField(verbose_name="User", max_length=50, blank=True)
    login = models.CharField(verbose_name="login", max_length=50)
    password = models.CharField(verbose_name="password", max_length=50)

    class Meta:
        verbose_name = 'Portal'
        verbose_name_plural = 'Portals'

    def __str__(self):
        return self.name
