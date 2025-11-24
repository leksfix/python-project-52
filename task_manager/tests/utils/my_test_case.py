from django.test import TestCase

from task_manager.users.models import User


class MyTestCase(TestCase):
    def setUp(self):
        self._test_username_1 = "testuser1"
        self._test_password_1 = "12345"
        self.test_user_1 = User.objects.create_user(
            username=self._test_username_1,
            password=self._test_password_1,
        )
        self.test_user_1.save()

        self._test_username_2 = "testuser2"
        self._test_password_2 = "54321"
        self.test_user_2 = User.objects.create_user(
            username=self._test_username_2,
            password=self._test_password_2,
        )
        self.test_user_2.save()

    def login_user_1(self):
        return self.client.login(
            username=self._test_username_1,
            password=self._test_password_1,
        )

    def login_user_2(self):
        return self.client.login(
            username=self._test_username_2,
            password=self._test_password_2,
        )
