from apps.search.models import SearchHistory
from config.application.usecases import Usecase


class BookSearchByTitleUsecase(Usecase):
    """書籍名で検索を行う。"""

    def __init__(self, search_service):
        self.search_service = search_service
    
    def run(self, mode, page, query):
        if len(query) > 50:
            raise ValueError("検索文字列が長すぎます")

        results_list, total_pages = self.search_service.search(query, page)

        # TODO サービス層に移動する
        SearchHistory.objects.create(query=query)

        context = {
            "results": results_list,
            "query": query,
            "current_page": page,
            "total_pages": total_pages,
            "mode": mode,
        }

        return context
