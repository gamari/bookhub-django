import logging
import openai

from config.settings import OPEN_AI_KEY

logger = logging.getLogger("app_logger")

class AiDomainService(object):
    def __init__(self) -> None:
        openai.api_key = OPEN_AI_KEY

    def create_selection_title(self, demand):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "指定された要求を満たす書籍を検索するための「検索ワード」を作成してください。検索ワードは、できるだけ曖昧にヒットしやすいワードを選んでください。ただし、検索ワードを空白区切りで返してください。また、検索ワード以外は含めないでください。"
                },
                {
                    "role": "user", 
                    "content": "推理小説が見たいです。"
                },
                {
                    "role": "assistant",
                    "content": "推理 小説"
                },
                {
                "role": "user",
                "content": demand
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        tokens = response.usage.get("total_tokens")
        logger.info(f"USE TOKENS: {tokens}")
        title = response.choices[0].message.content

        return title
    
    def recommend_books(self, demand, books):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "指定された要求と、書籍一覧を見比べて、おすすめの本を3つピックアップしてください。ただし、JSONの配列形式のみ返してください。また、idのみを返してください。同一タイトルのものは選択しないでください。そして、過激な内容やセンシティブな内容は選択しないでください。"
                },
                {
                    "role": "assistant",
                    "content": "[230, 333, 1258]"
                },
                {
                    "role": "user",
                    "content": f"{demand}\n\n書籍一覧:\n{books}"
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        selecion = response.choices[0].message.content
        logger.info(selecion)

        return selecion