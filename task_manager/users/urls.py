from django.urls import path
from task_manager.users import views

urlpatterns = [
    path("create/", views.UsersCreateView.as_view(), name="users_create"),
    path("<int:pk>/update/", views.UsersUpdateView.as_view(), name="users_update"),
    path("<int:pk>/delete/", views.UsersDeleteView.as_view(), name="users_delete"),
    path("", views.UsersIndexView.as_view(), name="users_index"),
]
