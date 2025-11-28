from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from typing import Dict, Any
from .models import Task

# Create your tests here.
# myapp/tests.py

class TaskModelTestCase(TestCase):
    """
    Test cases for the Task model.
    Tests model creation, validation, and custom methods.
    """
    
    def setUp(self) -> None:
        """Set up test data before each test method."""
        self.task_data: Dict[str, Any] = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'high',
        }
    
    def test_task_creation(self) -> None:
        """Test that a task can be created with all fields."""
        task = Task.objects.create(**self.task_data)
        
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.priority, 'high')
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)
    
    def test_task_str_representation(self) -> None:
        """Test the string representation of a task."""
        task = Task.objects.create(title='My Task')
        self.assertEqual(str(task), 'My Task')
    
    def test_task_default_values(self) -> None:
        """Test that default values are set correctly."""
        task = Task.objects.create(title='Default Task')
        
        self.assertFalse(task.completed)
        self.assertEqual(task.priority, 'medium')
        self.assertIsNone(task.description)
        self.assertIsNone(task.due_date)
    
    def test_task_is_overdue_method(self) -> None:
        """Test the is_overdue() method logic."""
        # Task with past due date and not completed
        past_date = timezone.now() - timedelta(days=1)
        overdue_task = Task.objects.create(
            title='Overdue Task',
            due_date=past_date,
            completed=False
        )
        self.assertTrue(overdue_task.is_overdue())
        
        # Task with future due date
        future_date = timezone.now() + timedelta(days=1)
        future_task = Task.objects.create(
            title='Future Task',
            due_date=future_date,
            completed=False
        )
        self.assertFalse(future_task.is_overdue())
        
        # Completed task with past due date
        completed_task = Task.objects.create(
            title='Completed Task',
            due_date=past_date,
            completed=True
        )
        self.assertFalse(completed_task.is_overdue())
        
        # Task without due date
        no_due_date_task = Task.objects.create(title='No Due Date')
        self.assertFalse(no_due_date_task.is_overdue())
    
    def test_task_ordering(self) -> None:
        """Test that tasks are ordered by created_at descending."""
        task1 = Task.objects.create(title='First Task')
        task2 = Task.objects.create(title='Second Task')
        
        tasks = Task.objects.all()
        self.assertEqual(tasks[0], task2)  # Newest first
        self.assertEqual(tasks[1], task1)


class TaskViewTestCase(TestCase):
    """
    Test cases for Task views.
    Tests all CRUD operations and view responses.
    """
    
    def setUp(self) -> None:
        """Set up test client and sample data."""
        self.client = Client()
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            priority='medium'
        )
    
    def test_task_list_view_get(self) -> None:
        """Test that task list view returns tasks."""
        response = self.client.get(reverse('task_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
        self.assertIn('tasks', response.context)
        self.assertEqual(len(response.context['tasks']), 1)
    
    def test_task_list_view_empty(self) -> None:
        """Test task list view with no tasks."""
        Task.objects.all().delete()
        response = self.client.get(reverse('task_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 0)
    
    def test_task_create_view_get(self) -> None:
        """Test that create view displays form."""
        response = self.client.get(reverse('task_create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'title')
    
    def test_task_create_view_post(self) -> None:
        """Test creating a new task via POST."""
        task_count_before = Task.objects.count()
        
        response = self.client.post(reverse('task_create'), {
            'title': 'New Task',
            'description': 'New Description',
            'priority': 'high',
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Task.objects.count(), task_count_before + 1)
        
        new_task = Task.objects.get(title='New Task')
        self.assertEqual(new_task.description, 'New Description')
        self.assertEqual(new_task.priority, 'high')
    
    def test_task_update_view_get(self) -> None:
        """Test that update view displays task data."""
        response = self.client.get(
            reverse('task_update', kwargs={'pk': self.task.pk})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
    
    def test_task_update_view_post(self) -> None:
        """Test updating a task via POST."""
        response = self.client.post(
            reverse('task_update', kwargs={'pk': self.task.pk}),
            {
                'title': 'Updated Task',
                'description': 'Updated Description',
                'priority': 'low',
                'completed': 'on',
            }
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect
        
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')
        self.assertEqual(self.task.priority, 'low')
        self.assertTrue(self.task.completed)
    
    def test_task_delete_view_get(self) -> None:
        """Test that delete confirmation page displays."""
        response = self.client.get(
            reverse('task_delete', kwargs={'pk': self.task.pk})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
    
    def test_task_delete_view_post(self) -> None:
        """Test deleting a task via POST."""
        task_count_before = Task.objects.count()
        task_pk = self.task.pk
        
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task_pk})
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Task.objects.count(), task_count_before - 1)
        self.assertFalse(Task.objects.filter(pk=task_pk).exists())
    
    def test_task_toggle_complete(self) -> None:
        """Test toggling task completion status."""
        self.assertFalse(self.task.completed)
        
        response = self.client.get(
            reverse('task_toggle_complete', kwargs={'pk': self.task.pk})
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect
        
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)
        
        # Toggle again
        self.client.get(
            reverse('task_toggle_complete', kwargs={'pk': self.task.pk})
        )
        
        self.task.refresh_from_db()
        self.assertFalse(self.task.completed)
    
    def test_task_update_nonexistent_returns_404(self) -> None:
        """Test that updating non-existent task returns 404."""
        response = self.client.get(
            reverse('task_update', kwargs={'pk': 99999})
        )
        
        self.assertEqual(response.status_code, 404)
    
    def test_task_delete_nonexistent_returns_404(self) -> None:
        """Test that deleting non-existent task returns 404."""
        response = self.client.get(
            reverse('task_delete', kwargs={'pk': 99999})
        )
        
        self.assertEqual(response.status_code, 404)


class TaskURLTestCase(TestCase):
    """
    Test cases for URL routing.
    Tests that all URLs resolve correctly.
    """
    
    def setUp(self) -> None:
        """Set up test data."""
        self.task = Task.objects.create(title='Test Task')
    
    def test_task_list_url_resolves(self) -> None:
        """Test that task list URL resolves."""
        url = reverse('task_list')
        self.assertEqual(url, '/tasks/')
    
    def test_task_create_url_resolves(self) -> None:
        """Test that task create URL resolves."""
        url = reverse('task_create')
        self.assertEqual(url, '/tasks/create/')
    
    def test_task_update_url_resolves(self) -> None:
        """Test that task update URL resolves."""
        url = reverse('task_update', kwargs={'pk': self.task.pk})
        self.assertEqual(url, f'/tasks/{self.task.pk}/update/')
    
    def test_task_delete_url_resolves(self) -> None:
        """Test that task delete URL resolves."""
        url = reverse('task_delete', kwargs={'pk': self.task.pk})
        self.assertEqual(url, f'/tasks/{self.task.pk}/delete/')