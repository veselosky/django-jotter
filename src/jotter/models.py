from django.conf import settings
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from tinymce.models import HTMLField


class NotebookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("user")


class NotebookQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)

    def mark_deleted(self):
        return self.update(is_deleted=True)


class Notebook(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = NotebookManager.from_queryset(NotebookQuerySet)()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "slug"], name="unique_notebook_slug_for_user"
            )
        ]

    def get_absolute_url(self):
        return reverse("jotter_notebook_detail", kwargs={"notebook_slug": self.slug})

    def __str__(self):
        return self.name


class NoteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("notebook", "notebook__user")


class NoteQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)

    def mark_deleted(self):
        return self.update(is_deleted=True)


class Note(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    content = HTMLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = NoteManager.from_queryset(NoteQuerySet)()
    tags = TaggableManager(blank=True)

    def get_absolute_url(self):
        return reverse(
            "jotter_note_update",
            kwargs={"pk": self.pk, "notebook_slug": self.notebook.slug},
        )
