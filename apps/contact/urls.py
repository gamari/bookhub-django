from django.urls import path

from . import views

urlpatterns = [
    path("contact/", views.contact_page, name="contact"),
    path("help/activity/", views.help_activity_page, name="help_activity"),
    path("terms/", views.terms_page, name="terms"),
    path("privacy/", views.privacy_page, name="privacy")
]
