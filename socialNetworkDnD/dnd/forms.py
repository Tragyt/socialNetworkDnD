from django import forms
from django.contrib.auth.models import User

from dnd.models import Profile


# widget=forms.FileInput(),
class UpdateProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control mb-3"}), required=False)
    experience = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": "3"}), required=False)
    img = forms.FileField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Profile
        fields = ("bio", "img", "experience")


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control mb-3"}), required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control mb-3"}), required=False)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
