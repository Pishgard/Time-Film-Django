from django.contrib import admin
from .models import Post
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali


@admin.register(Post)
class PostAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'updated_at', 'created_at')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%y/%m/%d')
    get_created_jalali.short_description = 'زمان ساخت'