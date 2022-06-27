from django.db import models
from django.contrib.auth import get_user_model


class DataFile(models.Model):
    hash_checksum = models.CharField('hash checksum', max_length=100, null=True, blank=True)
    file_contents = models.FileField('file contents', null=True, blank=True, upload_to="user_files")
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)


class Activity(models.Model):
    log_date = models.DateField('date', null=True, blank=True)
    activity_type = models.CharField('activity type', max_length=50, null=True, blank=True)
    quantity = models.IntegerField('quantity', default=0)
    upload_date = models.DateField('upload date', auto_now_add=True)
    data_file = models.ForeignKey('DataFile', on_delete=models.SET_NULL, null=True, verbose_name='file')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)


