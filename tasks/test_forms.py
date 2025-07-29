from django.test import TestCase
from tasks.forms import TaskForm
from tasks.models import Category

class TaskFormTestCase(TestCase):
    """Test suite for the TaskForm."""

    def setUp(self):
        """Set up test dependencies."""
        # Create a Category instance
        self.category = Category.objects.create(name="Test Category")
        # Create a valid TaskForm instance
        self.valid_data = {
            'title': 'Test Task',
            'due_date': '2023-10-01',
            'category': self.category.id
        }

    def test_task_form_valid_data(self):
        """Test that the form is valid with correct data."""
        form = TaskForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.due_date.strftime('%Y-%m-%d'), '2023-10-01')
        self.assertEqual(task.category, self.category)

    def test_task_form_missing_title(self):
        """Test that the form is invalid if the title is missing."""
        invalid_data = self.valid_data.copy()
        invalid_data['title'] = ''
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_task_form_missing_due_date(self):
        """Test that the form is invalid if the due date is missing."""
        invalid_data = self.valid_data.copy()
        invalid_data['due_date'] = ''
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)

    def test_task_form_missing_category(self):
        """Test that the form is invalid if the category is missing."""
        invalid_data = self.valid_data.copy()
        invalid_data['category'] = ''
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_task_form_invalid_due_date_format(self):
        """Test that the form is invalid if the due date format is incorrect."""
        invalid_data = self.valid_data.copy()
        invalid_data['due_date'] = 'invalid-date'
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)

    def test_task_form_exceeding_title_max_length(self):
        """Test that the form is invalid if the title exceeds the max length."""
        invalid_data = self.valid_data.copy()
        invalid_data['title'] = 'A' * 101  # Assuming max_length=100
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
