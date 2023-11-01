import json
import logging
import requests
from requests_oauthlib import OAuth1

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config
from apps.management.application.usecases import CreateRecommendBook

logger = logging.getLogger("app_logger")

class RecommendPostAPIView(APIView):
    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "管理者以外は利用できません。"}, status=status.HTTP_400_BAD_REQUEST)
        
        usecase = CreateRecommendBook.build()
        usecase.execute()

        return Response({"detail": "ツイートが成功しました。"}, status=status.HTTP_200_OK)
