from django.db import models
from django.contrib.auth import get_user_model


class DataFile(models.Model):
    hash_checksum = models.CharField('hash checksum', max_length=100, null=True, blank=True)
    file_contents = models.FileField('file contents', null=True, blank=True, upload_to="user_files")
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.hash_checksum} {self.user}'


class Activity(models.Model):
    log_date = models.DateField('date', null=True, blank=True)
    activity_type = models.CharField('activity type', max_length=50, null=True, blank=True)
    quantity = models.IntegerField('quantity', default=0)
    upload_date = models.DateField('upload date', auto_now_add=True)
    data_file = models.ForeignKey('DataFile', on_delete=models.CASCADE, null=True, verbose_name='file')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'uploaded on {self.upload_date}: ' \
               f'{self.log_date} {self.activity_type} {self.quantity} by user {self.user}'

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'


