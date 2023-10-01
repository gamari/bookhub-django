from datetime import timedelta, date, timedelta
from typing import List, Dict
from collections import defaultdict

from record.domain.values import Activity


class ActivityCollection:
    """活動履歴の集合体。"""

    def __init__(self, activities: List[Activity]):
        self._activities = activities

    @classmethod
    def from_raw_data(
        cls, raw_data: List[Dict[str, any]], start_date: date, end_date: date
    ) -> "ActivityCollection":
        activity_data_default = cls._generate_default_data(start_date, end_date)
        for data in raw_data:
            activity_data_default[data["date_str"]] = data["count"]

        return cls(
            [
                Activity(date=key, count=value)
                for key, value in activity_data_default.items()
            ]
        )

    @staticmethod
    def _generate_default_data(start_date: date, end_date: date) -> defaultdict:
        date_data_default = defaultdict(int)
        current_day = start_date
        while current_day <= end_date:
            date_data_default[current_day] = 0
            current_day += timedelta(days=1)
        return date_data_default

    def filter_activities(self) -> List[Activity]:
        # activityのカウントが5ずつでレベルを変える

        return self._activities
