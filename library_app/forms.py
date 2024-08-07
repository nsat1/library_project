from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Reader


class ReaderRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_reader = True

        if commit:
            user.save()
            Reader.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                address=self.cleaned_data['address']
            )

        return user
