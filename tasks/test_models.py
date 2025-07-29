from django.test import TestCase
from django.core.exceptions import ValidationError
from tasks.models import Task, Category

class TaskModelTestCase(TestCase):
    """Test suite for the Task model."""

    def setUp(self):
        """Set up test dependencies."""
        # Create a Category instance
        self.category = Category.objects.create(name="Test Category")
        # Create a Task instance
        self.task = Task.objects.create(
            title="Test Task",
            due_date="2023-10-01",
            completed_status=False,
            category=self.category
        )

    def test_task_creation(self):
        """Test that a Task instance can be created."""
        self.assertIsInstance(self.task, Task)
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.due_date, "2023-10-01")
        self.assertFalse(self.task.completed_status)
        self.assertEqual(self.task.category, self.category)

    def test_task_string_representation(self):
        """Test the string representation of a Task instance."""
        self.assertEqual(str(self.task), "In TEST CATEGORY category: Test Task")

    def test_task_due_date(self):
        """Test the due_date field of a Task instance."""
        self.assertEqual(self.task.due_date, "2023-10-01")

    def test_task_completed_status_default(self):
        """Test the default value of the completed_status field."""
        task = Task.objects.create(
            title="New Task",
            due_date="2023-10-02",
            category=self.category
        )
        self.assertFalse(task.completed_status)

    def test_task_category_relationship(self):
        """Test the relationship between Task and Category."""
        self.assertEqual(self.task.category.name, "Test Category")
        self.assertIn(self.task, self.category.tasks.all())

    def test_task_title_max_length(self):
        """Test that a Task title exceeding max length raises a ValidationError."""
        long_title = "A" * 101  # Assuming max_length=100
        task = Task(
            title=long_title,
            due_date="2023-10-01",
            completed_status=False,
            category=self.category
        )
        with self.assertRaises(ValidationError):
            task.full_clean()  # This validates the model fields
            task.save()
