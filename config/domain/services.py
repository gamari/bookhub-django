import logging, openai

from config.ai import OpenAiClient
from config.settings import OPEN_AI_KEY

logger = logging.getLogger("app_logger")

class AiDomainService(object):
    def __init__(self) -> None:
        self.client = OpenAiClient(OPEN_AI_KEY)
    
    @classmethod
    def initialize(cls):
        return cls()
    
    def _create_selection_title(self, instruction: str, content: str):
        # TODO 検証
        self.client.add_system_message(instruction)
        self.client.add_user_message(content)
        title = self.client.query()
        logger.debug(f"RESPONSE: {title}")
        logger.info(f"USE TOKENS: {title}")
        return title
    
    def create_selection_title_by_demand(self, demand: str) -> str:
        instruction = "指定された要求を満たす書籍を検索するための「検索ワード」を作成してください。検索ワードは、できるだけ曖昧にヒットしやすいワードを選んでください。ただし、検索ワードを空白区切りで返してください。また、検索ワード以外の言葉含めないでください。"

        self.client.add_system_message(instruction)
        self.client.add_sample_message("user", "推理ものの小説を見たい。")
        self.client.add_sample_message("assistant", "検索ワード:推理 小説")
        self.client.add_user_message(demand)
        title = self.client.query()

        title = title.replace("検索ワード:", "")

        return title

    
    def create_selection_title_by_profile(self, profile):
        instruction = "指定されたプロフィールの人が調べそうな「検索ワード」を作成してください。検索ワードは、できるだけ曖昧にヒットしやすいワードを選んでください。ただし、検索ワードを空白区切りで返してください。また、検索ワード以外の言葉含めないでください。"

        self.client.add_system_message(instruction)
        self.client.add_sample_message("user", "推理小説が好きです。")
        self.client.add_sample_message("assistant", "検索ワード:推理 小説")
        self.client.add_user_message(profile)

        title = self.client.query()
        title = title.replace("検索ワード:", "")

        return title
    
    def recommend_books(self, demand, books):
        instruction = "指定された要求と、書籍一覧を見比べて、おすすめの本を3つピックアップしてください。ただし、JSONの配列形式のみ返してください。また、idのみを返してください。同一タイトルのものは選択しないでください。そして、過激な内容やセンシティブな内容は選択しないでください。"

        self.client.add_system_message(instruction)
        self.client.add_sample_message("assistant", "選択したID:[230, 333, 1258]")
        self.client.add_user_message(f"{demand}\n\n書籍一覧:\n{books}")

        selection = self.client.query()
        logger.debug(f"RESPONSE: {selection}")
        selection = selection.replace("選択したID:", "")

        return selection
    