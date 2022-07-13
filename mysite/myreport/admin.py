from django.contrib import admin
from .models import Activity, DataFile


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('log_date', 'quantity_impressions', 'quantity_clicks', 'user')


class DataFileAdmin(admin.ModelAdmin):
    list_display = ('hash_checksum', 'file_contents', 'user', 'upload_date')


admin.site.register(DataFile, DataFileAdmin)
admin.site.register(Activity, ActivityAdmin)

