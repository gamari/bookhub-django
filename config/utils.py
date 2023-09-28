from datetime import timedelta


# 日付系
def get_month_date_range(today):
    start_date = today.replace(day=1)
    end_date = today.replace(month=today.month % 12 + 1, day=1) - timedelta(days=1)
    return start_date, end_date