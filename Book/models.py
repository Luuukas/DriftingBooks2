from django.db import models

# Create your models here.

class Book(models.Model):
    isbn = models.CharField(unique=True, max_length=16, null=False)
    bookname = models.CharField(max_length=64, null=True, blank=True)
    origin_bookname = models.CharField(max_length=64, null=True, blank=True)
    writer = models.CharField(max_length=64, null=True, blank=True)
    translator = models.CharField(max_length=64, null=True, blank=True)
    pagenum = models.CharField(max_length=8, null=True, blank=True)
    publishtime = models.CharField(max_length=64, null=True, blank=True)
    price = models.CharField(max_length=64, null=True, blank=True)
    content_intro = models.CharField(max_length=512, null=True)
    writer_intro = models.CharField(max_length=512, null=True)
    neededcredit = models.IntegerField(default=-1)
    coverurl = models.CharField(max_length=64, null=True)
    press = models.CharField(max_length=64, null=True)
