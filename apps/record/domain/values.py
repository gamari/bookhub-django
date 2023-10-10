from datetime import date
import math


class Activity:
    def __init__(self, date: date, count: int):
        self._date = date
        self._count = count

    @property
    def date(self) -> date:
        return self._date

    @property
    def count(self) -> int:
        return self._count

    @property
    def level(self) -> int:
        return max(0, min(5, math.ceil(self._count / 5)))
