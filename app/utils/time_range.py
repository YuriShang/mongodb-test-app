import calendar
from datetime import timedelta, datetime


def time_range(date, dt_upto, group_type, by_group_type_range):
    by_group_type_range.append(datetime.isoformat(date))

    if group_type == "month":
        days = calendar.monthrange(date.year, date.month)[1]
        date += timedelta(days=days)

    elif group_type == "day":
        date += timedelta(days=1)

    elif group_type == "hour":
        date += timedelta(hours=1)

    if date <= dt_upto:
        time_range(date, dt_upto, group_type, by_group_type_range)

    return by_group_type_range

