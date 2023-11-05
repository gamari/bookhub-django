from django.urls import path

from . import views, views_api

urlpatterns = [
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path("notes/<int:note_id>/edit/", views.edit_note, name="edit_note"),
    path("notes/<int:note_id>/delete/", views.delete_note, name="delete_note"),
    path('books/<int:book_id>/notes/', views.note_of_book, name='create_note_of_book'),
    
    # api
    path("api/ai/books/<int:book_id>/notes/", views_api.CreateNoteByOutput.as_view(), name="create_note_by_output")
]
