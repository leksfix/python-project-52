from django.urls import reverse
from django.shortcuts import get_object_or_404
from task_manager.tests.utils.my_test_case import MyTestCase
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TasksIndexViewTest(MyTestCase):
    def setUp(self):
        super().setUp()
        self.labels = [
            Label.objects.create(name='Label 1'),
            Label.objects.create(name='Label 2'),
        ]
        self.statuses = [
            Status.objects.create(name='Status 1'),
            Status.objects.create(name='Status 2'),
        ]
        self.authors = [
            self.test_user_1,
            self.test_user_2,
        ]
        self.executors = [
            self.test_user_1,
            self.test_user_2,
        ]
        task_num = 0
        for label in self.labels:
            for status in self.statuses:
                for author in self.authors:
                    for executor in self.executors:
                        task_num += 1
                        task = Task.objects.create(
                            name=f'Task {task_num}',
                            description=f'Task {task_num} desc',
                            author=author,
                            executor=executor,
                            status=status,
                        )
                        task.labels.set([label])
        self.all_tasks = Task.objects.all().order_by("id")

    def test_tasks_list_not_logged_in(self):
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_tasks_list_all(self):
        self.login_user_1()
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_filter.html')
        self.assertQuerySetEqual(self.all_tasks, response.context['filter'].qs)

    def test_tasks_list_my_tasks(self):
        self.login_user_1()
        response = self.client.get(reverse('tasks:index'), {'my_tasks': True})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_filter.html')
        self.assertQuerySetEqual(
            Task.objects.filter(author=self.test_user_1.pk).order_by("id"),
            response.context['filter'].qs.order_by("id")
        )

        self.login_user_2()
        response = self.client.get(reverse('tasks:index'), {'my_tasks': True})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_filter.html')
        self.assertQuerySetEqual(
            Task.objects.filter(author=self.test_user_2.pk).order_by("id"),
            response.context['filter'].qs.order_by("id")
        )

    def test_tasks_list_filter(self):
        self.login_user_1()
        for label in self.labels:
            for status in self.statuses:
                for executor in self.executors:
                    response = self.client.get(
                        reverse('tasks:index'),
                        {
                            'status': status.pk,
                            'executor': executor.pk,
                            'label': label.pk,
                        }
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertTemplateUsed(response, 'tasks/task_filter.html')
                    self.assertQuerySetEqual(
                        Task.objects.filter(
                            status=status,
                            executor=executor,
                            labels__in=[label],
                        ).order_by("id"),
                        response.context['filter'].qs.order_by("id")
                    )


class TasksDetailViewTest(MyTestCase):
    def setUp(self):
        super().setUp()
        labels = [
            Label.objects.create(name='Label 1'),
            Label.objects.create(name='Label 2'),
        ]
        status = Status.objects.create(name='Status')
        user=self.test_user_1
        self.task = Task.objects.create(
            name='Task name',
            description='Task desc',
            author=user,
            executor=user,
            status=status,
        )
        self.task.labels.set(labels)

    def test_tasks_detail_not_logged_in(self):
        url = reverse('tasks:detail', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_tasks_detail_logged_in(self):
        self.login_user_1()
        url = reverse('tasks:detail', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        obj = response.context['object']
        self.assertQuerySetEqual([obj], [self.task], ordered=False)


class TasksCreateViewTest(MyTestCase):
    def setUp(self):
        super().setUp()
        self.labels = [
            Label.objects.create(name='Label 1').pk,
            Label.objects.create(name='Label 2').pk,
            ]
        self.status = Status.objects.create(name='Status')
        self.user=self.test_user_1

    def test_task_create_not_logged_in(self):
        response = self.client.post(
            reverse('tasks:create'),
            {
                'name': 'New task',
                'description': 'New task desc',
                'status': self.status.pk,
                'labels': self.labels,
                'executor': self.user.pk,
             }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_task_create_logged_in(self):
        self.login_user_1()
        response = self.client.post(
            reverse('tasks:create'),
            {
                'name': 'New task',
                'description': 'New task desc',
                'status': self.status.pk,
                'labels': self.labels,
                'executor': self.user.pk,
             }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("tasks:index")))
        task = get_object_or_404(Task, name='New task')
        self.assertEqual(task.description, 'New task desc')
        self.assertEqual(task.status.pk, self.status.pk)
        self.assertEqual(task.executor.pk, self.user.pk)
        self.assertListEqual(
            sorted(task.labels.values_list('pk', flat=True)),
            sorted(self.labels)
        )
        self.assertEqual(task.author.pk, self.user.id)


class TasksUpdateViewTest(MyTestCase):
    def setUp(self):
        super().setUp()
        self.old_labels = [
            Label.objects.create(name='Label 1').pk,
            Label.objects.create(name='Label 2').pk,
            ]
        self.new_labels = [
            Label.objects.create(name='Label 3').pk,
            Label.objects.create(name='Label 4').pk,
            ]
        self.old_status = Status.objects.create(name='Old status')
        self.new_status = Status.objects.create(name='New status')

        self.task = Task.objects.create(
                name='Old task',
                description='Old task desc',
                author=self.test_user_1,
                executor=self.test_user_1,
                status=self.old_status,
                )
        self.task.labels.set(self.old_labels)

    def test_task_update_not_logged_in(self):
        url = reverse('tasks:update', kwargs={'pk': self.task.pk})
        data = {
            'name': 'New task',
            'description': 'New task desc',
            'status': self.new_status.pk,
            'labels': self.new_labels,
            'executor': self.test_user_2.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_task_update_logged_in(self):
        self.login_user_1()
        url = reverse('tasks:update', kwargs={'pk': self.task.pk})
        data = {
            'name': 'New task',
            'description': 'New task desc',
            'status': self.new_status.pk,
            'labels': self.new_labels,
            'executor': self.test_user_2.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("tasks:index")))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'New task')
        self.assertEqual(self.task.description, 'New task desc')
        self.assertEqual(self.task.status.pk, self.new_status.pk)
        self.assertEqual(self.task.executor.pk, self.test_user_2.pk)
        self.assertListEqual(
            sorted(self.task.labels.values_list('pk', flat=True)),
            sorted(self.new_labels)
        )
        self.assertEqual(self.task.author.pk, self.test_user_1.pk)


class TasksDeleteViewTest(MyTestCase):
    def setUp(self):
        super().setUp()
        self.labels = [
            Label.objects.create(name='Label 1').pk,
            Label.objects.create(name='Label 2').pk,
            ]
        self.status = Status.objects.create(name='Test status')

        self.task = Task.objects.create(
                name='Test task',
                description='Test task desc',
                author=self.test_user_1,
                executor=self.test_user_1,
                status=self.status,
                )
        self.task.labels.set(self.labels)

    def test_task_delete_not_logged_in(self):
        url = reverse('tasks:delete', kwargs={'pk': self.task.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_task_delete_not_author(self):
        self.login_user_2()
        url = reverse('tasks:delete', kwargs={'pk': self.task.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("tasks:index")))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_author(self):
        self.login_user_1()
        url = reverse('tasks:delete', kwargs={'pk': self.task.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("tasks:index")))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())


