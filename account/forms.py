from django import forms
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class RegistrationForm(forms.Form):
    username = forms.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=30,
        widget=forms.TextInput(attrs={"class": "required"}),
        label="Username",
        error_message={
            'invalid': "This value may contain only \
                            letters, numbers and @.+- characters."}
    )
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data["username"]
        existing = get_user_model().objects.filter(username__iexact=username)
        if existing.exists():
            raise forms.ValidationError("A user with that \
                                        username already exists.")
        else:
            return self.cleaned_data["username"]


class SettingsForm(forms.Form):
    email = forms.EmailField()

'''
class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = "__all__"
'''
