from django.db import models
from django.db.models.fields import TextField
from django.utils import timezone
from actors.models import Actors

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Movie(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'در انتظار'),
        ('published', 'منتشر شده'),
    )

    title = models.CharField('نام فیلم', max_length=250, null=True)
    image = models.ImageField('تصویر', upload_to='movie/%Y/%m/%d', blank=True)
    rate = models.FloatField('امتیاز فیلم', default=0.0)
    genre = models.CharField('ژانر فیلم', max_length=250, null=True)
    time = models.IntegerField('زمان فیلم (دقیقه)')
    year_make = models.IntegerField('سال ساخت')

    description = TextField('خلاصه قیلم', null=True)
    
    actors = models.ManyToManyField(Actors,blank=True, related_name= 'actors', verbose_name='بازیگران')

    view_count = models.IntegerField('تعداد بازدید', default=0)
    status = models.CharField('وضعیت', max_length=10, choices=STATUS_CHOICES, default='waiting')
    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Our custom manager

    publish = models.DateTimeField('تاریخ انتشار', default=timezone.now)
    created_at = models.DateTimeField('تاریخ ساخت', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        ordering = ('-updated_at',)
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم ها'

    def __str__(self):
        return self.title