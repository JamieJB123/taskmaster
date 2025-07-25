from django.shortcuts import render
from .models import Task

def home(request):
    # Fetch tasks based on their completion status
    to_do_tasks = Task.objects.filter(completed_status=False).order_by("due_date")
    done_tasks = Task.objects.filter(completed_status=True).order_by("due_date")

    # Pass the tasks to the template
    context = {
        'to_do_tasks': to_do_tasks,
        'done_tasks': done_tasks,
    }
    return render(request, 'tasks/index.html', context)
