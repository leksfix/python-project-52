from django.urls import reverse
from task_manager.tests.utils.my_test_case import MyTestCase
from task_manager.statuses.models import Status


class StatusesIndexViewTest(MyTestCase):
    def setUp(self):
        super().setUp()
        number_of_statuses = 5
        for status_num in range(number_of_statuses):
            Status.objects.create(name=f'Status {status_num}')
        self.statuses = Status.objects.all().order_by("id")

    def test_statuses_list_if_not_logged_in(self):
        response = self.client.get(reverse('statuses:index'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_statuses_list_if_logged_in(self):
        self.login_user_1()
        response = self.client.get(reverse('statuses:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_list.html')
        self.assertQuerySetEqual(self.statuses, response.context['status_list'])


class StatusesCreateViewTest(MyTestCase):
    def test_status_create_not_logged_in(self):
        response = self.client.post(
            reverse('statuses:create'),
            {'name': 'Новый статус'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_status_create_logged_in(self):
        self.login_user_1()
        response = self.client.post(
            reverse('statuses:create'),
            {'name': 'Новый статус'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("statuses:index")))
        self.assertTrue(Status.objects.filter(name='Новый статус').exists())


class StatusesUpdateViewTest(MyTestCase):
    def setUp(self):
        super().setUp()
        self.status = Status.objects.create(name='Старый статус')

    def test_status_update_not_logged_in(self):
        url = reverse('statuses:update', kwargs={'pk': self.status.pk})
        data = {'name': 'Новый статус'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_status_update_logged_in(self):
        self.login_user_1()
        url = reverse('statuses:update', kwargs={'pk': self.status.pk})
        data = {'name': 'Новый статус'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("statuses:index")))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Новый статус')


class StatusesDeleteViewTest(MyTestCase):
    def setUp(self):
        super().setUp()
        self.status = Status.objects.create(name='Статус')

    def test_status_delete_not_logged_in(self):
        url = reverse('statuses:delete', kwargs={'pk': self.status.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_status_delete_logged_in(self):
        self.login_user_1()
        url = reverse('statuses:delete', kwargs={'pk': self.status.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("statuses:index")))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
