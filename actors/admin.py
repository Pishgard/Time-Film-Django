from django.contrib import admin
from .models import Actors
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali


@admin.register(Actors)
class ActorsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['name', 'get_publish_jalali', 'age']
    list_filter = ['created_at', 'age']
    search_fields = ['name']
    date_hierarchy = 'publish'

    readonly_fields = ['view_count']

    def get_publish_jalali(self, obj):
    	return datetime2jalali(obj.publish).strftime('%Y/%m/%d - %H:%M:%S')
    get_publish_jalali.short_description = 'تاریخ انتشار'
    get_publish_jalali.admin_order_field = 'publish'