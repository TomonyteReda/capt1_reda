from django.contrib import admin
from .models import Activity, DataFile
from django.utils.translation import gettext_lazy as _


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('log_date', 'quantity_impressions', 'quantity_clicks', 'user', 'get_upload_date')
    list_filter = ('log_date', 'user', 'data_file__upload_date')
    fieldsets = (
        ('General', {'fields': ('user', 'log_date')}),
        ('Activities', {'fields': ('quantity_impressions', 'quantity_clicks')}),
    )

    search_fields = ('log_date', 'user__username')

    def get_upload_date(self, obj):
        return obj.data_file.upload_date

    get_upload_date.short_description = _('Upload Date')


class DataFileAdmin(admin.ModelAdmin):
    list_display = ('hash_checksum', 'file_contents', 'user', 'upload_date')
    list_filter = ('user', 'upload_date')

    search_fields = ('upload_date', 'user__username')


admin.site.register(DataFile, DataFileAdmin)
admin.site.register(Activity, ActivityAdmin)

