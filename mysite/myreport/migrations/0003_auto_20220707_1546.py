# Generated by Django 3.2.13 on 2022-07-07 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myreport', '0002_auto_20220705_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='activity_type',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='quantity',
        ),
        migrations.AddField(
            model_name='activity',
            name='quantity_clicks',
            field=models.IntegerField(default=0, verbose_name='clicks'),
        ),
        migrations.AddField(
            model_name='activity',
            name='quantity_impressions',
            field=models.IntegerField(default=0, verbose_name='impressions'),
        ),
    ]
