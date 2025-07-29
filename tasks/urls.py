from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('complete/<int:task_id>/', views.mark_as_complete, name='mark_as_complete'),  # Mark as complete
    path('uncomplete/<int:task_id>/', views.mark_as_uncomplete, name='uncomplete_task'),  # Mark as uncomplete
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),  # Delete task
]
