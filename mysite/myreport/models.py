from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class DataFile(models.Model):
    hash_checksum = models.CharField(_('hash checksum'), max_length=100, null=True, blank=True)
    file_contents = models.FileField(_('file contents'), null=True, blank=True, upload_to="user_files")
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('user'))
    upload_date = models.DateField(_('upload date'), auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.upload_date}'

    class Meta:
        verbose_name = _('Data File')
        verbose_name_plural = _('Data Files')


class Activity(models.Model):
    log_date = models.DateTimeField(_('date'), null=True, blank=True)
    quantity_impressions = models.IntegerField(_('impressions'), default=0)
    quantity_clicks = models.IntegerField(_('clicks'), default=0)
    data_file = models.ForeignKey('DataFile', on_delete=models.CASCADE, null=True, related_name='activity')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('user'))

    def __str__(self):
        return f'Log Date: {self.log_date} ' \
               f'Impressions:{self.quantity_impressions} ' \
               f'Clicks: {self.quantity_clicks} ' \
               f'Uploaded by user {self.user} '

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')



