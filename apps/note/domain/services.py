import logging

from apps.note.models import Note
from config.ai import OpenAiClient
from config.settings import OPEN_AI_KEY


logger = logging.getLogger("app_logger")

class NoteAiService(OpenAiClient):
    def __init__(self, api_key: str) -> None:
        super().__init__(OPEN_AI_KEY)
    
    @classmethod
    def initialize(cls):
        return cls(OPEN_AI_KEY)
    
    def create_content_by_reading_memos(self, memos):
        """メモからノートの内容を作成する。"""
        instruction = "メモ一覧を元に、指定された要求を満たすノートを書いてください。"

        content = ""
        for memo in memos:
            content += memo.content + "\n"
        logger.debug(content)
        self.add_system_message(instruction)
        
        demand = "メモを整理して体系化してください。"
        self.add_user_message(f"""要求: {demand}

メモ一覧:
{content}
""")
        note = self.query()
        self.reset()
        logger.debug(note)

        return note
        

class NoteDomainService(object):
    def __init__(self) -> None:
        pass
    
    @classmethod
    def initialize(cls):
        return cls()
    
    def get_notes_by_book_and_user(self, book, user):
        return Note.objects.filter(book=book, author=user).order_by("-created_at")
    
    def create_content_by_reading_memos(self, memos):
        """メモからノートの内容を作成する。"""
        ai_service = NoteAiService.initialize()
        content = ai_service.create_content_by_reading_memos(memos)
        return content