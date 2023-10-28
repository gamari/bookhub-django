from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.providers.google.urls')),  # Google認証のみ利用


    path("", include("authentication.urls")),
    path("", include("apps.book.urls")),
    path("", include("apps.record.urls")),
    path("", include("apps.review.urls")),
    path("", include("apps.follow.urls")),
    path("", include("apps.contact.urls")),
    path("", include("apps.ranking.urls")),
    path("", include("apps.search.urls")),
    path("", include("apps.selection.urls")),
    path("", include("apps.management.urls")),
]

# ファイル設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("admin/", admin.site.urls)]