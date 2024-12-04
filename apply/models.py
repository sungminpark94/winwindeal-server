from django.db import models

# Create your models here.
class Reservations(models.Model):
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    visitdate = models.IntegerField(null=False, blank=False, default=0)
    visitlocation = models.IntegerField(null=False, blank=False, default=0)