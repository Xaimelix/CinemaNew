import datetime


def to_date_datetime_format(date: str) -> datetime.datetime:
    res = datetime.datetime.strptime(date, '%Y-%m-%d')
    return res


def is_date1_lower_date2(date1: datetime.datetime, date2: datetime.datetime) -> bool:
    if date1 < date2 and date1 != datetime.datetime.today():
        return True
    else:
        return False

