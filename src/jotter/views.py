from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from taggit.forms import TagWidget
from tinymce.widgets import TinyMCE

from .models import Note, Notebook


class NotebookListView(LoginRequiredMixin, ListView):
    model = Notebook
    template_name = "jotter/index.html"
    context_object_name = "notebook_list"
    allow_empty = True

    def get_queryset(self):
        qs = super().get_queryset()
        # Users can only see their own notebooks
        qs = qs.active().filter(user=self.request.user)
        return qs


class NotebookCreateView(LoginRequiredMixin, CreateView):
    model = Notebook
    template_name = "jotter/notebook_form.html"
    fields = ["name"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.name)
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["notebook_list"] = self.request.user.notebook_set.active()
        return context


class NotebookDeleteView(LoginRequiredMixin, DeleteView):
    model = Notebook
    template_name = "jotter/notebook_confirm_delete.html"
    slug_url_kwarg = "notebook_slug"

    def get_success_url(self):
        return reverse("jotter_index")

    def get_queryset(self):
        qs = super().get_queryset()
        # Users can only delete their own notebooks
        qs = qs.filter(user=self.request.user)
        return qs

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["notebook_list"] = self.request.user.notebook_set.active()
        return context


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "jotter/note_list.html"
    context_object_name = "note_list"
    allow_empty = True

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        if self.kwargs["notebook_slug"]:
            context["notebook"] = Notebook.objects.active().get(
                slug=self.kwargs["notebook_slug"],
                user=self.request.user,
            )
        # For the interface, we want to display a list of all the user's notebooks
        context["notebook_list"] = self.request.user.notebook_set.active()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        # Users can only see their own notes
        qs = qs.active().filter(notebook__user=self.request.user)
        # Filter by notebook if provided (optional, could be global search)
        if self.kwargs["notebook_slug"]:
            qs = qs.filter(notebook__slug=self.kwargs["notebook_slug"])
        # TODO filter Notes by tag if provided
        # TODO text search Note title field
        return qs


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "tags"]
        widgets = {
            "content": TinyMCE(
                mce_attrs={
                    "toolbar": (
                        "undo redo | bold italic | link | code | fullscreen"
                        " | bullist numlist | table | hr | removeformat | help"
                    ),
                    "menubar": True,
                    "plugins": (
                        "advlist anchor autosave code codesample emoticons fullscreen "
                        "help hr link lists paste preview quickbars searchreplace "
                        "table textpattern visualblocks visualchars wordcount"
                    ),
                },
            ),
            "title": forms.TextInput(attrs={"placeholder": "Title", "title": "Title"}),
            "tags": TagWidget(attrs={"placeholder": "Tags", "title": "Tags"}),
        }


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = "jotter/note_form.html"
    form_class = NoteForm

    def form_valid(self, form):
        form.instance.notebook = Notebook.objects.get(
            slug=self.kwargs["notebook_slug"],
            user=self.request.user,
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        self.notebook = self.request.user.notebook_set.active().get(
            slug=self.kwargs["notebook_slug"],
        )
        context["notebook_list"] = self.request.user.notebook_set.active()
        context["notebook"] = self.notebook
        context["note_list"] = self.notebook.note_set.active().defer("content")
        return context


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = "jotter/note_form.html"
    form_class = NoteForm

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["notebook_list"] = self.request.user.notebook_set.active()
        context["notebook"] = self.object.notebook
        context["note_list"] = self.object.notebook.note_set.active().defer("content")
        return context


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = "jotter/note_confirm_delete.html"

    def get_success_url(self):
        return reverse(
            "jotter_notebook_detail",
            kwargs={"notebook_slug": self.kwargs["notebook_slug"]},
        )

    def get_queryset(self):
        qs = super().get_queryset()
        # Users can only delete their own notes
        qs = qs.filter(notebook__user=self.request.user)
        return qs

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["notebook_list"] = self.request.user.notebook_set.active()
        context["notebook"] = self.object.notebook
        context["note_list"] = self.object.notebook.note_set.active().defer("content")
        return context
