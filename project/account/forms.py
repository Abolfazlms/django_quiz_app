from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ("username", "phone_number", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.phone_number = self.cleaned_data["phone_number"]
        if commit:
            user.save()
        return user
