from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("authentication.urls")),
    path("", include("book.urls")),
    path("", include("review.urls")),
    path("", include("record.urls")),
    path("", include("ranking.urls")),
    path("", include("search.urls")),
    path("", include("follow.urls")),
    path("", include("contact.urls")),
]

# ファイル設定
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)