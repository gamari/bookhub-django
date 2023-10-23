from django.urls import path

from . import views

urlpatterns = [
    path("selection/create/", views.create_selection, name="create_selection"),
    path("selection/<uuid:selection_id>/", views.selection_detail, name="selection_detail"),
    path("selection/<uuid:selection_id>/delete/", views.delete_selection, name="delete_selection"),
    path('edit_selection/<uuid:selection_id>/', views.edit_selection, name='edit_selection'),


    # TODO OGP 未完成
    path('ogp/<uuid:selection_id>/', views.generate_ogp, name='generate_ogp'),
]
