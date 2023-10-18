from django.urls import path

import apps.selection.views

urlpatterns = [
    path("selection/create/", apps.selection.views.create_selection, name="create_selection"),
    path("selection/<uuid:selection_id>/", apps.selection.views.selection_detail, name="selection_detail"),
    path("selection/<uuid:selection_id>/delete/", apps.selection.views.delete_selection, name="delete_selection"),

    # OGP
    path('ogp/<uuid:selection_id>/', apps.selection.views.generate_ogp, name='generate_ogp'),
]
