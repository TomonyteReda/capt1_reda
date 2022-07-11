from datetime import datetime, date
import pandas as pd
from .models import Activity


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


def read_file_as_df(file_name_elements, file_contents):
    file_extension = file_name_elements[-1].split('.')[-1]
    if file_extension == 'parquet':
        df = pd.read_parquet(file_contents, engine='pyarrow')
    elif file_extension == 'xlsx':
        df = pd.read_excel(file_contents, engine='openpyxl')
    elif file_extension == 'csv':
        df = pd.read_csv(file_contents)
    return df


def add_data_from_file_to_db(file_contents, file_name, user, instance):
    file_name_elements = get_elements_from_file_name(file_name)
    df = read_file_as_df(file_name_elements, file_contents)
    activity = Activity()
    save_activity_count_by_type(file_name_elements, activity, df)
    activity.log_date = convert_string_to_date(file_name_elements)
    activity.data_file = instance
    activity.user = user
    activity.save()


