from datetime import timedelta, datetime


# 日付系
def get_month_date_range(target):
    start_date = target.replace(day=1)
    end_date = target.replace(month=target.month % 12 + 1, day=1) - timedelta(days=1)
    return start_date, end_date

def get_month_range_of_today():
    first_day_of_month = datetime.now().replace(day=1)
    last_day_of_month = first_day_of_month.replace(
        month=first_day_of_month.month % 12 + 1, day=1
    ) - timedelta(days=1)
    return first_day_of_month, last_day_of_month