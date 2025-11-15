from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from task_manager.users.models import User

class StatusesIndexViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        number_of_statuses = 5
        for status_num in range(number_of_statuses):
            Status.objects.create(name=f'Status {status_num}')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('statuses:index'))
        self.assertRedirects(resp, '/login/?next=/statuses/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('statuses:index'))
        self.assertEqual(str(resp.context['user']), 'testuser1')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'statuses/status_list.html')

    def test_statuses_list(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('statuses:index'))
        self.assertEqual(str(resp.context['user']), 'testuser1')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('status_list' in resp.context)
        self.assertEqual(len(resp.context['status_list']), 5)


class StatusesCreateViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()

    def test_status_create_not_logged_in(self):
        response = self.client.post(
            reverse('statuses:create'),
            {'name': 'Новый статус'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_status_create_logged_in(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('statuses:index'))
        self.assertEqual(str(resp.context['user']), 'testuser1')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('status_list' in resp.context)
        self.assertEqual(len(resp.context['status_list']), 0)
        response = self.client.post(
            reverse('statuses:create'),
            {'name': 'Новый статус'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='Новый статус').exists())
        resp = self.client.get(reverse('statuses:index'))
        self.assertTrue('status_list' in resp.context)
        self.assertEqual(len(resp.context['status_list']), 1)


class StatusesUpdateViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        self.status = Status.objects.create(name='Старый статус')

    def test_status_update_not_logged_in(self):
        url = reverse('statuses:update', kwargs={'pk': self.status.pk})
        data = {'name': 'Новый статус'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_status_update_logged_in(self):
        self.client.login(username='testuser1', password='12345')
        url = reverse('statuses:update', kwargs={'pk': self.status.pk})
        data = {'name': 'Новый статус'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Новый статус')


class StatusesDeleteViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        self.status = Status.objects.create(name='Статус')

    def test_status_delete_not_logged_in(self):
        url = reverse('statuses:delete', kwargs={'pk': self.status.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_status_delete_logged_in(self):
        self.client.login(username='testuser1', password='12345')
        url = reverse('statuses:delete', kwargs={'pk': self.status.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
