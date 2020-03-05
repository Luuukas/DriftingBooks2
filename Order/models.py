from django.db import models
import django.utils.timezone as timezone
import time
# Create your models here.

# 生成订单号
def get_order_code_with_type(type):
    def get_order_code():
        order_no = str(type) + str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]
        return order_no
    return get_order_code

def get_order_code_RECE():
        order_no = "RECE" + str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]
        return order_no

def get_order_code_RETR():
        order_no = "RETR" + str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]
        return order_no

def get_order_code_ACQU():
        order_no = "ACQU" + str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]
        return order_no

class Order(models.Model):
    # 声明抽象基类
    class Meta:
        abstract = True
    expresscompany = models.IntegerField(default=-1)
    trackingnumber = models.CharField(max_length=64, default="")
    order_state = models.IntegerField(default=0)
    submittime = models.DateTimeField(default=timezone.now)
    dealtime = models.DateTimeField(null=True, blank=True)
    related_bottle = models.OneToOneField("Bottle.Bottle", on_delete=models.PROTECT)
    related_user = models.ForeignKey("User.User", on_delete=models.PROTECT)

class receiveOrder(Order):
    transactioncode = models.CharField(max_length=32, default=get_order_code_RECE)
    from_address = models.CharField(max_length=256)
    from_name = models.CharField(max_length=64)
    from_phonenumber = models.CharField(max_length=16)

class retriveOrder(Order):
    transactioncode = models.CharField(max_length=32, default=get_order_code_RETR)
    to_address = models.CharField(max_length=256)
    to_name = models.CharField(max_length=64)
    to_phonenumber = models.CharField(max_length=16)

class acquireOrder(Order):
    transactioncode = models.CharField(max_length=32, default=get_order_code_ACQU)
    to_address = models.CharField(max_length=256)
    to_name = models.CharField(max_length=64)
    to_phonenumber = models.CharField(max_length=16)