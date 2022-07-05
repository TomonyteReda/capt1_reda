# Generated by Django 3.2.13 on 2022-07-05 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myreport', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name': 'Activity', 'verbose_name_plural': 'Activities'},
        ),
        migrations.AlterField(
            model_name='activity',
            name='data_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myreport.datafile', verbose_name='file'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='log_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date'),
        ),
    ]
