from django.urls import path
from task_manager.users import views

app_name = "users"
urlpatterns = [
    path("create/", views.UsersCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.UsersUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.UsersDeleteView.as_view(), name="delete"),
    path("", views.UsersIndexView.as_view(), name="index"),
]
