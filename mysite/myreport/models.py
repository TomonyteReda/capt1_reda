from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class DataFile(models.Model):
    hash_checksum = models.CharField('hash checksum', max_length=100, null=True, blank=True)
    file_contents = models.FileField('file contents', null=True, blank=True, upload_to="user_files")
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    upload_date = models.DateField('upload date', auto_now_add=True)

    def __str__(self):
        return f'{self.hash_checksum} {self.user} {self.upload_date}'


class Activity(models.Model):
    log_date = models.DateTimeField('date', null=True, blank=True)
    quantity_impressions = models.IntegerField('impressions', default=0)
    quantity_clicks = models.IntegerField('clicks', default=0)
    data_file = models.ForeignKey('DataFile', on_delete=models.CASCADE, null=True, related_name='activity')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'uploaded on {self.upload_date}: ' \
               f'{self.log_date} {self.quantity_impressions} {self.quantity_clicks} by user {self.user}'

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')



