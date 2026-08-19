from django.contrib.auth.forms import UserCreationForm

from menu_mvp.accounts.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
