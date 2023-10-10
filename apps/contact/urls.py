from django.urls import path

from .views import contact_page, help_activity_page

urlpatterns = [
    path("contact/", contact_page, name="contact"),
    path("help/activity/", help_activity_page, name="help_activity")
]
