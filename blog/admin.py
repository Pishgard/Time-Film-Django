from django.contrib import admin
from .models import Post
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali


@admin.register(Post)
class PostAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title', 'author', 'get_publish_jalali', 'status']
    list_filter = ['status', 'created_at', 'publish', 'author']
    search_fields = ['status', 'author__username', 'title']
    # prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    # autocomplete_fields = ['category']
    # filter_horizontal = ['tags']

    list_editable = ['status']
    readonly_fields = ['view_count']

    def get_publish_jalali(self, obj):
    	return datetime2jalali(obj.publish).strftime('%Y/%m/%d - %H:%M:%S')
    get_publish_jalali.short_description = 'تاریخ انتشار'
    get_publish_jalali.admin_order_field = 'publish'