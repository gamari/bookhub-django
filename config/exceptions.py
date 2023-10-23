class ApplicationException(Exception):
    """アプリの固有例外を管理する。"""

    def __init__(self, errors):
        error_messages = []
        for field_errors in errors.values():
            error_messages.extend(field_errors)
        
        message = "\n".join(error_messages)
        self.message = message
        super().__init__(message)

class NotOwnerError(Exception):
    pass


class InvalidInputError(Exception):
    pass