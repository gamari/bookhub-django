from apps.ads.models import RecommendBook


class RecommendRepository(object):
    @classmethod
    def initialize(cls):
        return cls()
    
    @classmethod
    def get_recommend_books(cls, limit=5):
        return RecommendBook.objects.all()[:limit]
    