from django.urls import path

from . import views

urlpatterns = [
    path(
        "notebook/create/",
        views.NotebookCreateView.as_view(),
        name="jotter_notebook_create",
    ),
    path(
        "<slug:notebook_slug>/delete/",
        views.NotebookDeleteView.as_view(),
        name="jotter_notebook_delete",
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
    path(
        "<slug:notebook_slug>/<int:pk>/delete/",
        views.NoteDeleteView.as_view(),
        name="jotter_note_delete",
    ),
    path("", views.NotebookListView.as_view(), name="jotter_index"),
]
