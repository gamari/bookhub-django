import logging, openai
from typing import List
from apps.book.models import Book

from config.ai import OpenAiClient
from config.settings import OPEN_AI_KEY
from config.utils import extract_ids_from_selection

logger = logging.getLogger("app_logger")

# TODO resetの機構はよくないので、リファクタリングする。

class AiDomainService(object):
    def __init__(self) -> None:
        self.client = OpenAiClient(OPEN_AI_KEY)
    
    @classmethod
    def initialize(cls):
        return cls()
    
    def reset(self):
        self.client.reset()
    
    def create_selection_title_by_demand(self, demand: str) -> str:
        instruction = "指定された要求を満たす書籍を検索するための「検索ワード」を作成してください。検索ワードは、できるだけ曖昧にヒットしやすいワードを選んでください。ただし、検索ワードを空白区切りで返してください。また、検索ワード以外の言葉含めないでください。"

        self.client.add_system_message(instruction)
        self.client.add_sample_message("user", "推理ものの小説を見たい。")
        self.client.add_sample_message("assistant", "検索ワード:推理 小説")
        self.client.add_user_message(demand)
        title = self.client.query()
        self.reset()

        title = title.replace("検索ワード:", "")

        return title
    
    def create_tags_by_demand(self, demand: str) -> List[str]:
        instruction = "指定された要求を満たす書籍を検索するための「タグ」を作成してください。ただし、以下のルールに従って作成してください。\n#ルール\n1. タグは空白区切りで返してください。\n2. タグ以外の言葉含めないでください。\n3. タグは4つ作成してください。"

        self.client.add_system_message(instruction)
        self.client.add_sample_message("user", "推理ものの小説を見たい。")
        self.client.add_sample_message("assistant", "タグ:推理 小説")
        self.client.add_user_message(demand)
        response = self.client.query()
        self.reset()

        tags = response.replace("タグ", "").split(" ")

        return tags
    
    def create_tags_by_book(self, book):
        """タグ作成。"""
        sample_title="対岸の家事"
        sample = "家族のために「家事をすること」を仕事に選んだ、専業主婦の詩穂。娘とたった二人だけの、途方もなく繰り返される毎日。幸せなはずなのに、自分の選択が正しかったのか迷う彼女のまわりには、性別や立場が違っても、同じく現実に苦しむ人たちがいた。二児を抱え、自分に熱があっても休めない多忙なワーキングマザー。医者の夫との間に子どもができず、姑や患者にプレッシャーをかけられる主婦。外資系企業で働く妻の代わりに、二年間の育休をとり、１歳の娘を育てるエリート公務員。誰にも頼れず、いつしか限界を迎える彼らに、詩穂は優しく寄り添い、自分にできることを考え始める――。"[:120]
        instruction = "指定された書籍と、書籍詳細の内容から、タグを作成してください。ただし、タグを空白区切りで返してください。また、タグ以外の言葉含めないでください。"

        self.client.add_system_message(instruction)
        self.client.add_sample_message("user", f"書籍名:{sample_title}\n書籍詳細:{sample}")
        self.client.add_sample_message("assistant", "タグ:子育て 小説 生き方 母")
        self.client.add_user_message(book.description[:180])
        tags = self.client.query()
        self.reset()

        tags = tags.replace("タグ:", "").split(" ")
        logger.debug(f"tags: {tags}")
        
        # 空配列は排除する
        tags = list(filter(lambda x: x != "", tags))

        return tags

    def create_selection_title_by_book_ids(self, book_ids_str: str) -> str:
        instruction = "指定された書籍一覧から、最適なタイトルをつけてください。注目を集めやすいタイトルにしてください。"

        self.client.add_system_message(instruction)
        self.client.add_sample_message("assistant", "タイトル:泣ける作品集")
        self.client.add_user_message(f"書籍一覧:\n{book_ids_str}")
        title = self.client.query()
        logger.debug(f"RESPONSE: {title}")
        self.reset()

        title = title.replace("タイトル:", "")

        return title
    
    def create_selection_title_by_profile(self, profile):
        instruction = "指定されたプロフィールの人が調べそうな「検索ワード」を作成してください。検索ワードは、できるだけ曖昧にヒットしやすいワードを選んでください。ただし、検索ワードを空白区切りで返してください。また、検索ワード以外の言葉含めないでください。ワードは4つまでです。"

        self.client.add_system_message(instruction)
        self.client.add_sample_message("user", "推理小説が好きです。")
        self.client.add_sample_message("assistant", "検索ワード:推理 小説")
        self.client.add_user_message(profile)

        title = self.client.query()
        title = title.replace("検索ワード:", "")
        self.reset()

        return title
    
    def recommend_books_by_demand(self, demand, books: List[Book]):
        target = [{
            "id": book.id,
            "title": book.title,
        } for book in books]
        logger.debug(f"target: {target}")


        instruction = "指定された要求と、書籍一覧を見比べて、おすすめの本をピックアップしてください。ただし、ルールに従って選択してください。\n\n# ルール\n1.JSONの配列形式のみで返してください。\n2. idのみを返してください。\n3. 同一タイトルのものは選択しないでください。\n4. 過激な内容やセンシティブな内容は選択しないでください。\n5. 選択できる数は5つまでです。\n6. 要求を満たした書籍のみを選択してください。"

        # 選択する
        self.client.add_system_message(instruction)
        self.client.add_sample_message("assistant", "選択したID:[230, 1258, 5852]")
        self.client.add_user_message(f"{demand}\n\n書籍一覧:\n{target}")
        logger.debug(target)

        response = self.client.query()
        logger.debug(f"RESPONSE: {response}")
        selected_ids = response.replace("選択したID:", "")
        self.reset()

        recommend_book_ids = extract_ids_from_selection(selected_ids)
        logger.debug(recommend_book_ids)
        recommend_books = [book for book in books if book.id in recommend_book_ids]

        return recommend_books
    
    def recommend_books_by_profile(self, profile, books):
        instruction = "指定されたプロフィールと、書籍一覧を見比べて、おすすめの本を3つピックアップしてください。ただし、JSONの配列形式のみ返してください。また、idのみを返してください。同一タイトルのものは選択しないでください。そして、過激な内容やセンシティブな内容は選択しないでください。"

        self.client.add_system_message(instruction)
        self.client.add_sample_message("assistant", "選択したID:[230, 333, 1258]")
        self.client.add_user_message(f"{profile}\n\n書籍一覧:\n{books}")

        selection = self.client.query()
        logger.debug(f"RESPONSE: {selection}")
        selection = selection.replace("選択したID:", "")
        self.reset()

        return selection