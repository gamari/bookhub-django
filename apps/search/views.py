from django.shortcuts import render

from apps.book.domain.repositories import BookRepository, BookshelfRepository
from apps.book.domain.services import BookDomainService
from apps.search.application.usecases import BookSearchByTitleUsecase
from apps.search.domain.services import BookSearchService, GoogleBooksService
from apps.search.infrastracture.external.apis import GoogleBooksAPIClient


def book_search(request):
    """書籍検索"""
    query = request.GET.get("query")
    mode = request.GET.get("mode", "")
    page = int(request.GET.get("page", 1))

    # TODO 検証のため
    # mode = "detail"

    if mode == "detail":
        search_service = GoogleBooksService(
            GoogleBooksAPIClient(),
            BookDomainService(BookRepository(), BookshelfRepository()),
        )
    else:
        search_service = BookSearchService()

    usecase = BookSearchByTitleUsecase(search_service)
    context = usecase.execute(mode, page, query)

    return render(request, "pages/search_results.html", context)
