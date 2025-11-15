from django.urls import path

from task_manager.statuses import views

app_name = "statuses"
urlpatterns = [
    path("create/", views.StatusesCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.StatusesUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.StatusesDeleteView.as_view(), name="delete"),
    path("", views.StatusesIndexView.as_view(), name="index"),
]
