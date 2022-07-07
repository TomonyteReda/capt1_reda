from django.contrib import admin
from .models import Activity, DataFile


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('log_date', 'quantity_impressions', 'quantity_clicks', 'upload_date', 'user')


admin.site.register(DataFile)
admin.site.register(Activity, ActivityAdmin)

