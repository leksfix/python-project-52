from django.urls import path

from task_manager.tasks import views

app_name = "tasks"
urlpatterns = [
    path("create/", views.TasksCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.TasksUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.TasksDeleteView.as_view(), name="delete"),
    path("<int:pk>/", views.TasksDetailView.as_view(), name="detail"),
    path("", views.TasksIndexView.as_view(), name="index"),
]
