from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('allauth.urls')),

    path("", include("authentication.urls")),
    path("", include("apps.book.urls")),
    path("", include("apps.record.urls")),
    path("", include("apps.review.urls")),
    path("", include("apps.follow.urls")),
    path("", include("apps.contact.urls")),
    path("", include("apps.ranking.urls")),
    path("", include("apps.search.urls")),
]

# ファイル設定
if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("admin/", admin.site.urls)]