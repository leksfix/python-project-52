from django.urls import reverse

from task_manager.tests.utils.my_test_case import MyTestCase
from task_manager.users.models import User


class UsersLoginViewTest(MyTestCase):
    def test_user_login(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': self._test_username_1,
                'password': self._test_password_1,
            }
        )
        self.assertEqual(int(self.client.session['_auth_user_id']), self.test_user_1.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))


class UsersIndexViewTest(MyTestCase):
    def setUp(self):
        super().setUp()

    def test_users_list(self):
        response = self.client.get(reverse('users:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertQuerySetEqual(
            User.objects.all().order_by("id"),
            response.context['user_list'].order_by("id"))


class UsersCreateViewTest(MyTestCase):
    def test_user_create(self):
        response = self.client.post(
            reverse('users:create'),
            {
                'first_name': 'First',
                'last_name': 'Last',
                'username': 'testuser',
                'password1': 'testpassword',
                'password2': 'testpassword',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))
        self.assertTrue(User.objects.filter(username='testuser').exists())


class UsersUpdateViewTest(MyTestCase):
    def setUp(self):
        super().setUp()
        self.updated_user = {
            'first_name': 'First',
            'last_name': 'Last',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

    def test_user_update_not_logged_in(self):
        user_old = self.test_user_1
        url = reverse('users:update', kwargs={'pk': user_old.pk})
        response = self.client.post(url, self.updated_user)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("users:index")))
        user_new = User.objects.get(pk=user_old.pk)
        self.assertEqual(user_new.first_name, user_old.first_name)
        self.assertEqual(user_new.last_name, user_old.last_name)
        self.assertEqual(user_new.username, user_old.username)
        self.assertEqual(user_new.password, user_old.password)

    def test_user_update_not_me(self):
        self.login_user_1()
        user_old = self.test_user_2
        url = reverse('users:update', kwargs={'pk': user_old.pk})
        response = self.client.post(url, self.updated_user)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("users:index")))
        user_new = User.objects.get(pk=user_old.pk)
        self.assertEqual(user_new.first_name, user_old.first_name)
        self.assertEqual(user_new.last_name, user_old.last_name)
        self.assertEqual(user_new.username, user_old.username)
        self.assertEqual(user_new.password, user_old.password)

    def test_user_update_me(self):
        self.login_user_1()
        user_old = self.test_user_1
        url = reverse('users:update', kwargs={'pk': user_old.pk})
        response = self.client.post(url, self.updated_user)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("users:index")))
        user_new = User.objects.get(pk=user_old.pk)
        self.assertEqual(user_new.first_name, self.updated_user['first_name'])
        self.assertEqual(user_new.last_name, self.updated_user['last_name'])
        self.assertEqual(user_new.username, self.updated_user['username'])
        self.assertTrue(
            self.client.login(
                username=self.updated_user['username'],
                password=self.updated_user['password1'],
            )
        )
        self.assertEqual(int(self.client.session['_auth_user_id']), user_old.id)



class UserDeleteViewTest(MyTestCase):
    def setUp(self):
        super().setUp()

    def test_user_delete_not_logged_in(self):
        url = reverse('users:delete', kwargs={'pk': self.test_user_1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("users:index")))

    def test_user_delete_not_me(self):
        self.login_user_2()
        url = reverse('users:delete', kwargs={'pk': self.test_user_1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("users:index")))
        self.assertTrue(User.objects.filter(pk=self.test_user_1.pk).exists())

    def test_user_delete_me(self):
        self.login_user_1()
        url = reverse('users:delete', kwargs={'pk': self.test_user_1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("users:index")))
        self.assertFalse(User.objects.filter(pk=self.test_user_1.pk).exists())
