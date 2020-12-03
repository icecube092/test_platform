from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from stud_teach.forms import CreateUserForm

from stud_teach.models import Teacher, Student

from stud_teach.forms import UserAuthorize


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get("teacher"):
                user = Teacher()
            else:
                user = Student()
            user.username = form.cleaned_data.get("login")
            user.set_password(form.cleaned_data.get("password"))
            user.email = form.cleaned_data.get("email")
            user.save()
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
            return HttpResponseRedirect("/tests/1")
        else:
            return render(request, "registration/login.html", {"form": form})
    else:
        form = UserAuthorize()
        return render(request, "registration/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/tests/1")


def profile(request):
    """
    профиль пользователя
    """
    user_id = request.GET.get("user_id")
    edit = request.GET.get("edit")
    profile = get_object_or_404(UserProfile, id=user_id)
    projects = profile.project_set.all()
    is_owner = profile.id == request.user.id
    if edit and is_owner:
        if request.method == "GET":
            form = EditProfileForm(initial={"level": profile.level,
                                            "about": profile.about})
            return render(request, "user_info/edit_profile.html",
                          {"form": form, "profile": profile})
        elif request.method == "POST":
            form = EditProfileForm(request.POST)
            if form.is_valid():
                level = form.cleaned_data["level"]
                for level_set in UserProfile.LEVELS:
                    if level in level_set:
                        profile.level = level_set[1]
                        break
                profile.about = form.cleaned_data["about"]
                profile.save()
            return render(request, "user_info/edit_profile.html",
                          {"form": form})
    else:
        return render(request, "user_info/profile.html",
                      {"profile": profile, "is_owner": is_owner,
                       "projects": projects})
