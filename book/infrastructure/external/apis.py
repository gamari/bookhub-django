import requests

from config.settings import GOOGLE_BOOKS_API_KEY

class GoogleBooksAPIClient:
    @staticmethod
    def fetch_books(query, page):
        print("GoogleBooksAPIClient")
        startIndex = (int(page) - 1) * 10
        GOOGLE_BOOKS_API_URL = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{query}&startIndex={startIndex}&maxResults=10&langRestrict=ja&Country=JP&key={GOOGLE_BOOKS_API_KEY}"
        print(GOOGLE_BOOKS_API_URL)
        
        response = requests.get(GOOGLE_BOOKS_API_URL)
        
        return response.json() if response.status_code == 200 else {}
