import requests
import logging
from requests_oauthlib import OAuth1
from decouple import config

logger = logging.getLogger("app_logger")


class BaseHttpClient(object):
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers if headers else {}

    def get(self, endpoint, params=None):
        response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers, params=params)
        return response

    def post(self, endpoint, data=None, json_data=None, headers=None):
        headers = {**self.headers, **(headers or {})}
        url = f"{self.base_url}{endpoint}"
        logger.debug(url)
        response = requests.post(url, headers=headers, data=data, json=json_data, auth=self.auth)
        return response

class TwitterClient(BaseHttpClient):
    def __init__(self, api_key=None, api_secret_key=None, access_token=None, secret_token=None):
        super().__init__("https://api.twitter.com/2/")
        
        self.api_key = api_key or config("TWITTER_API_KEY", default="")
        self.api_secret_key = api_secret_key or config("TWITTER_API_SECRET_KEY", default="")
        self.access_token = access_token or config("TWITTER_ACCESS_TOKEN", default="")
        self.secret_token = secret_token or config("TWITTER_SECRET_TOKEN", default="")
        self.auth = OAuth1(self.api_key, self.api_secret_key, self.access_token, self.secret_token)

    def post_tweet(self, text):
        endpoint = "tweets"
        headers = {
            "Content-Type": "application/json",
            **self.headers
        }
        logger.debug(headers)
        payload = {
            "text": text
        }
        response = self.post(endpoint, json_data=payload, headers=headers)

        if response.status_code != 201:
            logger.error(f"投稿に失敗しました: {response.text}")
            raise Exception("投稿に失敗しました。")
