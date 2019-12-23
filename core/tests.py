from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy

User = get_user_model()


class UserTestCase(TestCase):

    def setUp(self) -> None:
        User.objects.create_superuser(username='admin', email='admin@admin.com', password='admin123')
        User.objects.create_user(username='caio', email='caio@caio.com', password='123456')
        self.client = Client()

    def test_user_cannot_list_authors(self):
        self.client.login(username='caio', password='123456')
        response = self.client.get(reverse_lazy('core:author_list'))
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_delete_author(self):
        self.client.login(username='caio', password='123456')
        response = self.client.get(reverse_lazy('core:author_delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 403)

    def test_user_can_access_only_his_update_view(self):
        self.client.login(username='caio', password='123456')
        response = self.client.get(reverse_lazy('core:author_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)
        response = self.client.get(reverse_lazy('core:author_update', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_view_author_list_view(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse_lazy('core:author_list'))
        authors = response.context['authors']
        self.assertEqual(authors.count(), 2)
