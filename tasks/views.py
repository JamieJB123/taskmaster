from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def home(request):
    """Logic for the 'task form'"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Save the new task to the database
            new_task = form.save(commit=False)
            new_task.completed_status = False # Default to not completed
            new_task.save()
            return redirect('home') # Redirect to the home page after saving
    else:
        form = TaskForm() # Reinitialize the form if it's not valid


    # Fetch tasks based on their completion status
    to_do_tasks = Task.objects.filter(completed_status=False).order_by("due_date")
    done_tasks = Task.objects.filter(completed_status=True).order_by("due_date")

    # Pass the form and tasks to the template
    context = {
        'form': form,  # The TaskForm instance
        'to_do_tasks': to_do_tasks,
        'done_tasks': done_tasks,
    }
    return render(request, 'tasks/index.html', context)

def mark_as_complete(request, task_id):
    """Mark a task as complete."""
    task = get_object_or_404(Task, id=task_id)
    task.completed_status = True
    task.save()
    return redirect('home')

def mark_as_uncomplete(request, task_id):
    """Mark a task as uncomplete."""
    task = get_object_or_404(Task, id=task_id)
    task.completed_status = False
    task.save()
    return redirect('home')

def delete_task(request, task_id):
    """Delete a task."""
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('home')
