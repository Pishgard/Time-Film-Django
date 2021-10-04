from django.db import models
from django.db.models.fields import TextField
from accounts.models import User


class UserProfile(models.Model):

    GENDER_CHOICES = (
        ('male', 'مرد'),
        ('female', 'زن')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField('جنسیت', max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    bio = TextField('توضیحات', blank=True, null=True)
    image_profile = models.ImageField('تصویر پروفایل', upload_to='users/%Y/%m/%d', default='default.jpg', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'