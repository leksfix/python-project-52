from django.urls import path

from task_manager.labels import views

app_name = "labels"
urlpatterns = [
    path("create/", views.LabelsCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.LabelsUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.LabelsDeleteView.as_view(), name="delete"),
    path("", views.LabelsIndexView.as_view(), name="index"),
]
