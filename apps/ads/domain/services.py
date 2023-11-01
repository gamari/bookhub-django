from apps.ads.domain.repository import RecommendRepository


class RecommendDomainService(object):
    def __init__(self, recommend_repo):
        self.recommend_repo = recommend_repo
    
    @classmethod
    def initialize(cls):
        recommend_repo = RecommendRepository.initialize()
        return cls(recommend_repo)

    def get_recommend_three_books(self):
        return self.recommend_repo.get_recommend_books(3)