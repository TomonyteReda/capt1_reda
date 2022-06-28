from django.contrib import admin
from .models import Activity, DataFile


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('log_date', 'activity_type', 'quantity', 'upload_date', 'user')


admin.site.register(DataFile)
admin.site.register(Activity, ActivityAdmin)

