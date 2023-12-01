from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class NotebookViewsTestCase(TestCase):
    """Test the CRUD views for notebooks and notes."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        User.objects.create_user(
            username="testuser", email="test@example.com", password="test"
        )

    def setUp(self):
        self.client.login(username="testuser", password="test")

    def test_crud_views(self):
        url = reverse("jotter_notebook_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.post(url, {"name": "Example Notebook"})
        self.assertEqual(response.status_code, 200)

        notebook_slug = "example-notebook"
        url = reverse("jotter_notebook_detail", kwargs={"notebook_slug": notebook_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse("jotter_note_create", kwargs={"notebook_slug": notebook_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            url, {"title": "Example Note", "content": "Example Content"}
        )
        self.assertEqual(response.status_code, 302)

        note_pk = 1
        url = reverse(
            "jotter_note_update", kwargs={"notebook_slug": notebook_slug, "pk": note_pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            url, {"title": "Example Note", "content": "Example Content"}
        )
        self.assertEqual(response.status_code, 302)

        url = reverse(
            "jotter_note_delete", kwargs={"notebook_slug": notebook_slug, "pk": note_pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        url = reverse("jotter_notebook_delete", kwargs={"notebook_slug": notebook_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_notebook_list_view(self):
        url = reverse("jotter_index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
