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


class UserUpdateForm(UserCreateForm):

    def clean_username(self):
        new_username = self.cleaned_data.get("username")
        old_username = self.instance.username
        if new_username.lower() == old_username.lower():
            # Skip user existance check
            return new_username
        
        return super().clean_username()

