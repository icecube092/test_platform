from django import forms
from django.contrib.auth import authenticate

from stud_teach.models import Teacher, Student


class CreateUserForm(forms.Form):
    """
    форма для регистрации
    """
    login = forms.CharField(max_length=20, error_messages={"required": "Укажите логин"}, label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=32)
    password_again = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=32)
    email = forms.EmailField()
    teacher = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()
        login = cleaned_data.get("login")
        password = cleaned_data.get("password")
        password_again = cleaned_data.get("password_again")
        email = cleaned_data.get("email")
        if password != password_again:
            self.add_error("password_again", "Пароли должны совпадать!")
        if Teacher.objects.filter(username=login) or Student.objects.filter(username=login):
            self.add_error("login", "Логин занят")
        if Teacher.objects.filter(email=email) or Student.objects.filter(email=email):
            self.add_error("email", "Емэйл занят")
        return self.cleaned_data


class UserAuthorize(forms.Form):
    """
    форма для авторизации
    """
    login = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(UserAuthorize, self).clean()
        login = cleaned_data.get("login")
        password = cleaned_data.get("password")
        if not authenticate(username=login, password=password):
            self.add_error("password", "Неверный логин или пароль")
        return self.cleaned_data


class Profile(forms.Form):
    avatar = forms.ImageField()
    phone = forms.CharField()