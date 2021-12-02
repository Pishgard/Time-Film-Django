from django.contrib import admin
from .models import Actors
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali


@admin.register(Actors)
class ActorsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['name', 'get_publish_jalali']
    list_filter = ['created_at',]
    search_fields = ['name']
    # prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    # autocomplete_fields = ['category']
    # filter_horizontal = ['tags']

    # list_editable = ['status']
    readonly_fields = ['view_count']

    def get_publish_jalali(self, obj):
    	return datetime2jalali(obj.publish).strftime('%Y/%m/%d - %H:%M:%S')
    get_publish_jalali.short_description = 'تاریخ انتشار'
    get_publish_jalali.admin_order_field = 'publish'