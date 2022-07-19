from functools import partial
import hashlib
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import DataFile, Activity
from .forms import ModelReportFilterForm
from datetime import datetime, date, timedelta
import pandas as pd

upload_date = date.today()
upload_date_str = str(upload_date)


def get_elements_from_file_name(file):
    file_name = str(file)
    file_name_elements = file_name.split('_')
    return file_name_elements


def convert_string_to_date(file_name_elements):
    date_element = file_name_elements[3][:12]
    year = int(date_element[:4])
    month = int(date_element[4:6])
    day = int(date_element[6:8])
    minutes = int(date_element[8:10])
    log_date_values = datetime(year, month, day, minutes)
    log_date = log_date_values.strftime('%Y-%m-%d %H:%M')
    return log_date


def save_activity_count_by_type(file_name_elements, activity, df):
    activity_type = file_name_elements[0]
    if activity_type == 'impressions':
        activity.quantity_impressions = len(df)
    elif activity_type == 'clicks':
        activity.quantity_clicks = len(df)
    else:
        activity.quantity_impressions = 0
        activity.quantity_clicks = 0


def read_file_as_df(file_extension, file_contents):
    if file_extension == 'parquet':
        df = pd.read_parquet(file_contents, engine='pyarrow')
    elif file_extension == 'xlsx':
        df = pd.read_excel(file_contents, engine='openpyxl')
    elif file_extension == 'csv':
        df = pd.read_csv(file_contents)
    return df


def add_data_from_file_to_db(df, file_name, user, instance):
    file_name_elements = get_elements_from_file_name(file_name)
    activity = Activity()
    save_activity_count_by_type(file_name_elements, activity, df)
    activity.log_date = convert_string_to_date(file_name_elements)
    activity.data_file = instance
    activity.user = user
    activity.save()


def process_load_data(request, instance, file_name, file_extension):
    df = read_file_as_df(file_extension=file_extension, file_contents=instance.file_contents)
    add_data_from_file_to_db(df=df, file_name=file_name, user=instance.user,
                             instance=instance)
    messages.success(request, _('File {} uploaded successfully!').format(str(file_name)))


def hash_file(file, block_size=65536):
    hasher = hashlib.md5()
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)
    return hasher.hexdigest()


def check_for_upload_form_error(request, instance, file_name, file_extension):
    if file_extension not in ['parquet', 'csv', 'xlsx']:
        messages.error(request, _('Incorrect file format. Only *.parquet, *.csv, *.xlsx formats are supported')
                       .format(str(file_name)))
        status = 'error'
    elif DataFile.objects.filter(user=instance.user, hash_checksum=instance.hash_checksum).count() >= 1:
        messages.error(request, _('File {} is already uploaded').format(str(file_name)))
        status = 'error'
    else:
        status = 'correct'
    return status


def get_report_queryset(request):
    queryset = Activity.objects.filter(user=request.user)
    if request.method == 'GET':
        form = ModelReportFilterForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            if data['from_']:
                queryset = queryset.filter(
                    log_date__gte=data['from_'])
            if data['to']:
                queryset = queryset.filter(
                    log_date__lte=data['to'] + timedelta(days=1))
            if data['uploaded']:
                queryset = queryset.filter(
                    data_file__upload_date=data['uploaded'])
    else:
        form = ModelReportFilterForm()
    return form, queryset


