from apps.management.models import Notice


class NoticeDomainService(object):
    def __init__(self) -> None:
        pass

    @classmethod
    def initialize(cls):
        return cls()

    def get_latest_notice(self):
        latest_notice = Notice.objects.order_by("-created_at").first()
        return latest_notice
    
    def get_latest_notices(self, limit=3):
        latest_notices = Notice.objects.order_by("-created_at")[:limit]
        return latest_notices