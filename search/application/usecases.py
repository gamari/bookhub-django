from config.application.usecases import Usecase


class BookSearchByTitleUsecase(Usecase):
    """書籍名で検索を行う。"""

    def __init__(self, mode, page, query, search_service) -> None:
        self.mode = mode
        self.page = page
        self.query = query
        self.search_service = search_service

    def run(self):
        results_list, total_pages = self.search_service.search(self.query, self.page)

        context = {
            "results": results_list,
            "query": self.query,
            "current_page": self.page,
            "total_pages": total_pages,
            "mode": self.mode,
        }

        return context
