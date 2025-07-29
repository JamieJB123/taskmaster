from django.test import TestCase
from django.urls import reverse
from tasks.models import Task, Category

class HomeViewTestCase(TestCase):
    """Test suite for the home view."""

    def setUp(self):
        """Set up test dependencies."""
        # Create a Category instance
        self.category = Category.objects.create(name="Test Category")
        # Create some Task instances
        self.task1 = Task.objects.create(
            title="Test Task 1",
            due_date="2023-10-01",
            completed_status=False,
            category=self.category
        )
        self.task2 = Task.objects.create(
            title="Test Task 2",
            due_date="2023-10-02",
            completed_status=True,
            category=self.category
        )

    def test_home_view_status_code(self):
        """Test that the home view returns a 200 status code."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')


    def test_home_view_template_used(self):
        """Test that the home view uses the correct template."""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_home_view_context_data(self):
        """Test that the home view provides the correct context data."""
        response = self.client.get(reverse('home'))
        self.assertIn('form', response.context)
        self.assertIn('to_do_tasks', response.context)
        self.assertIn('done_tasks', response.context)
        self.assertEqual(response.context['to_do_tasks'].count(), 1)
        self.assertEqual(response.context['done_tasks'].count(), 1)

    def test_home_view_post_request_creates_task(self):
        """Test that a POST request to the home view creates a new task."""
        response = self.client.post(reverse('home'), {
            'title': 'New Task',
            'due_date': '2023-10-03',
            'category': self.category.id
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertEqual(Task.objects.count(), 3)

    def test_home_view_redirect_after_post(self):
        """Test that the home view redirects after a successful POST request."""
        response = self.client.post(reverse('home'), {
            'title': 'New Task',
            'due_date': '2023-10-03',
            'category': self.category.id
        })
        self.assertRedirects(response, reverse('home'))
