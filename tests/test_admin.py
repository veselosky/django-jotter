from django.contrib.auth import get_user_model
from django.test import TestCase


class AdminViewsTestCase(TestCase):
    """Test the Add and ChangeList views for the admin site for each of our models."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        User.objects.create_superuser(
            username="testadmin", email="superuser@example.com", password="test"
        )

    def setUp(self):
        self.client.login(username="testadmin", password="test")

    def test_notebook_add(self):
        response = self.client.get("/admin/jotter/notebook/add/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/jotter/notebook/")
        self.assertEqual(response.status_code, 200)

    def test_note_add(self):
        response = self.client.get("/admin/jotter/note/add/")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/jotter/note/")
        self.assertEqual(response.status_code, 200)
