import datetime
import random
import time


TIME_FORMAT_DEFAULT = '%Y-%m-%d %H:%M:%S.%f'
TIME_FORMAT_SECOND = '%Y-%m-%d %H:%M:%S'
TIME_FORMAT_FOR_FILE = '%Y_%m_%d__%H_%M_%S_%f'
TIME_FORMAT_UNIQUE = '%Y_%m_%d__%H_%M_%S_%f'


def get_time_str_now(time_format):
    date_time_obj = datetime.datetime.now()
    return convert_time_obj_to_time_str(date_time_obj, time_format)


def get_time_str_unique(time_str=None, time_obj=None, time_format=None):
    if time_obj:
        time_str = convert_time_obj_to_time_str(time_obj, time_format)
    time_str = time_str or get_time_str_now(TIME_FORMAT_UNIQUE)
    return '%s__%.8d' % (time_str, random.randrange(0, 99999999))


def get_time_str_now_for_file():
    return get_time_str_now(TIME_FORMAT_FOR_FILE)


def convert_time_obj_to_time_str(date_time_obj=None, time_format=TIME_FORMAT_DEFAULT):
    date_time_obj = date_time_obj or datetime.datetime.now()
    return date_time_obj.strftime(time_format)


def convert_time_str_to_time_obj(date_time_str, time_format=TIME_FORMAT_DEFAULT):
    try:
        return datetime.datetime.strptime(date_time_str, time_format)
    except:
        return None


def convert_time_zone(time_obj, tz_to, tz_from=None):
    tz_from = tz_from or time_obj.tzinfo
    if tz_from:
        time_obj = time_obj.replace(tzinfo=tz_from)
    else:
        if not time_obj.tzinfo:
            raise ValueError('tz_from is none.')
    time_obj = time_obj.astimezone(tz_to)
    return time_obj


def convert_time_zone_with_time_str(time_str, tz_to, tz_from=None, format_from=TIME_FORMAT_DEFAULT, format_to=None):
    format_to = format_to or format_from
    time_obj = datetime.datetime.strptime(time_str, format_from)
    tz_from = tz_from or time_obj.tzinfo
    if tz_from:
        time_obj = time_obj.replace(tzinfo=tz_from)
    else:
        if not time_obj.tzinfo:
            raise ValueError('tz_from is none.')
    time_obj = time_obj.astimezone(tz_to)
    time_str = time_obj.strftime(format_to)
    return time_str


def convert_time_str_format(time_str_src, t_format_src, t_format_dst):
    time_obj = datetime.datetime.strptime(time_str_src, t_format_src)
    return time_obj.strftime(t_format_dst)


def convert_time_str_to_stamp_ms(time_str, time_format=TIME_FORMAT_DEFAULT):
    try:
        dt = datetime.datetime.strptime(time_str, time_format)
    except:
        dt = datetime.datetime.strptime(time_str, TIME_FORMAT_SECOND)
    stamp = time.mktime(dt.timetuple())
    return int(stamp * 1000)


def convert_stamp_ms_to_time_str(timestamp, time_format=TIME_FORMAT_DEFAULT):
    stamp = float(timestamp) / 1000.0
    dt = datetime.datetime.fromtimestamp(stamp)
    return dt.strftime(time_format)


def convert_time_obj_to_timestamp(time_obj):
    return time.mktime(time_obj.timetuple()) + (time_obj.microsecond / 1000000.0)


def convert_timestamp_to_time_obj(stamp):
    dt = datetime.datetime.fromtimestamp(float(stamp))
    return dt


def datetime_sub_seconds(time_obj_a, time_obj_b):
    delta = time_obj_a - time_obj_b
    seconds = delta.days * 3600 * 24 + delta.seconds
    return seconds


if __name__ == "__main__":
    stamp = convert_time_str_to_stamp_ms("2016-08-10 10:32:56")
    print stamp
