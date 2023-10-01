from collections import defaultdict
from datetime import date, timedelta, datetime


class DateUtils(object):
    @staticmethod
    def head_of_calendar(first_date: date) -> date:
        """1日からカレンダーの先頭を計算する。"""
        days_until_sunday = first_date.weekday()
        return first_date - timedelta(days=days_until_sunday)

    @staticmethod
    def end_of_calendar(last_date: date) -> date:
        """最終日からカレンダーの末尾を計算する"""
        days_from_last_saturday = 6 - last_date.weekday()
        return last_date + timedelta(days=days_from_last_saturday)

    @staticmethod
    def generate_default_date_data(start_date: date, end_date: date) -> defaultdict:
        date_data_default = defaultdict(int)
        current_day = start_date
        while current_day <= end_date:
            date_data_default[current_day] = 0
            current_day += timedelta(days=1)
        return date_data_default


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
