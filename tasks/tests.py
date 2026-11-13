from dataclasses import dataclass

from django.contrib.auth.models import User
from django.template.defaultfilters import title
from django.urls import reverse
from django.views.generic import detail
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.task1 = Task.objects.create(title='Первая задача',description='Описание 1', completed=False)
        self.task2 = Task.objects.create(title='Вторая задача',description='Описание 2', completed=True)
        self.list_url = reverse('task-list')

    def test_unauthenticated_access_denied(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_task_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)


    def test_get_task_detail(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Новая задача','description': 'Новое описание', 'completed': True}
        response = self.client.post(self.list_url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_update_task(self):
        self.client.force_authenticate(user=self.user)
        detail_url = reverse('task-detail', args =[self.task1.id])
        data = {'title':'Обновленная задача','description': 'Новое описание', 'completed': True}
        response = self.client.put(detail_url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.completed)

    def test_delete_task(self):
        self.client.force_authenticate(user=self.user)
        detail_url = reverse('task-detail', args=[self.task1.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)

    def test_filter_tasks_by_status(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url,{'completed':True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'],'Вторая задача')






