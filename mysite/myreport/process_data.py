from datetime import datetime, date
import pandas as pd
from .models import Activity


upload_date = date.today()
upload_date_str = str(upload_date)


def get_elements_from_file_name(file):
    file_name = str(file)
    file_name_elements = file_name.split('_')
    return file_name_elements


def convert_string_to_date(date_element):
    year = int(date_element[:4])
    month = int(date_element[4:6])
    day = int(date_element[6:8])
    minutes = int(date_element[8:10])
    seconds = int(date_element[-2:])
    log_date_values = datetime(year, month, day, minutes, seconds)
    return log_date_values


def get_date_time_value(file_name_elements):
    date_element = file_name_elements[3][:12]
    log_date = convert_string_to_date(date_element)
    return log_date


def get_activity_type_from_file_name(file_name_elements):
    activity_type = file_name_elements[0]
    return activity_type


def add_data_instance_to_dict(data, df, log_date, activity_type):
    data['log_date'] = log_date.strftime('%Y-%m-%d')
    data['activity_type'] = activity_type
    data['quantity'] = len(df)
    return data


def put_data_from_raw_files_to_dict(file_contents, file_name):
    data = {}
    df = pd.read_parquet(file_contents, engine='pyarrow')
    file_name_elements = get_elements_from_file_name(file_name)
    log_date = get_date_time_value(file_name_elements)
    activity_type = get_activity_type_from_file_name(file_name_elements)
    data = add_data_instance_to_dict(data, df, log_date, activity_type)
    return data


def add_data_from_file_to_db(file_contents, file_name, user, instance):
    data = put_data_from_raw_files_to_dict(file_contents, file_name)
    activity = Activity()
    activity.log_date = data['log_date']
    activity.quantity = data['quantity']
    activity.data_file = instance
    activity.user = user
    activity.save()


