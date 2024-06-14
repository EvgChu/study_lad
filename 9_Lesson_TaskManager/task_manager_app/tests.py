from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, Comment

class TaskManagerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(
            title='Test Task', 
            description='Test Description', 
            status=Task.Status.ACTIVE, 
            priority=Task.Priority.medium, 
            creator=self.user
        )
        self.comment = Comment.objects.create(task=self.task, text='Test Comment', creator=self.user)

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager_app/task_list.html')
        self.assertContains(response, 'Test Task')

    def test_task_list_view_with_filter(self):
        response = self.client.get(reverse('task_list') + '?status=АКТ')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
        
    def test_task_detail_view(self):
        response = self.client.get(reverse('task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager_app/task_detail.html')
        self.assertContains(response, 'Test Task')
        self.assertContains(response, 'Test Comment')

    def test_task_create_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager_app/task_form.html')

    def test_task_create_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('task_create'), {
            'title': 'New Task',
            'description': 'New Description',
            'status': Task.Status.ACTIVE,
            'priority': Task.Priority.medium
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_edit_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task_edit', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager_app/task_form.html')

    def test_task_edit_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('task_edit', args=[self.task.pk]), {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': Task.Status.DONE,
            'priority': Task.Priority.high
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, Task.Status.DONE)
        self.assertEqual(self.task.priority, Task.Priority.high)

    def test_task_delete_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager_app/task_confirm_delete.html')

    def test_task_delete_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_detail_view_post_comment(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('task_detail', args=[self.task.pk]), {
            'text': 'New Comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_detail', args=[self.task.pk]))
        self.assertTrue(Comment.objects.filter(text='New Comment').exists())
