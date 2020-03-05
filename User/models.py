from django.db import models
import django.utils.timezone as timezone
# Create your models here.
class User(models.Model):
    username = models.CharField(unique=True, max_length=20, null=False)
    password = models.CharField(max_length=20, null=False)
    phonenumber = models.CharField(unique=True, max_length=20, null=False)
    issuper = models.BooleanField(default=False)
    addresses = models.CharField(max_length=1024,default='{"address":[]}')
    credit = models.IntegerField(default=0)
    enrolldatetime = models.DateTimeField(default=timezone.now)
    # Bottle的一对一从
    # Order的一对一从
    isdeleted = models.BooleanField(default=False)
    star = models.ManyToManyField("Bottle.Bottle")