from apps.ranking.models import WeeklyRanking, WeeklyRankingEntry


class RankingDomainService(object):
    """ランキングに関するドメインサービス"""

    @classmethod
    def initialize(cls):
        return cls()

    def get_latest_ranking_entries(self):
        try:
            latest_ranking = WeeklyRanking.objects.latest("end_date")
            if latest_ranking is None:
                return None
            return WeeklyRankingEntry.objects.filter(
                ranking=latest_ranking
            ).order_by("-added_count")
        except:
            return None