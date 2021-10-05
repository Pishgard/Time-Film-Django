from django.db import models
from django.db.models.fields import TextField
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import pagination
from rest_framework.response import Response

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'در انتظار'),
        ('published', 'منتشر شده'),
    )

    title = models.CharField('عنوان', max_length=250, null=True)
    description = TextField('توضیحات', null=True)
    image = models.ImageField('تصویر', upload_to='blog/%Y/%m/%d', blank=True)

    # price = models.IntegerField('قیمت', null=True,blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, verbose_name="نویسنده")
    view_count = models.IntegerField('تعداد بازدید', default=0)
    
    status = models.CharField('وضعیت', max_length=10, choices=STATUS_CHOICES, default='waiting')
    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Our custom manager

    publish = models.DateTimeField('تاریخ انتشار', default=timezone.now)
    created_at = models.DateTimeField('تاریخ ساخت', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ('-updated_at',)
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return self.title