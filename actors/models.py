from django.db import models
from django.db.models.fields import TextField
from django.utils import timezone

class Actors(models.Model):

    name = models.CharField('نام بازیگر', max_length=250, null=True)
    image = models.ImageField('تصویر', upload_to='actors/%Y/%m/%d', blank=True)
    age = models.IntegerField('سن')

    description = TextField('توضیحات', null=True, blank=True)
    
    view_count = models.IntegerField('تعداد بازدید', default=0)
    publish = models.DateTimeField('تاریخ انتشار', default=timezone.now)
    created_at = models.DateTimeField('تاریخ ساخت', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ('-updated_at',)
        verbose_name = 'بازیگر'
        verbose_name_plural = 'بازیگران'

    def __str__(self):
        return self.name