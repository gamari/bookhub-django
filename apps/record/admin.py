from django.contrib import admin

from apps.record.models import ReadingMemo, ReadingRecord

admin.site.register(ReadingRecord)
admin.site.register(ReadingMemo)