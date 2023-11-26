from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .models import Note, Notebook


class NotebookListView(ListView):
    model = Notebook
    template_name = "jotter/index.html"
    context_object_name = "notebook_list"
    allow_empty = True


class NotebookCreateView(CreateView):
    model = Notebook
    template_name = "jotter/notebook_form.html"
    fields = ["name"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("jotter_index")


class NoteListView(ListView):
    model = Note
    template_name = "jotter/note_list.html"
    context_object_name = "note_list"
    allow_empty = True

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        if self.kwargs["notebook_slug"]:
            context["notebook"] = Notebook.objects.get(
                slug=self.kwargs["notebook_slug"],
                user=self.request.user,
            )
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        # Users can only see their own notes
        qs = qs.filter(notebook__user=self.request.user)
        # Filter by notebook if provided (optional, could be global search)
        if self.kwargs["notebook_slug"]:
            qs = qs.filter(notebook__slug=self.kwargs["notebook_slug"])
        return qs


class NoteCreateView(CreateView):
    model = Note
    template_name = "jotter/note_form.html"
    fields = ["title", "content", "tags"]

    def form_valid(self, form):
        form.instance.notebook = Notebook.objects.get(
            slug=self.kwargs["notebook_slug"],
            user=self.request.user,
        )
        return super().form_valid(form)


class NoteUpdateView(UpdateView):
    model = Note
    template_name = "jotter/note_form.html"
    fields = ["title", "content", "tags"]
