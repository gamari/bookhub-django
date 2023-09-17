import requests
from abc import ABC, abstractmethod


class BookAPI(ABC):
    @abstractmethod
    def search(self, query):
        pass

    @abstractmethod
    def get_detail(self, book_id):
        pass


class GoogleBooksAPI(BookAPI):
    BASE_URL = "https://www.googleapis.com/books/v1/volumes"

    def search(self, query):
        results = []
        response = requests.get(
            self.BASE_URL,
            params={"q": f"intitle:{query}", "langRestrict": "ja", "Country": "JP"},
        )
        data = response.json()
        for item in data.get("items", []):
            results.append(
                {
                    "title": item["volumeInfo"].get("title"),
                    "author": ", ".join(item["volumeInfo"].get("authors", [])),
                    "id": item["id"],
                    "thumbnail": item["volumeInfo"]
                    .get("imageLinks", {})
                    .get("thumbnail"),
                    # TODO 説明の追加
                    "description": item["volumeInfo"].get("description"),
                }
            )
        return results

    def get_detail(self, book_id):
        response = requests.get(f"{self.BASE_URL}/{book_id}")
        data = response.json()
        return {
            "title": data["volumeInfo"].get("title"),
            "author": ", ".join(data["volumeInfo"].get("authors", [])),
            "description": data["volumeInfo"].get("description"),
            "thumbnail": data["volumeInfo"].get("imageLinks", {}).get("thumbnail"),
        }
