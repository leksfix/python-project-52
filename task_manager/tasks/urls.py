from django.urls import path
from task_manager.tasks import views
from django_filters.views import FilterView
from task_manager.tasks.models import Task


urlpatterns = [
    path("create/", views.TasksCreateView.as_view(), name="tasks_create"),
    path("<int:pk>/update/", views.TasksUpdateView.as_view(), name="tasks_update"),
    path("<int:pk>/delete/", views.TasksDeleteView.as_view(), name="tasks_delete"),
    path("<int:pk>/", views.TasksDetailView.as_view(), name="tasks_detail"),
    #path("", views.TasksIndexView.as_view(), name="tasks_index"),
    path("", FilterView.as_view(
        model=Task,
        filterset_fields = ["status", "assignee", "labels"]
    ), name="tasks_index"),
]
