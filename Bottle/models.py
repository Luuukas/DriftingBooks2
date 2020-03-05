from django.db import models
import django.utils.timezone as timezone
# Create your models here.
class Bottle(models.Model):
    related_book = models.ForeignKey("Book.Book", on_delete=models.PROTECT)
    related_user = models.ForeignKey("User.User", on_delete=models.PROTECT)
    # Order的从
    article = models.CharField(max_length=128)
    photos = models.CharField(max_length=128)
    timeouthandle = models.BooleanField(default=True)
    book_sendto = models.IntegerField(default=0)  # 赠送对象，0：未给个人，<0：已确定机构代号, >0:已给个人uid
    upload_datetime = models.DateTimeField(default=timezone.now)
    book_state = models.IntegerField(default=0) # 供个人查看的状态, 1：未入库 2：已入库 3：已拒收 4：已捐赠