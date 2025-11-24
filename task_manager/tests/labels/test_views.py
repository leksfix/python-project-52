from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.tests.utils.my_test_case import MyTestCase


class LabelsIndexViewTest(MyTestCase):
    def setUp(self):
        super().setUp()
        number_of_labels = 3
        for label_num in range(number_of_labels):
            Label.objects.create(name=f'Label {label_num}')
        self.labels = Label.objects.all().order_by("id")

    def test_labels_list_not_logged_in(self):
        response = self.client.get(reverse('labels:index'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_labels_list_logged_in(self):
        self.login_user_1()
        response = self.client.get(reverse('labels:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_list.html')
        self.assertQuerySetEqual(self.labels, response.context['label_list'])


class LabelsCreateViewTest(MyTestCase):
    def test_label_create_not_logged_in(self):
        response = self.client.post(
            reverse('labels:create'),
            {'name': 'New label'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_label_create_logged_in(self):
        self.login_user_1()
        response = self.client.post(
            reverse('labels:create'),
            {'name': 'New label'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("labels:index")))
        self.assertTrue(Label.objects.filter(name='New label').exists())


class LabelsUpdateViewTest(MyTestCase):
    def setUp(self):
        super().setUp()
        self.label = Label.objects.create(name='Old label')

    def test_label_update_not_logged_in(self):
        url = reverse('labels:update', kwargs={'pk': self.label.pk})
        data = {'name': 'New label'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_label_update_logged_in(self):
        self.login_user_1()
        url = reverse('labels:update', kwargs={'pk': self.label.pk})
        data = {'name': 'New label'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("labels:index")))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'New label')


class LabelsDeleteViewTest(MyTestCase):
    def setUp(self):
        super().setUp()
        self.label = Label.objects.create(name='Label')

    def test_label_delete_not_logged_in(self):
        url = reverse('labels:delete', kwargs={'pk': self.label.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_label_delete_logged_in(self):
        self.login_user_1()
        url = reverse('labels:delete', kwargs={'pk': self.label.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("labels:index")))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
