from datetime import datetime, timedelta
import requests

from config.settings import GOOGLE_BOOKS_API_KEY


class URLBuilder(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.params = {}

    def add_param(self, key, value):
        self.params[key] = value
        return self

    def build(self):
        param_str = "&".join([f"{k}={v}" for k, v in self.params.items()])
        return f"{self.base_url}?{param_str}"


class GoogleBooksURLBuilder(URLBuilder):
    def with_query(self, query):
        return self.add_param("q", query)
    
    def with_query_in_title(self, query):
        # return self.add_param("q", 'intitle:"' + query + '"')
        return self.add_param("q", 'intitle:' + query + '')
    
    def with_query_in_description(self, query):
        return self.add_param("q", f'"{query} in:description"')

    def with_start_index(self, start_index):
        return self.add_param("startIndex", start_index)
    
    def with_print_type(self, print_type="books"):
        """
        all, books, magazines
        """
        return self.add_param("printType", print_type)

    def with_max_results(self, max_results=10):
        return self.add_param("maxResults", max_results)

    def with_lang_restrict(self, lang="ja"):
        return self.add_param("langRestrict", lang)

    def with_country(self, country="JP"):
        return self.add_param("Country", country)
    
    def with_order_by(self, order_by="relevance"):
        """relevance, newest"""
        return self.add_param("orderBy", order_by)

    def with_api_key(self, api_key):
        return self.add_param("key", api_key)
    



class GoogleBooksAPIClient(object):
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"

    def fetch_books(self, query, page):
        start_index = (int(page) - 1) * 10
        url = (
            GoogleBooksURLBuilder(GoogleBooksAPIClient.BASE_URL)
            # .with_query(query)
            .with_query_in_title(query)
            # .with_query_in_description(query)
            .with_start_index(start_index)
            # .with_max_results(10)
            .with_lang_restrict("ja")
            .with_country("JP")
            .with_print_type("books")
            .with_order_by("relevance")
            .with_api_key(GOOGLE_BOOKS_API_KEY)
            .build()
        )
        print(url)
        response = requests.get(url)
        return response.json() if response.status_code == 200 else {}

    @staticmethod
    def fetch_new_books():
        # TODO 確認する
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=7)
        query = f"publishedDate:{start_date}..{end_date}"
        url = (
            GoogleBooksURLBuilder(GoogleBooksAPIClient.BASE_URL)
            .with_query(query)
            .with_max_results(10)
            .with_lang_restrict("ja")
            .with_country("JP")
            .with_api_key(GOOGLE_BOOKS_API_KEY)
            .build()
        )
        print(url)
        response = requests.get(url)
        return response.json() if response.status_code == 200 else {}
