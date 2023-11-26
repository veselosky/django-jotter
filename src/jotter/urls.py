from django.urls import path

from . import views

urlpatterns = [
    path("", views.NotebookListView.as_view(), name="jotter_index"),
    path(
        "notebook/create/",
        views.NotebookCreateView.as_view(),
        name="jotter_notebook_create",
    ),
    path(
        "<slug:notebook_slug>/",
        views.NoteListView.as_view(),
        name="jotter_notebook_detail",
    ),
    path(
        "<slug:notebook_slug>/create/",
        views.NoteCreateView.as_view(),
        name="jotter_note_create",
    ),
    path(
        "<slug:notebook_slug>/<int:pk>/",
        views.NoteUpdateView.as_view(),
        name="jotter_note_update",
    ),
]
