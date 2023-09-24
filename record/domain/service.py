class ReadingService:
    """読書ドメイン"""
    
    def __init__(self, record_repository):
        self.record_repository = record_repository

    def get_or_create_record(self, user, book):
        return self.record_repository.get_or_create(user, book)
