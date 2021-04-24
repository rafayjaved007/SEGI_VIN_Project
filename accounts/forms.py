from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class SignUpForm(UserCreationForm):
    date_of_birth = forms.DateField()

    class Meta:
        # Only the fields that we specify in fields attribute of Meta class with be saved
        # automatically in concerned Model e.g. date_of_birth will not be saved automatically
        model = User
        fields = ('email', 'username',)
