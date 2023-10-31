import json
import logging
import requests
from requests_oauthlib import OAuth1

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config

logger = logging.getLogger("app_logger")

class AutoPostAPIView(APIView):
    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "管理者以外は利用できません。"}, status=status.HTTP_400_BAD_REQUEST)
        
        TWITTER_API_KEY = config("TWITTER_API_KEY", default="")
        TWITTER_API_SECRET_KEY = config("TWITTER_API_SECRET_KEY", default="")
        TWITTER_ACCESS_TOKEN = config("TWITTER_ACCESS_TOKEN", default="")
        TWITTER_SECRET_TOKEN = config("TWITTER_SECRET_TOKEN", default="")

        auth = OAuth1(TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_SECRET_TOKEN)

        payload = {
            "text": "テスト"
        }

        headers = {
            "Content-Type": "application/json"
        }

        url = "https://api.twitter.com/2/tweets"

        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)

            logger.debug(response.status_code)
            logger.debug(response.text)

            return Response({"detail": "ツイートが成功しました。"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({"detail": f"ツイートの投稿に失敗しました: {e}"}, status=status.HTTP_400_BAD_REQUEST)
