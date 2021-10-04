from django.contrib import admin
from .models import User
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali


@admin.register(User)
class Admin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%y/%m/%d')
    get_created_jalali.short_description = 'تاریخ عضویت'