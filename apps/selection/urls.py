from django.urls import path

from . import views, views_api

urlpatterns = [
    path("selection/<uuid:selection_id>/", views.selection_detail, name="selection_detail"),
    path("selection/<uuid:selection_id>/delete/", views.delete_selection, name="delete_selection"),
    path("selection/create/", views.CreateSelectionView.as_view(), name="create_selection"),
    path('selection/<uuid:selection_id>/edit/', views.EditSelectionView.as_view(), name='edit_selection'),

    # TODO OGP 未完成
    path('ogp/<uuid:selection_id>/', views.generate_ogp, name='generate_ogp'),

    # API
    path('api/selection/<uuid:selection_id>/like/', views_api.like_book_selection, name='api_like_book_selection'),
]
