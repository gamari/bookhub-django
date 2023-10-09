from django.shortcuts import render

from book.domain.repositories import BookRepository, BookshelfRepository
from book.domain.services import BookDomainService
from search.application.usecases import BookSearchByTitleUsecase
from search.domain.services import BookSearchService, GoogleBooksService
from search.infrastracture.external.apis import GoogleBooksAPIClient


def book_search(request):
    """書籍検索"""
    query = request.GET.get("query")
    mode = request.GET.get("mode", "")
    page = int(request.GET.get("page", 1))

    # TODO 検証のため
    mode = "detail"

    if mode == "detail":
        search_service = GoogleBooksService(
            GoogleBooksAPIClient(),
            BookDomainService(BookRepository(), BookshelfRepository()),
        )
    else:
        search_service = BookSearchService()

    usecase = BookSearchByTitleUsecase(mode, page, query, search_service)
    context = usecase.execute()

    return render(request, "books/search_results.html", context)
