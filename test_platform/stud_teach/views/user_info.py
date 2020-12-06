from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from stud_teach.forms import CreateUserForm

from stud_teach.models import Teacher, Student

from stud_teach.forms import UserAuthorize

from stud_teach.forms import ProfileForm


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get("teacher"):
                user = Teacher()
                user.is_staff = True
            else:
                user = Student()
            user.username = form.cleaned_data.get("login")
            user.set_password(form.cleaned_data.get("password"))
            user.email = form.cleaned_data.get("email")
            user.save()
            if isinstance(user, Teacher):
                group = Group.objects.get(name="Teachers")  # предварительно нужно создать группу
                group.user_set.add(user)
            authenticate(username = user.username, password = user.password)
            return HttpResponseRedirect("/login/")
        else:
            return render(request, "registration/register.html", {"form": form})
    else:
        form = CreateUserForm()
        return render(request, "registration/register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = UserAuthorize(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get("login"),
                                password=form.cleaned_data.get("password"))
            login(request, user)
            return HttpResponseRedirect(reverse("tests_list", args=[1]))
        else:
            return render(request, "registration/login.html", {"form": form})
    else:
        form = UserAuthorize()
        return render(request, "registration/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("tests_list", args=[1]))


class Profile(View):
    def get(self, request):
        user_id = request.GET.get("user_id")
        if user_id:
            try:
                user = Student.objects.get(id=user_id)
            except Student.DoesNotExist:
                return HttpResponseRedirect(reverse("tests_list", args=[1]))
            is_owner = request.user.id == user.id
            tests = user.done_tests.all()
            form = ProfileForm(instance=user)
            return render(request, "profile.html",
                          {"user": user, "is_owner": is_owner, "tests": tests, "form": form})
        else:
            return HttpResponseRedirect(reverse("tests_list", args=[1]))

    def post(self, request):
        user_id = request.GET.get("user_id")
        if user_id:
            try:
                user = Student.objects.get(id=user_id)
            except Student.DoesNotExist:
                return HttpResponseRedirect(reverse("tests_list", args=[1]))
            form = ProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(f"{reverse('profile')}?user_id={user_id}")
        else:
            return HttpResponseRedirect(reverse("tests_list", args=[1]))