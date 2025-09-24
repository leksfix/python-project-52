from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.models import User

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
        ]

    def clean_username(self):
        # To skip user existance check
        return self.cleaned_data.get("username")


class UserUpdateForm(UserCreateForm):
    pass
