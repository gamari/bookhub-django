from config.application.usecases import Usecase


class BookSearchByTitleUsecase(Usecase):
    """書籍名で検索を行う。"""

    def __init__(self, search_service):
        self.search_service = search_service

    def run(self, mode, page, query):
        results_list, total_pages = self.search_service.search(query, page)

        context = {
            "results": results_list,
            "query": query,
            "current_page": page,
            "total_pages": total_pages,
            "mode": mode,
        }

        return context
