import logging

from django.shortcuts import render
from django.core.paginator import Paginator

from apps.book.domain.repositories import BookRepository, BookshelfRepository
from apps.book.domain.services import BookDomainService
from apps.book.models import Book
from apps.search.application.usecases import BookSearchByTitleUsecase
from apps.search.domain.services import BookSearchService, GoogleBooksService
from apps.search.infrastracture.external.apis import GoogleBooksAPIClient
from apps.search.models import SearchHistory

logger = logging.getLogger("app_logger")

def book_search(request):
    """書籍検索"""
    query = request.GET.get("query")
    mode = request.GET.get("mode", "")
    page = int(request.GET.get("page", 1))

    # queryが無い場合はページを表示
    if not query:
        return render(request, "pages/search_results.html")

    if mode == "detail":
        logger.debug("詳細検索します")
        search_service = GoogleBooksService(
            GoogleBooksAPIClient(),
            BookDomainService(BookRepository(), BookshelfRepository()),
        )
    else:
        logger.debug("通常検索します")
        search_service = BookSearchService()

    try:
        usecase = BookSearchByTitleUsecase(search_service)
        context = usecase.execute(mode, page, query)

        if page == 1:
            if request.user.is_authenticated:
                SearchHistory.objects.create(query=query, user=request.user)
            else:
                SearchHistory.objects.create(query=query)

        return render(request, "pages/search_results.html", context)
    except ValueError as e:
        context = {"error_message": str(e)}
        return render(request, "pages/search_results.html", context)

def tag_search(request):
    tag_name = request.GET.get("tag")
    page = request.GET.get('page')

    if not tag_name:
        return render(request, "pages/search/tag.html")

    if not page:
        page = 1
    
    books = Book.objects.filter(tags__name=tag_name)
    paginator = Paginator(books, 1)
    result = paginator.get_page(page)
    logger.debug(result)
    logger.debug(result.next_page_number)
    logger.debug(result.paginator.num_pages)
    
    return render(request, "pages/search/tag.html", {"tag_name": tag_name, "result": result})
    
