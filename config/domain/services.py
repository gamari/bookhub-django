import logging, openai

from config.ai import OpenAiClient
from config.settings import OPEN_AI_KEY

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
    
    def create_tags_by_book(self, book):
        """タグ作成。"""
        # title = book.title
        # description = book.description[:180]
        title="対岸の家事"
        description = "家族のために「家事をすること」を仕事に選んだ、専業主婦の詩穂。娘とたった二人だけの、途方もなく繰り返される毎日。幸せなはずなのに、自分の選択が正しかったのか迷う彼女のまわりには、性別や立場が違っても、同じく現実に苦しむ人たちがいた。二児を抱え、自分に熱があっても休めない多忙なワーキングマザー。医者の夫との間に子どもができず、姑や患者にプレッシャーをかけられる主婦。外資系企業で働く妻の代わりに、二年間の育休をとり、１歳の娘を育てるエリート公務員。誰にも頼れず、いつしか限界を迎える彼らに、詩穂は優しく寄り添い、自分にできることを考え始める――。"[:180]
        instruction = "指定された書籍と、書籍詳細の内容から、タグを作成してください。ただし、タグを空白区切りで返してください。また、タグ以外の言葉含めないでください。"

        self.client.add_system_message(instruction)
        self.client.add_sample_message("user", f"書籍名:{title}\n書籍詳細:{description}")
        self.client.add_sample_message("assistant", "タグ:子育て 小説 生き方 母")
        self.client.add_user_message(book.description)
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
    
    def recommend_books_by_demand(self, demand, books):
        instruction = "指定された要求と、書籍一覧を見比べて、おすすめの本を3つピックアップしてください。ただし、JSONの配列形式のみ返してください。また、idのみを返してください。同一タイトルのものは選択しないでください。そして、過激な内容やセンシティブな内容は選択しないでください。"

        self.client.add_system_message(instruction)
        self.client.add_sample_message("assistant", "選択したID:[230, 333, 1258]")
        self.client.add_user_message(f"{demand}\n\n書籍一覧:\n{books}")

        selection = self.client.query()
        logger.debug(f"RESPONSE: {selection}")
        selection = selection.replace("選択したID:", "")
        self.reset()

        return selection
    
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