from django.contrib import admin
from .models import UserProfile
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali


@admin.register(UserProfile)
class ProfileAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'gender')