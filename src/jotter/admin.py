from django.contrib import admin

from .models import Note, Notebook


@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created", "updated")
    search_fields = ("name", "user__username")
    readonly_fields = ("created", "updated")
    list_filter = ("user",)
    ordering = ("-updated",)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "notebook", "created", "updated")
    search_fields = ("title", "notebook__name")
    readonly_fields = ("created", "updated")
    list_filter = ("notebook__user", "notebook")
    ordering = ("-updated",)
